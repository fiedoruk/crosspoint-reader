#!/usr/bin/env python3
"""Reconstruct the PR #3877 regression and its minimal fix from public refs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
destination = args.destination.resolve()
destination.mkdir()  # Refuse existing paths; never reset someone else's checkout.
lock = json.loads((HERE / "source-lock.json").read_text())
patch = HERE / "subdir-guards.patch"
assert hashlib.sha256(patch.read_bytes()).hexdigest() == lock["patchSha256"]
for name in ("cp", "googletest"):
    repo = destination / name
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "fetch", "--quiet", "--depth=1", lock[name]["url"], lock[name]["commit"]], cwd=repo, check=True)
    subprocess.run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], cwd=repo, check=True)
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip() == lock[name]["commit"]
cp = destination / "cp"
host = [sys.executable, str(HERE / "run_host.py"), str(cp), str(destination / "googletest")]
subprocess.run(host + [str(destination / "before"), "--expect-old-failure"], check=True)
subprocess.run(["git", "apply", "--check", str(patch)], cwd=cp, check=True)
subprocess.run(["git", "apply", str(patch)], cwd=cp, check=True)
assert hashlib.sha256((cp / "src/activities/plugins/PluginCatalogActivity.cpp").read_bytes()).hexdigest() == lock["resultSha256"]
subprocess.run(["git", "diff", "--check"], cwd=cp, check=True)
subprocess.run(host + [str(destination / "after")], check=True)
receipt = {"result": "PASS", "cp": lock["cp"]["commit"], "patchSha256": lock["patchSha256"],
           "before": json.loads((destination / "before/receipt.json").read_text()),
           "after": json.loads((destination / "after/receipt.json").read_text()), "device": "NOT_MEASURED"}
(destination / "reproduction.json").write_text(json.dumps(receipt, indent=2) + "\n")
