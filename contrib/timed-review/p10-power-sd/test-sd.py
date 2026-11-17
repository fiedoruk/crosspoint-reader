"""Test the production SD wrapper and ordinary sleep decision with a failing card."""
import argparse
import subprocess
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cp', required=True, type=Path)
root = parser.parse_args().cp
hal = (root / 'lib/hal/HalStorage.cpp').read_text()
main = (root / 'src/main.cpp').read_text()
start = hal.index('bool HalStorage::prepareForDeepSleep()')
wrapper = hal[start:hal.index('\n}', start) + 2]
start = main.index('  if (!Storage.prepareForDeepSleep())', main.index('void enterDeepSleep('))
caller = main[start:main.index('\n}', start)]
harness = r'''
#include <cassert>
#include <string>
#include <vector>
#define LOG_ERR(...) ((void)0)
#define LOG_DBG(...) ((void)0)
std::vector<int> trace;
int failures;
struct {bool shutdown(){trace.push_back(1);return failures-- <= 0;}} SDCard;
void delay(int n){assert(n==20);}
struct HalStorage{struct StorageLock{};bool prepareForDeepSleep();} Storage;
struct {void consumePowerGesture(){trace.push_back(2);}} mappedInputManager;
struct {bool lastSleepFromReader=true;std::string openEpubPath="/book.epub";} APP_STATE;
struct {void goToReader(const std::string& s){assert(s=="/book.epub");trace.push_back(3);}
void goHome(){trace.push_back(4);}} activityManager;
bool deepSleepInProgress;
struct {void deepSleep(){trace.push_back(5);}} halTiltSensor,display;
struct {void startDeepSleep(int,bool,int){trace.push_back(6);}} powerManager;
int gpio=0,timerInterval=60;
WRAPPER
void sleepTail(){
CALLER
}
int main(){
 for(int fail:{0,1,2}){
  trace.clear();failures=fail;deepSleepInProgress=true;sleepTail();
  if(fail==2){assert((trace==std::vector<int>{1,1,2,3}));assert(!deepSleepInProgress);}
  else if(fail==1)assert((trace==std::vector<int>{1,1,5,5,6}));
  else assert((trace==std::vector<int>{1,5,5,6}));
 }
}
'''
with tempfile.TemporaryDirectory() as temp:
    source = Path(temp) / 'test.cpp'
    binary = Path(temp) / 'test'
    source.write_text(harness.replace('WRAPPER', wrapper).replace('CALLER', caller))
    subprocess.run(['c++','-std=c++20','-fsanitize=address,undefined',str(source),'-o',str(binary)],check=True)
    subprocess.run([str(binary)],check=True)
print('PASS ordinary sleep: first success, transient failure and permanent failure returning to reader')
