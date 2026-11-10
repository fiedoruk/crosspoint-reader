#!/usr/bin/env python3
"""Run the TIMED busy-header host test against an assembled CP/SDK tree."""
import argparse
from pathlib import Path
import subprocess
import tempfile
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--cp', type=Path, required=True)
p.add_argument('--arduinojson', type=Path, required=True)
p.add_argument('--negative-control', action='store_true')
a = p.parse_args()
root, here = a.cp.resolve(), Path(__file__).resolve().parent
sdk = root / 'freeink-sdk/libs/network/SecureNet'
includes = [here/'stubs', sdk/'include', root/'test/timed_sync/stubs', root/'test/plugin_verified_http/stubs', root/'test/plugin_event_budget/stubs', a.arduinojson, root/'src', root/'lib/GfxRenderer', root/'lib/Memory']
sources = [root/'src/util/PluginHttp.cpp', root/'src/util/PluginEvents.cpp', root/'src/util/PluginEventAsset.cpp', root/'src/util/TimedSleepPaint.cpp', root/'lib/GfxRenderer/Bitmap.cpp', root/'lib/GfxRenderer/BitmapHelpers.cpp', here/'BusyHeadersTest.cpp']
with tempfile.TemporaryDirectory(prefix='timed-busy-') as d:
    exe = Path(d)/'test'
    cmd = ['nice','-n','10','c++','-std=c++20','-O0','-fsanitize=address,undefined','-fno-omit-frame-pointer']
    if a.negative_control:
        # Test-only shadow header in a temporary directory: remove the inner
        # busy-loop abort poll. Never change or package the production file.
        header = (sdk/'include/SecureHttpClient.h').read_text()
        original = 'if (static_cast<int32_t>(millis() - deadline) >= 0 || isAborted(shouldAbort)) return false;'
        replacement = 'if (static_cast<int32_t>(millis() - deadline) >= 0) return false;'
        assert header.count(original) == 1
        (Path(d)/'SecureHttpClient.h').write_text(header.replace(original, replacement))
        cmd += ['-I',d]
    for include in includes: cmd += ['-I',str(include)]
    subprocess.run(cmd + [str(x) for x in sources] + ['-o',str(exe)],check=True)
    if a.negative_control:
        for case in ('abort', 'budget'):
            result = subprocess.run([str(exe),case],capture_output=True,text=True,timeout=15)
            assert result.returncode != 0 and 'triggerAt == trigger' in result.stderr, (case,result.returncode,result.stderr)
            progress = next(line for line in result.stderr.splitlines() if line.startswith('progress:'))
            print(f'{case}: mutation detected by progress oracle (exit {result.returncode}); {progress}')
    else:
        subprocess.run([str(exe)],check=True,timeout=15)
