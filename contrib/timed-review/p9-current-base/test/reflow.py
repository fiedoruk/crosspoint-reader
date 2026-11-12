"""Exercise production progress read, cache validation and resume mapping at host boundaries."""
from pathlib import Path
import argparse
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cp', type=Path, required=True)
parser.add_argument('--negative-control', action='store_true')
args = parser.parse_args()
root = args.cp
section = (root / 'lib/Epub/Epub/Section.cpp').read_text()
reader = (root / 'src/activities/reader/EpubReaderActivity.cpp').read_text()


def block(text, signature):
    start = text.index(signature)
    brace = text.index('{', start)
    depth, end = 1, brace + 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[start:end]


constants = section[section.index('constexpr uint8_t SECTION_FILE_VERSION'):section.index('}  // namespace')]
methods = '\n'.join(block(section, signature) for signature in (
    'void Section::writeSectionFileHeader(',
    'bool Section::loadSectionFile(',
    'std::optional<uint16_t> Section::getPageForVisibleTextOffset(',
))
methods += '\n' + block(reader, 'bool EpubReaderActivity::applyDeferredReposition(')
methods += '\n' + block(reader, 'void EpubReaderActivity::clearDeferredReposition(')
progress = block(reader, 'if (Storage.openFileForRead("ERS", epub->getCachePath() + "/progress.bin", f))')
methods += '\nvoid EpubReaderActivity::loadProgress() { HalFile f;\n' + progress + '\n}\n'
start = reader.index('    const bool explicitOffsetJump = pendingOffsetJump.has_value();')
selection = reader[start:reader.index('    if (!cacheComplete)', start)]
start = reader.index('    if (pendingPageJump.has_value()) {', start)
end = reader.index('    pendingOffsetJump.reset();', start) + len('    pendingOffsetJump.reset();')
normal_resume = selection + reader[start:end]
if args.negative_control:
    assert normal_resume.count('section->currentPage = *offsetPage;') == 1
    normal_resume = normal_resume.replace('section->currentPage = *offsetPage;',
                                          'section->currentPage = nextPageNumber;', 1)
methods += '\nvoid EpubReaderActivity::resumeLoadedSection() {\n' + normal_resume + '\n}\n'
start = reader.index('  if (automaticPageTurnActive &&', reader.index('void EpubReaderActivity::renderBook()'))
margin = reader[start:reader.index('  const uint16_t viewportWidth', start)]
methods += '\nint bottomMargin(bool automaticPageTurnActive, int statusBarHeight) { int orientedMarginBottom=0;\n'
methods += margin + '\nreturn orientedMarginBottom; }\n'
source = Path(__file__).with_suffix('.cpp').read_text()
source = source.replace('PRODUCTION_CONSTANTS', constants).replace('PRODUCTION_METHODS', methods)
with tempfile.TemporaryDirectory(prefix='p9-reflow-') as directory:
    cpp = Path(directory) / 'test.cpp'
    cpp.write_text(source)
    executable = Path(directory) / 'test'
    subprocess.run(['c++', '-std=c++20', '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
                    '-I', str(root / 'lib/Epub/Epub'), str(cpp), '-o', str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
print('PASS production progress read, cache validation, viewport margin and normal/deferred resume mapping; rebuilt LUT is synthetic')
