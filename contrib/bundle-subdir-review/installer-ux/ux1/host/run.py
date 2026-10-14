"""Run extracted production methods with explicit host-only boundaries."""
from pathlib import Path
import argparse, subprocess, json, time, hashlib
p = argparse.ArgumentParser()
p.add_argument('cp', type=Path)
p.add_argument('gtest', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
cp = a.cp.resolve()
g = a.gtest.resolve() / 'googletest'
out = a.output.resolve()
out.mkdir()
here = Path(__file__).resolve().parent
cpp = (cp / 'src/activities/plugins/PluginCatalogActivity.cpp').read_text()
hdr = (cp / 'src/activities/plugins/PluginCatalogActivity.h').read_text()
start = hdr.index('struct PluginRef {')
end = hdr.index('\n};', start) + 3
(out / 'PluginRef.inc').write_text(hdr[start:end])
start = cpp.index('std::vector<PluginRef> discoverPlugins() {')
end = cpp.index('\nbool anyPluginInstalled()', start)
(out / 'DiscoverPlugins.inc').write_text(cpp[start:end])
start = cpp.index('  const auto previous =', cpp.index('void PluginCatalogActivity::enterPluginPicker()'))
end = cpp.index('  requestUpdate();', start)
(out / 'RestoreSelection.inc').write_text(cpp[start:end])
start = time.monotonic()
cmd = ['c++', '-std=c++20', '-g', '-pthread', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-I' + str(cp / 'src'), '-I' + str(out), '-I' + str(g / 'include'), '-I' + str(g), str(here / 'PickerOrderTest.cpp'), str(g / 'src/gtest-all.cc'), str(g / 'src/gtest_main.cc'), '-o', str(out / 'test')]
subprocess.run(cmd, check=True)
subprocess.run([str(out / 'test'), '--gtest_output=json:' + str(out / 'tests.json')], check=True)
d = json.loads((out / 'tests.json').read_text())
assert d['failures'] == 0
receipt = {'result': 'PASS', 'tests': d['tests'], 'seconds': round(time.monotonic() - start, 3), 'sanitizers': ['address', 'undefined'], 'extractedProductionFunctions': ['discoverPlugins', 'selection restore block'], 'boundaryMocks': ['SD discovery results', 'metadata parser', 'moveSelectionTo'], 'sourceSha256': hashlib.sha256(cpp.encode()).hexdigest(), 'device': 'NOT_MEASURED'}
(out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
