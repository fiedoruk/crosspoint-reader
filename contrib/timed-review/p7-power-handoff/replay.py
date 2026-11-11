#!/usr/bin/env python3
"""Reconstruct the pinned P7 integration. Does not build, flash or publish."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('destination', type=Path)
parser.add_argument('--cp-source', default='https://github.com/crosspoint-reader/crosspoint-reader.git')
parser.add_argument('--sdk-source', default='https://github.com/Free-Ink/freeink-sdk.git')
args = parser.parse_args()
manifest = json.loads((here / 'manifest.json').read_text())
destination = args.destination.resolve()
if destination.exists():
    parser.error('destination must not exist')
for name, expected in manifest['files'].items():
    if hashlib.sha256((here / name).read_bytes()).hexdigest() != expected:
        raise SystemExit('Packet checksum mismatch: ' + name)

def git(path, *arguments):
    return subprocess.check_output(['git', *arguments], cwd=path, text=True).strip()

for path, source, ref, patches, expected in (
    (destination, args.cp_source, manifest['cp'], manifest['cpPatches'], manifest['cpTree']),
    (destination / 'freeink-sdk', args.sdk_source, manifest['sdk'], manifest['sdkPatches'], manifest['sdkTree']),
):
    path.mkdir(parents=True, exist_ok=True)
    git(path, 'init', '--quiet')
    git(path, 'fetch', '--quiet', '--depth=1', source, ref)
    git(path, 'checkout', '--quiet', '--detach', 'FETCH_HEAD')
    if git(path, 'rev-parse', 'HEAD') != ref:
        raise SystemExit('Unexpected source ref')
    for patch in patches:
        git(path, 'apply', '--index', str(here / 'patches' / patch))
    if git(path, 'write-tree') != expected:
        raise SystemExit('Unexpected result tree: ' + str(path))
print('P7 source replay PASS; build and hardware not run')
