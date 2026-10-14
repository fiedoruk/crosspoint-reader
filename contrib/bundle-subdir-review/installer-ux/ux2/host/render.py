"""Run extracted production methods with explicit host-only boundaries."""
from pathlib import Path
import argparse, subprocess, time, json, hashlib
p = argparse.ArgumentParser()
p.add_argument('cp', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
cp = a.cp.resolve()
out = a.output.resolve()
out.mkdir()
here = Path(__file__).resolve().parent
s = (cp / 'src/activities/reader/DictionaryDefinitionActivity.cpp').read_text()
parts = []
for start, end in [('DictionaryDefinitionActivity::BodyArea DictionaryDefinitionActivity::bodyArea() const {', '\n// Styled path:'), ('int DictionaryDefinitionActivity::measureSpan(', '\nvoid DictionaryDefinitionActivity::loop()'), ('void DictionaryDefinitionActivity::drawBody(', '\nvoid DictionaryDefinitionActivity::render(')]:
    i = s.index(start)
    j = s.index(end, i)
    parts.append(s[i:j])
(out / 'LayoutMethods.inc').write_text('\n'.join(parts))
ui = cp / 'freeink-sdk/libs/ui/FreeInkUI'
cmd = ['c++', '-std=c++20', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-I' + str(out), '-I' + str(cp / 'lib/EpdFont'), '-I' + str(cp / 'lib/Utf8'), '-I' + str(ui / 'include'), str(here / 'LayoutProbe.cpp'), str(cp / 'lib/EpdFont/EpdFont.cpp'), str(cp / 'lib/Utf8/Utf8.cpp'), str(ui / 'src/FreeInkUI.cpp'), '-o', str(out / 'render')]
start = time.monotonic()
subprocess.run(cmd, check=True)
subprocess.run([str(out / 'render'), str(out)], check=True)
(out / 'receipt.json').write_text(json.dumps({'result': 'HOST_LAYOUT_PASS', 'cases': 16, 'adversarialSpanCases': 3, 'seconds': round(time.monotonic() - start, 3), 'sourceSha256': hashlib.sha256(s.encode()).hexdigest(), 'actualProduction': 'bodyArea, measureSpan, wrapText, drawBody; native FreeInkUI button', 'mocks': 'CP GfxRenderer adapter/metrics/header; Ubuntu12 layout and NotoSerif18 span stress; no Arabic/Bidi or SD fonts claim', 'device': 'NOT_MEASURED'}, indent=2) + '\n')
