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
parts = [('src/activities/reader/DictionaryDefinitionActivity.cpp', 'void DictionaryDefinitionActivity::onEnter() {', '\nvoid DictionaryDefinitionActivity::onExit()', 'ViewerEnter.inc'), ('src/activities/reader/DictionaryDefinitionActivity.cpp', 'void DictionaryDefinitionActivity::loop() {', '\n// Draws the current page:', 'ViewerLoop.inc'), ('src/activities/plugins/PluginCatalogActivity.cpp', 'void PluginCatalogActivity::activateItem(const int itemIndex) {', '\nvoid PluginCatalogActivity::drawFooter()', 'ActivateItem.inc')]
hashes = {}
for path, start, end, name in parts:
    text = (cp / path).read_text()
    i = text.index(start)
    j = text.index(end, i)
    (out / name).write_text(text[i:j])
    hashes[path] = hashlib.sha256(text.encode()).hexdigest()
start = time.monotonic()
command = ['c++', '-std=c++20', '-g', '-pthread', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-I' + str(out), '-I' + str(g / 'include'), '-I' + str(g), str(here / 'FlowTest.cpp'), str(g / 'src/gtest-all.cc'), str(g / 'src/gtest_main.cc'), '-o', str(out / 'test')]
subprocess.run(command, check=True)
subprocess.run([str(out / 'test'), '--gtest_output=json:' + str(out / 'tests.json')], check=True)
d = json.loads((out / 'tests.json').read_text())
assert d['failures'] == 0
receipt = {'result': 'PASS', 'tests': d['tests'], 'seconds': round(time.monotonic() - start, 3), 'sanitizers': ['address', 'undefined'], 'actualProduction': ['viewer onEnter', 'viewer loop', 'catalog activateItem'], 'mocks': ['input snapshots', 'UiAppHost routing gate', 'download boundary', 'activity callbacks and allocation failure'], 'sourceSha256': hashes, 'device': 'NOT_MEASURED'}
(out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
