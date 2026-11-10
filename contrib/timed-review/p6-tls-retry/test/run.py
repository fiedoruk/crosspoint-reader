#!/usr/bin/env python3
"""Pinned SecureClient before/after against real loopback TLS; no hardware."""
import argparse,hashlib,json,resource,shutil,subprocess,sys,tempfile,time
from pathlib import Path
P=argparse.ArgumentParser(); P.add_argument('--cp',type=Path,required=True); P.add_argument('--baseline',type=Path,required=True); P.add_argument('--fixture',type=Path,required=True); P.add_argument('--wolf-root',type=Path,required=True); P.add_argument('--wolf-archive',type=Path,required=True); P.add_argument('--output',type=Path,required=True); a=P.parse_args()
sys.dont_write_bytecode=True; sys.path.insert(0,str(a.fixture.resolve())); from fixture import Fixture
here=Path(__file__).resolve().parent
flags=['-std=c++20','-O0','-w','-fsanitize=address,undefined','-fno-omit-frame-pointer','-DFREEINK_NET_WOLFSSL=1','-DWOLFSSL_USER_SETTINGS','-DWOLFSSL_OPTIONS_H','-DWOLFSSL_CLIENT_EXAMPLE','-DWOLFSSL_TLS13','-DWOLFSSL_HAVE_SP_ECC','-DWOLFSSL_SP_SMALL','-DHAVE_CURVE25519','-DHAVE_SNI']
commands=[]; results=[]; started=time.monotonic()
def run(cmd,**kwargs):
 p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True,**kwargs); commands.append({'cmd':[str(x) for x in cmd],'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 if p.returncode: a.output.write_text(json.dumps({'status':'FAIL','commands':commands},indent=2)); raise RuntimeError(p.stderr[-3000:])
 return p
with tempfile.TemporaryDirectory(prefix='p6-tls-') as tmp:
 t=Path(tmp); stub=t/'stubs'; shutil.copytree(a.cp/'test/plugin_verified_tls/transport_stubs',stub)
 p=stub/'WiFiClient.h'; s=p.read_text().replace('class WiFiClient :','inline unsigned p6TcpAttempts=0;\ninline int p6OpenSockets=0;\nclass WiFiClient :').replace('int connect(const char*, uint16_t port) override {','int connect(const char*, uint16_t port) override {\n    ++p6TcpAttempts;').replace('if (fd_ < 0) return false;\n    sockaddr_in','if (fd_ < 0) return false;\n    ++p6OpenSockets;\n    sockaddr_in').replace('close(fd_);','close(fd_);\n      --p6OpenSockets;'); p.write_text(s)
 programs={}
 for name,src in [('baseline',a.baseline),('fixed',a.cp/'freeink-sdk/libs/network/SecureNet')]:
  inc=flags+['-I',str(stub),'-I',str(src/'include'),'-I',str(a.wolf_root)]
  obj=t/(name+'.o'); exe=t/name
  run(['nice','-n','10','c++',*inc,'-DwolfSSL_connect=p6Connect','-DwolfSSL_check_domain_name=p6Domain','-c',src/'src/SecureClient.cpp','-o',obj])
  run(['nice','-n','10','c++',*inc,here/'retry_client.cpp',obj,a.wolf_archive,'-o',exe]); programs[name]=exe
 with Fixture(t/'fixture',host='good.test') as f:
  ca=t/'ca.pem'; ca.write_bytes(f.root); bad=t/'bad.pem'; bad.write_text('not PEM'); unknown=t/'unknown.pem'; unknown.write_bytes(f.unknown)
  for variant,exe in programs.items():
   for case,endpoint,trust,mode in [('good12','tls12',ca,'normal'),('good13','tls13',ca,'normal'),('wronghost','wronghost',ca,'normal'),('unknownca','tls12',unknown,'normal'),('badca','tls12',bad,'normal'),('setup','tls12',ca,'setup'),('fallback','tls12',ca,'fallback'),('cancel','tls12',ca,'cancel'),('budget','tls12',ca,'budget'),('cancel-second','tls12',ca,'cancel-second'),('budget-second','tls12',ca,'budget-second'),('timeout','tls12',ca,'timeout')]:
    server=f.endpoints[endpoint]; before=len(server.requests)
    proc=run([exe,server.port,trust,mode,ca,f.endpoints['tls12'].port],timeout=10); x=json.loads(proc.stdout); n=len(server.requests)-before
    success=case in ('good12','good13','fallback'); expectTcp=2 if case in ('fallback','cancel-second','budget-second') or (variant=='baseline' and case in ('wronghost','unknownca','badca','setup','timeout')) else 1
    assert x['connected']==success and x['tcp']==expectTcp and n==int(success),(variant,case,x,n)
    assert x['closed'] and x['open_sockets']==0,(variant,case,x)
    assert x['recovered'],(variant,case,x)
    assert x['aborted']==(case in ('cancel','budget','cancel-second','budget-second')),(variant,case,x)
    if case in ('badca','setup'): assert x['handshakes']==0
    item={'variant':variant,'case':case,'observed':x,'requests':n,'pass':True}; results.append(item); print(json.dumps(item),flush=True)
a.output.write_text(json.dumps({'status':'PASS','cases':results,'commands':commands,'wallSeconds':time.monotonic()-started,'cpuSeconds':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,'archiveSha256':hashlib.sha256(a.wolf_archive.read_bytes()).hexdigest(),'limits':['HOST POSIX; no device heap/energy','first negotiation failure injected; second handshake real','wolfSSL static library not sanitizer-instrumented','MFL/retention off in reused archive']},indent=2)+'\n')
