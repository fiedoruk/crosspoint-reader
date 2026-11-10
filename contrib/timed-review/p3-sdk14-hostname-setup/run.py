#!/usr/bin/env python3
"""Compare pinned SecureClient implementations with G10's real loopback TLS.

The domain-setup fault returns wolfSSL's documented failure and mirrors its
MEMORY_ERROR state without allocating a hostname. It does not simulate MCU heap.
"""
import hashlib
import json
import os
import resource
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
G10 = HERE / 'fixture'
WOLF = Path(os.environ['P3_WOLFSSL_SRC']).resolve()
ARCHIVE = Path(os.environ['P3_WOLFSSL_ARCHIVE']).resolve()
sys.path.insert(0, str(G10))
sys.dont_write_bytecode = True
from fixture import Fixture

FLAGS = ['-std=c++20', '-O0', '-w', '-DFREEINK_NET_WOLFSSL=1',
         '-DWOLFSSL_USER_SETTINGS', '-DWOLFSSL_OPTIONS_H', '-DWOLFSSL_CLIENT_EXAMPLE',
         '-DWOLFSSL_TLS13', '-DWOLFSSL_HAVE_SP_ECC', '-DWOLFSSL_SP_SMALL',
         '-DHAVE_CURVE25519', '-DHAVE_SNI']
SOURCE = 'libs/network/SecureNet/src/SecureClient.cpp'
HEADER = 'libs/network/SecureNet/include/SecureClient.h'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    started = time.monotonic()
    commands, cases = [], []
    def run(command, **kwargs):
        now = time.monotonic()
        result = subprocess.run(command, capture_output=True, text=True, **kwargs)
        commands.append({'command': [str(c) for c in command], 'exit': result.returncode,
                         'wall_seconds': round(time.monotonic()-now, 3),
                         'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode:
            (HERE/'contract-failure.json').write_text(json.dumps(commands, indent=2)+'\n')
            raise RuntimeError(result.stderr[-4000:] or result.stdout)
        return result
    sources = {name: {'cpp_sha256': digest(HERE/'sources'/name/SOURCE),
                      'header_sha256': digest(HERE/'sources'/name/HEADER)}
               for name in ['pr14', 'pr14-fixed']}
    with tempfile.TemporaryDirectory(prefix='p3-tls-', dir=HERE) as tempdir:
        temp = Path(tempdir)
        stub = temp/'stubs'; stub.mkdir()
        for name in ['Arduino.h', 'Client.h', 'WiFiClient.h', 'Network.h']:
            shutil.copyfile(HERE/'transport_stubs'/name, stub/name)
        wifi = stub/'WiFiClient.h'
        wifi.write_text(wifi.read_text().replace('class WiFiClient :', 'inline unsigned p3TcpAttempts = 0;\nclass WiFiClient :')
                        .replace('int connect(const char*, uint16_t port) override {',
                                 'int connect(const char*, uint16_t port) override {\n    ++p3TcpAttempts;'))
        (stub/'esp_heap_caps.h').write_text('#pragma once\n#include <cstddef>\n#define MALLOC_CAP_DEFAULT 0\ninline size_t esp_get_free_heap_size(){return 1000000;}\ninline size_t heap_caps_get_largest_free_block(unsigned){return 1000000;}\n')
        programs = {}
        for variant, folder, extra in [
            ('pr14-certs-on', 'pr14', ['-DFREEINK_NET_WOLFSSL_CERTS=1', '-DP3_PR14']),
            ('pr14-fixed', 'pr14-fixed', ['-DFREEINK_NET_WOLFSSL_CERTS=1', '-DP3_PR14'])]:
            sdk = HERE/'sources'/folder
            flags = FLAGS + extra + ['-I', str(stub), '-I', str(sdk/Path(HEADER).parent), '-I', str(WOLF)]
            obj = temp/(variant+'.o')
            run(['nice','-n','10','c++',*flags,'-DwolfSSL_connect=p3Connect',
                 '-DwolfSSL_check_domain_name=p3Domain','-c',str(sdk/SOURCE),'-o',str(obj)])
            executable = temp/variant
            run(['nice','-n','10','c++',*flags,str(HERE/'contract_client.cpp'),str(obj),str(ARCHIVE),'-o',str(executable)])
            programs[variant] = executable
        with Fixture(temp/'fixture', host='good.test') as fixture:
            root, unknown, malformed = temp/'root.pem', temp/'unknown.pem', temp/'malformed.pem'
            root.write_bytes(fixture.root); unknown.write_bytes(fixture.unknown); malformed.write_text('not a PEM')
            matrix = [('good12','tls12',root,False,False),
                      ('wronghost','wronghost',root,False,False),
                      ('domain-setup-failure','wronghost',root,True,False)]
            for variant, executable in programs.items():
                for case, endpoint, ca, fault, insecure in matrix:
                    server = fixture.endpoints[endpoint]
                    before = len(server.requests)
                    result = run([str(executable), str(server.port), str(ca),
                                  'fault' if fault else 'normal', 'insecure' if insecure else 'verified'], timeout=8)
                    observed = json.loads(result.stdout)
                    marker = len(server.requests)-before
                    # Expected observations describe the pinned source, including
                    # fail-open controls. PASS is not a product qualification.
                    accepts_wrong = variant == 'main' or variant == 'pr14-certs-absent'
                    expected = case in ['good12','good13','legacy-insecure'] or (case == 'wronghost' and accepts_wrong)
                    if case in ['unknownca','malformedca'] and variant == 'pr14-certs-absent': expected = True
                    if case == 'domain-setup-failure': expected = (variant.startswith('pr14') and variant != 'pr14-fixed') or variant == 'main'
                    passed = observed['connected'] == expected and marker == int(expected)
                    item = {'variant':variant, 'case':case, 'pass':passed,
                            'protected_request_count':marker, 'observed':observed}
                    cases.append(item)
                    print(json.dumps(item), flush=True)
                    if not passed:
                        raise RuntimeError('Observation differed from reviewed source: '+str(item))
            fixture_result = fixture.snapshot()
    result = {'status':'PASS', 'cases':cases, 'commands':commands, 'sources':sources,
              'archive_sha256':digest(ARCHIVE), 'wolfssl':'Arduino-wolfSSL 5.7.2',
              'fixture':fixture_result, 'wall_seconds':round(time.monotonic()-started,3),
              'child_cpu_seconds':round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,3),
              'limits':['HOST POSIX transport; no device heap measurement',
                        'hostname setup failure injected at API boundary with MEMORY_ERROR state',
                        'HAVE_MAX_FRAGMENT and input retention are off in this older reusable host archive',
                        'MFL evidence is retained from G12, not rerun here',
                        'raw14 pinned source versus only the supplied setup-return guard']}
    filename = 'replay-results.json'
    (HERE/filename).write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS {len(cases)} actual-source TLS observations; failure controls are explicit; DEVICE NOT_MEASURED')

if __name__ == '__main__': main()
