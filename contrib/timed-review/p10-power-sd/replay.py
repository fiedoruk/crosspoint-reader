#!/usr/bin/env python3
"""Reconstruct pinned W06 or TIMED support; no build, hardware or publication."""
import argparse, hashlib, json, subprocess
from pathlib import Path
here=Path(__file__).resolve().parent
m=json.loads((here/'manifest.json').read_text())
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('destination',type=Path)
p.add_argument('--through',choices=['w06','timed'],required=True)
p.add_argument('--cp-source',default='https://github.com/crosspoint-reader/crosspoint-reader.git')
p.add_argument('--sdk-source',default='https://github.com/Free-Ink/freeink-sdk.git')
a=p.parse_args();dest=a.destination.resolve()
if dest.exists():p.error('destination must not exist')
for name,digest in m['files'].items():
 if hashlib.sha256((here/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Packet checksum mismatch: '+name)
def git(path,*args):return subprocess.check_output(['git',*args],cwd=path,text=True).strip()
for path,source,ref,patches,tree in [
 (dest,a.cp_source,m['cp'],m['cpPatches'][:m['cpPatches'].index(m['w06LastPatch'])+1] if a.through=='w06' else m['cpPatches'],m['cpTrees'][a.through]),
 (dest/'freeink-sdk',a.sdk_source,m['sdk'],m['sdkPatches'],m['sdkTree'])]:
 path.mkdir(parents=True,exist_ok=True);git(path,'init','--quiet')
 git(path,'fetch','--quiet','--depth=1',source,ref);git(path,'checkout','--quiet','--detach','FETCH_HEAD')
 if git(path,'rev-parse','HEAD')!=ref:raise SystemExit('Unexpected base')
 for patch in patches:git(path,'apply','--index',str(here/'patches'/patch))
 if git(path,'write-tree')!=tree:raise SystemExit('Unexpected result tree: '+str(path))
if git(dest,'ls-tree',m['cpTrees'][a.through],'freeink-sdk').split()[2]!=m['cpGitlinkUnchanged']:raise SystemExit('CP SDK pin differs')
print(json.dumps({'status':'SOURCE_REPLAY_PASS','through':a.through,'cpTree':m['cpTrees'][a.through],'sdkTree':m['sdkTree'],'build':'NOT_RUN','device':'NOT_MEASURED'}))
