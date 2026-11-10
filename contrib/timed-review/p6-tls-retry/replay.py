#!/usr/bin/env python3
"""Apply P6 to the immutable P4 future lane; no build or publication."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--p4-packet',type=Path,required=True)
p.add_argument('destination',type=Path)
p.add_argument('--cp-source');p.add_argument('--sdk-source')
a=p.parse_args(); here=Path(__file__).resolve().parent
m=json.loads((here/'manifest.json').read_text())
for name,digest in m['files'].items():
 if hashlib.sha256((here/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Packet checksum mismatch: '+name)
if hashlib.sha256((a.p4_packet/'manifest.json').read_bytes()).hexdigest()!=m['p4ManifestSha256']:raise SystemExit('P4 manifest mismatch')
cmd=['python3',str((a.p4_packet/'replay.py').resolve()),str(a.destination.resolve()),'--lane','future-qualification']
for flag,value in [('--cp-source',a.cp_source),('--sdk-source',a.sdk_source)]:
 if value:cmd.extend([flag,value])
subprocess.run(cmd,check=True)
sdk=a.destination.resolve()/'freeink-sdk'
subprocess.run(['git','apply','--check',str(here/'retry.patch')],cwd=sdk,check=True)
subprocess.run(['git','apply',str(here/'retry.patch')],cwd=sdk,check=True)
for name,digest in m['candidate'].items():
 if hashlib.sha256((sdk/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Candidate mismatch: '+name)
print('P6 source replay PASS; tests/build/device not run')
