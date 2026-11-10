from pathlib import Path
import os, subprocess, tempfile
root = Path(__file__).resolve().parents[2]
here = Path(__file__).resolve().parent
stock = os.environ.get('CROSSPOINT_STOCK_MAIN')
src = Path(stock).read_text() if stock else (root / 'src/main.cpp').read_text()
with tempfile.TemporaryDirectory(prefix='wifi-fallback-') as t:
    t = Path(t)
    sleep = src[src.index('static void deliverSleepPluginEvents('):src.index('\n#if FREEINK_DEVICE_PICCO', src.index('static void deliverSleepPluginEvents('))]
    timer = '' if stock else src[src.index('static uint64_t prepareTimerPanel() {', src.index('static bool timerStorageReady')):src.index('static void returnToTimerStandby() {')]
    (t/'Callers.inc').write_text(sleep+'\n'+timer)
    inc = os.environ['CROSSPOINT_ARDUINOJSON_INCLUDE']
    subprocess.run(['c++','-std=c++20','-O0','-Wall','-Wextra',*(['-DSTOCK_ONLY'] if stock else []),'-fsanitize=address,undefined','-fno-omit-frame-pointer', '-I',str(t),'-I',str(here/'stubs'),'-I',inc,'-I',str(root/'src'),'-I',str(root/'lib/Serialization'), str(root/'src/WifiCredentialStore.cpp'),str(here/'WifiFallbackTest.cpp'),'-o',str(t/'test')],check=True)
    subprocess.run([str(t/'test')],check=True)
