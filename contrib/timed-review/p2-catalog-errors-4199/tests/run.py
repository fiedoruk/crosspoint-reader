#!/usr/bin/env python3
import pathlib, subprocess, sys, tempfile
root = pathlib.Path(__file__).resolve().parents[1]
src = root / 'source'
if len(sys.argv) != 2:
    raise SystemExit('usage: python3 tests/run.py /path/to/ArduinoJson-7.4.2/src')
json_include = pathlib.Path(sys.argv[1])
def func(path, start):
    s=(src/path).read_text(); pos=s.index(start); brace=s.index('{',pos); depth=0
    for i in range(brace,len(s)):
        if s[i]=='{': depth+=1
        elif s[i]=='}':
            depth-=1
            if depth==0: return s[pos:i+1]
    raise ValueError(start)
parts=[func('src/activities/plugins/PluginCatalogActivity.cpp',x) for x in ['std::string httpStatusDetail(', 'std::string httpFailureDetail(']]
parts += [func('src/activities/CatalogActivity.cpp',x) for x in ['void CatalogActivity::fail(', 'void CatalogActivity::finishDownload(', 'bool CatalogActivity::buildStatusScreen(']]
with tempfile.TemporaryDirectory() as d:
    p=pathlib.Path(d); (p/'actual.inc').write_text('\n\n'.join(parts)+'\n')
    for flag in ('-fsigned-char','-funsigned-char'):
        exe=p/('test'+flag)
        cmd=['c++','-std=c++17','-O0','-Wall','-Wextra','-Werror',flag,'-I'+str(json_include),'-I'+str(p),str(root/'tests/harness.cpp'),'-o',str(exe)]
        subprocess.run(cmd,check=True); print('COMPILED',flag,flush=True)
        subprocess.run([str(exe)],check=True)
