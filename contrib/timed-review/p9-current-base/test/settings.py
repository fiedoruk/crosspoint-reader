"""Extend the existing timer visitor harness with the real new extensions descriptor."""
from pathlib import Path
import argparse,re,subprocess,tempfile,shutil
p=argparse.ArgumentParser();p.add_argument('--cp',type=Path,required=True);p.add_argument('--arduinojson',type=Path,required=True);a=p.parse_args();root=a.cp.resolve();original=root/'test/timer_plugin_permission'
with tempfile.TemporaryDirectory(prefix='p9-settings-') as temp:
 here=Path(temp);shutil.copytree(original,here/'test');here=here/'test'
 run=(here/'run.py').read_text().replace('root=Path(__file__).resolve().parents[2]',f'root=Path({str(root)!r})')
 # Preserve the original timer registry and append the exact unrelated toggle.
 run=run.replace('assert registry\n','assert registry\nextra=re.search(r\'  emit\\(SettingInfo::Toggle\\(StrId::STR_SHOW_FILE_EXTENSIONS,.*?;\',base_settings,re.S)\nassert extra\n')
 run=run.replace('setting_types+registry.group()', 'setting_types+registry.group()+extra.group()')
 run=run.replace('registry.group()+"\\n}\\n"','registry.group()+"\\n"+extra.group()+"\\n}\\n"')
 (here/'run.py').write_text(run)
 stub=here/'stubs/CrossPointSettings.h';s=stub.read_text();s=s.replace('struct CrossPointSettings {', 'struct CrossPointSettings {\n  uint8_t showFileExtensions = 1;',1);assert 'showFileExtensions' in s;stub.write_text(s)
 permission=here/'PermissionTest.cpp';value=permission.read_text().replace('  int loads = 0;', '  int loads = 0;\n  std::optional<Cred> getCredentialAt(size_t) { assert(false); return std::nullopt; }');permission.write_text(value)
 f=here/'VisitorTest.cpp';s=f.read_text();s=s.replace('result.push_back(std::move(info));','if (std::string(info.key) != "showFileExtensions") result.push_back(std::move(info));')
 s=s.replace('    ++visits;', '    if (std::string(info.key) == "showFileExtensions") return;\n    ++visits;')
 s=s.replace('int main() {','''int main() {
  for (bool enabled : {false, true}) {
    SETTINGS.showFileExtensions = enabled;
    JsonDocument value; SETTINGS.toJson(value);
    assert(value["showFileExtensions"].as<bool>() == enabled);
    SETTINGS.showFileExtensions = !enabled;
    SETTINGS.fromJson(value.as<JsonObject>());
    assert(bool(SETTINGS.showFileExtensions) == enabled);
  }
''',1);f.write_text(s)
 subprocess.run(['python3',str(here/'run.py'),'--arduinojson',str(a.arduinojson.resolve())],check=True)
print('PASS real timer visitor callbacks with showFileExtensions round-trip; unrelated settings/UI omitted')
