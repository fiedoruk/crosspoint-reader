#!/usr/bin/env python3
"""Replay a dependent W06/TIMED integration; no build or external write."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

packet = Path(__file__).resolve().parent
m = json.loads((packet / 'manifest.json').read_text())
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('destination', type=Path)
p.add_argument('--lane', choices=m['lanes'], required=True)
p.add_argument('--through', choices=['w04', 'prerequisites', 'w06', 'timed', 'p1'], default='p1')
p.add_argument('--cp-source', default=m['cpSource'])
p.add_argument('--sdk-source', default=m['sdkSource'])
a = p.parse_args()
dest = a.destination.resolve()
if dest.exists():
    p.error('destination must not exist')
for name, expected in m['patches'].items():
    if hashlib.sha256((packet / 'patches' / name).read_bytes()).hexdigest() != expected:
        raise SystemExit('Patch checksum mismatch: ' + name)

def git(path, *args):
    return subprocess.check_output(['git', *args], cwd=path, text=True).strip()

def checkout(path, source, commit):
    path.mkdir(parents=True)
    git(path, 'init', '--quiet')
    git(path, 'remote', 'add', 'origin', source)
    git(path, 'fetch', '--quiet', '--depth', '1', 'origin', commit)
    git(path, 'checkout', '--quiet', '--detach', commit)

checkout(dest, a.cp_source, m['cpBase'])
if git(dest, 'rev-parse', 'HEAD^{tree}') != m['cpBaseTree']:
    raise SystemExit('Unexpected CP base tree')
if git(dest, 'ls-tree', 'HEAD', 'freeink-sdk').split()[2] != m['cpSdkGitlink']:
    raise SystemExit('Unexpected CP SDK gitlink')
sdk = dest / 'freeink-sdk'
if sdk.exists():
    sdk.rmdir()
lane = m['lanes'][a.lane]
checkout(sdk, a.sdk_source, lane['sdkBase'])
git(sdk, 'apply', '--index', str(packet / 'patches' / lane['patch']))
if git(sdk, 'write-tree') != lane['tree']:
    raise SystemExit('Unexpected SDK result tree')
end = {'w04': 0, 'prerequisites': 1, 'w06': 2, 'timed': 4, 'p1': 7}[a.through]
for step in m['steps'][:end + 1]:
    git(dest, 'apply', '--index', str(packet / 'patches' / step['patch']))
    tree = git(dest, 'write-tree')
    if tree != step['tree']:
        raise SystemExit('Unexpected CP result tree: ' + step['patch'])
print(json.dumps({'status': 'APPLIED_VERIFIED', 'lane': a.lane, 'through': a.through,
                  'cpTree': tree, 'cpSdkGitlink': m['cpSdkGitlink'],
                  'actualSdkHead': git(sdk, 'rev-parse', 'HEAD'), 'sdkTree': lane['tree'],
                  'submoduleDirtyExpected': True, 'build': 'NOT_RUN', 'device': 'NOT_MEASURED'}, indent=2))
