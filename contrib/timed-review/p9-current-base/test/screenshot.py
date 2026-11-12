"""Round-trip production drawPixel through screenshot BMP in four orientations."""
from pathlib import Path
import argparse, subprocess, tempfile
p=argparse.ArgumentParser();p.add_argument('--cp',type=Path,required=True);a=p.parse_args();r=a.cp

def method(text, signature):
 start=text.index(signature);brace=text.index('{',start);depth=1;i=brace+1
 while depth:
  depth+=(text[i]=='{')-(text[i]=='}');i+=1
 return text[start:i]
gfx=(r/'lib/GfxRenderer/GfxRenderer.cpp').read_text();bmp=(r/'lib/GfxRenderer/Bitmap.h').read_text()
parts=[bmp[bmp.index('#pragma pack(push'):bmp.index('#pragma pack(pop)')+len('#pragma pack(pop)')], 'enum class BmpRowOrder { BottomUp, TopDown };',method((r/'lib/GfxRenderer/BitmapHelpers.cpp').read_text(),'void createBmpHeader('),method(gfx,'static inline void rotateCoordinates('),method(gfx,'void GfxRenderer::drawPixel('),method((r/'src/util/ScreenshotUtil.cpp').read_text(),'bool ScreenshotUtil::saveFramebufferAsBmp(')]
source=Path(__file__).with_suffix('.cpp').read_text().replace('PRODUCTION_METHODS','\n'.join(parts))
with tempfile.TemporaryDirectory(prefix='p9-screenshot-') as d:
 cpp=Path(d)/'test.cpp';cpp.write_text(source);exe=Path(d)/'test'
 subprocess.run(['c++','-std=c++20','-fsanitize=address,undefined','-fno-omit-frame-pointer',str(cpp),'-o',str(exe)],check=True);subprocess.run([str(exe)],check=True)
print('PASS production drawPixel/screenshot BMP: four orientations, padded stride; no display hardware')
