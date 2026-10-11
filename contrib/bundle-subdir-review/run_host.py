#!/usr/bin/env python3
"""Test the actual bundle method and discovery code with host storage stubs."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import time

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("cp", type=Path)
parser.add_argument("googletest", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("--expect-old-failure", action="store_true")
args = parser.parse_args()
cp, gtest, out = args.cp.resolve(), args.googletest.resolve() / "googletest", args.output.resolve()
out.mkdir()
source = (cp / "src/activities/plugins/PluginCatalogActivity.cpp").read_text()
start = source.index("HttpDownloader::DownloadError PluginCatalogActivity::downloadBundle(const Item& item) {")
end = source.index("\nHttpDownloader::DownloadError PluginCatalogActivity::downloadBook", start)
(out / "DownloadBundleBody.inc").write_text(source[start:end] + "\n")
binary = out / "bundle-flow-test"
command = shlex.split(os.environ.get("CXX", "c++")) + [
    "-std=c++20", "-g", "-pthread", "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
    "-I" + str(HERE / "host/stubs"), "-I" + str(out), "-I" + str(cp / "src"),
    "-I" + str(gtest / "include"), "-I" + str(gtest),
    str(HERE / "host/PluginBundleFlowTest.cpp"), str(cp / "src/util/PluginLocations.cpp"),
    str(gtest / "src/gtest-all.cc"), str(gtest / "src/gtest_main.cc"), "-o", str(binary),
]
started = time.monotonic()
subprocess.run(command, check=True)
result = subprocess.run([str(binary), "--gtest_output=json:" + str(out / "tests.json")])
report = json.loads((out / "tests.json").read_text())
failed = [test["name"] for suite in report["testsuites"] for test in suite["testsuite"] if test.get("failures")]
if args.expect_old_failure:
    if result.returncode != 1 or failed != ["InvalidSubdirectoriesDoNotWrite"]:
        raise SystemExit("Unexpected negative-control result")
elif result.returncode or failed:
    raise SystemExit("Patched bundle tests failed")
receipt = {"result": "PASS", "negativeControl": args.expect_old_failure,
           "tests": report["tests"], "failedTests": failed,
           "wallSeconds": round(time.monotonic() - started, 3),
           "sanitizers": ["address", "undefined"], "device": "NOT_MEASURED"}
(out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
