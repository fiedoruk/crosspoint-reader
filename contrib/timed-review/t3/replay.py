#!/usr/bin/env python3
"""Apply the pinned review series in a new directory; no build, flash or push."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('destination',type=Path)
p.add_argument('--cp-source',default='https://github.com/fiedoruk/crosspoint-reader.git')
p.add_argument('--sdk-source',default='https://github.com/Free-Ink/freeink-sdk.git')
p.add_argument('--through',choices=['w06','timed'],default='timed')
a=p.parse_args();packet=Path(__file__).resolve().parent;m=json.loads((packet/'manifest.json').read_text());dest=a.destination.resolve()
if dest.exists():p.error('destination must not exist')
for name,digest in m['patches'].items():
 if hashlib.sha256((packet/'patches'/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Patch checksum mismatch: '+name)
def git(cwd,*args):return subprocess.check_output(['git',*args],cwd=cwd,text=True).strip()
def clone(source,path,ref):
 subprocess.run(['git','clone','--no-checkout',source,str(path)],check=True)
 if subprocess.run(['git','cat-file','-e',ref+'^{commit}'],cwd=path,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
  git(path,'fetch','origin',ref)
 git(path,'checkout','--detach',ref)
clone(a.cp_source,dest,m['cpBase']);sdk=dest/'freeink-sdk'
if sdk.exists():sdk.rmdir()  # Gitlink placeholder must be empty.
clone(a.sdk_source,sdk,m['sdkBase']);git(sdk,'apply','--index',str(packet/'patches/sdk-verified.patch'))
steps=['01-checked-bmp.patch','02-bounded-events.patch','03-verified-events.patch']
if a.through=='timed':steps.append('04-timed-source.patch')
for name in steps:git(dest,'apply','--index',str(packet/'patches'/name))
actual=git(dest,'write-tree');assert actual==m['trees'][a.through],(actual,m['trees'][a.through])
print(json.dumps({'status':'APPLIED_VERIFIED','through':a.through,'cpBase':m['cpBase'],'sdkBase':m['sdkBase'],'tree':actual,'sdkTree':git(sdk,'write-tree'),'build':'NOT_RUN','device':'NOT_MEASURED'},indent=2))
