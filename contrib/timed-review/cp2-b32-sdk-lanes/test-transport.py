#!/usr/bin/env python3
"""Target actual W06 PluginHttp, SDK parser and wolfSSL via loopback."""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('checkout', type=Path)
p.add_argument('--wolf-root', type=Path, required=True)
p.add_argument('--wolf-archive', type=Path, required=True)
p.add_argument('--arduinojson', type=Path, required=True)
a = p.parse_args()
root = a.checkout.resolve(); here = root/'test/plugin_verified_tls'
sys.path.insert(0, str(here))
from tls_fixture import LoopbackTLS, issue, pem_cert, pem_key
sdk = root/'freeink-sdk/libs/network/SecureNet'
flags = ['-std=c++20','-O0','-w','-DFREEINK_NET_WOLFSSL=1','-DWOLFSSL_USER_SETTINGS','-DWOLFSSL_OPTIONS_H','-DWOLFSSL_CLIENT_EXAMPLE','-DWOLFSSL_TLS13','-DWOLFSSL_HAVE_SP_ECC','-DWOLFSSL_SP_SMALL','-DHAVE_CURVE25519','-DHAVE_SNI','-DHAVE_MAX_FRAGMENT']
with tempfile.TemporaryDirectory(prefix='p4-http-') as d:
    tmp=Path(d); exe=tmp/'check'
    cmd=['nice','-n','10','c++',*flags]
    for path in [here/'transport_stubs',sdk/'include',a.wolf_root/'src',root/'test/plugin_verified_http/stubs',root/'test/plugin_event_budget/stubs',a.arduinojson,root/'src',root/'lib/GfxRenderer',root/'lib/Memory']:
        cmd+=['-I',str(path)]
    for path in [sdk/'src/SecureClient.cpp',root/'src/util/PluginHttp.cpp',root/'src/util/PluginEventAsset.cpp',root/'lib/GfxRenderer/Bitmap.cpp',root/'lib/GfxRenderer/BitmapHelpers.cpp',here/'NativeHttpTest.cpp']:
        cmd.append(str(path))
    cmd += [str(a.wolf_archive),'-o',str(exe)]
    print('compile:', ' '.join(cmd), flush=True)
    subprocess.run(cmd,check=True)
    data=bytearray(94); data[:2]=b'BM'
    for at,value in [(2,94),(10,62),(14,40),(18,8),(22,8)]: data[at:at+4]=value.to_bytes(4,'little')
    data[26]=data[28]=1; data[58:61]=b'\xff\xff\xff'
    frame=tmp/'frame.bmp'; frame.write_bytes(data)
    key,ca=issue('Test root',ca=True); capath=tmp/'root.pem'; capath.write_bytes(pem_cert(ca))
    leafkey,leaf=issue('leaf',key,ca,'good.test'); cert=tmp/'leaf.pem'; secret=tmp/'leaf.key'; cert.write_bytes(pem_cert(leaf)); secret.write_bytes(pem_key(leafkey))
    cases=[('valid-large-csp','download',bytes(data),b'Content-Security-Policy: '+b'x'*5000+b'\r\n',False),('over-budget','download',bytes(data),b'Content-Security-Policy: '+b'x'*8200+b'\r\n',False),('aggregate-over-budget','download',bytes(data),(b'Content-Security-Policy: '+b'x'*4065+b'\r\n')*2,False),('malformed-count','download',bytes(data),b'ignored\r\n'*65,False),('cancel-during-csp','download-abort',bytes(data),b'Content-Security-Policy: '+b'x'*5000+b'\r\n',True),('token-refresh','auth',b'{"access_token":"fixture-issued"}',b'Content-Security-Policy: '+b'x'*5000+b'\r\n',False)]
    out=[]
    for name,mode,body,headers,pause in cases:
        with LoopbackTLS(cert,secret,payload=body,extra_headers=headers,pause_header=pause) as server:
            proc=subprocess.run([str(exe),mode,'good.test',str(server.port),str(capath),str(frame),'fresh'],capture_output=True,text=True,timeout=15)
        if proc.returncode: raise RuntimeError((name,proc.returncode,proc.stderr))
        got=json.loads(proc.stdout)
        expected={'valid-large-csp':(200,True,False,False),'over-budget':(-1,False,True,False),'aggregate-over-budget':(-1,False,True,False),'malformed-count':(-1,False,True,False),'cancel-during-csp':(-1,False,True,False),'token-refresh':(200,False,True,True)}[name]
        actual=(got['status'],got['committed'],got['old_preserved'],got['minted'])
        if actual != expected or not got['part_removed']: raise AssertionError((name,got,expected))
        out.append({'case':name,'result':'PASS','observed':got})
        print(json.dumps(out[-1]),flush=True)
print(json.dumps({'status':'PASS','cases':out,'boundary':'actual CP PluginHttp, SDK parser and wolfSSL; synthetic TLS, SD and clock; no device'},indent=2))
