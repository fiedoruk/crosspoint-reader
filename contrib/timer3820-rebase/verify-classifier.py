#!/usr/bin/env python3
"""Compare the actual new classifier with the pinned pre-change HAL policy."""
from pathlib import Path
import argparse
import subprocess
import tempfile

BASE = "6d2cd3a1c16cb9bdff5a52f6ec657d24f401b0a8"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("repo", type=Path)
args = parser.parse_args()
repo = args.repo.resolve()
source = subprocess.check_output(
    ["git", "show", BASE + ":lib/hal/HalGPIO.cpp"], cwd=repo, text=True
)
signature = "HalGPIO::WakeupReason HalGPIO::getWakeupReason() const {"
body = source.split(signature, 1)[1].split("\n}", 1)[0]
body = body[body.index("  if (resetReason"):]
body = body.replace("coldBootImpliesPowerButton()", "coldBoot")
body = body.replace("WakeupReason::", "wakeup::Reason::")
body = body.replace("ESP_SLEEP_WAKEUP_", "wakeup::WAKEUP_")
body = body.replace("ESP_RST_", "wakeup::RST_")
program = '''#include "WakeupClassify.h"
#include <iostream>
wakeup::Reason before(int wakeupCause, int resetReason, bool usbConnected, bool coldBoot) {
''' + body + '''
}
int main() {
  int checked = 0;
  int changed = 0;
  for (int cause = 0; cause < 16; ++cause) {
    for (int reset = 0; reset < 16; ++reset) {
      for (bool usb : {false, true}) {
        for (bool cold : {false, true}) {
          const auto old = before(cause, reset, usb, cold);
          const auto actual = wakeup::classify(cause, reset, usb, cold);
          const bool timer = cause == wakeup::WAKEUP_TIMER && reset == wakeup::RST_DEEPSLEEP;
          const auto expected = timer ? wakeup::Reason::Timer : old;
          if (actual != expected) {
            std::cerr << "Unexpected change: " << cause << ',' << reset << ',' << usb << ',' << cold << '\\n';
            return 1;
          }
          changed += actual != old;
          ++checked;
        }
      }
    }
  }
  if (checked != 1024 || changed != 4) return 2;
  std::cout << checked << " combinations passed; " << changed << " timer classifications changed\\n";
}
'''
with tempfile.TemporaryDirectory(prefix="timer-classifier-") as temp:
    directory = Path(temp)
    cpp = directory / "compare.cpp"
    executable = directory / "compare"
    cpp.write_text(program)
    subprocess.run(
        ["c++", "-std=c++20", "-Wall", "-Wextra", "-Werror", "-fsanitize=address,undefined",
         "-I", str(repo / "lib/hal"), str(cpp), "-o", str(executable)], check=True
    )
    subprocess.run([str(executable)], check=True)
