#!/usr/bin/env python3
"""Reconstruct this support packet from pinned public sources and run host checks."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path)
for name in ("cp", "sdk", "gtest"):
    parser.add_argument("--" + name + "-cache", type=Path)
args = parser.parse_args()
dest = args.destination.resolve()
dest.mkdir()
lock = json.loads((HERE / "source-lock.json").read_text())
for name, digest in lock["files"].items():
    assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, name
transport = {}
for name in ("cp", "sdk", "gtest"):
    repo = dest / ("cp/freeink-sdk" if name == "sdk" else name)
    repo.mkdir(exist_ok=name == "sdk")
    cache = getattr(args, name + "_cache")
    source = str(cache.resolve()) if cache else lock[name]["url"]
    transport[name] = "local Git cache" if cache else "public remote"
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "fetch", "--quiet", "--depth=1", source, lock[name]["commit"]], cwd=repo, check=True)
    subprocess.run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], cwd=repo, check=True)
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    assert actual == lock[name]["commit"], name
cp = dest / "cp"
for name in lock["patchOrder"]:
    subprocess.run(["git", "apply", "--check", str(HERE / name)], cwd=cp, check=True)
    subprocess.run(["git", "apply", str(HERE / name)], cwd=cp, check=True)
for name, digest in lock["resultFiles"].items():
    assert hashlib.sha256((cp / name).read_bytes()).hexdigest() == digest, name
subprocess.run(["git", "diff", "--check"], cwd=cp, check=True)
subprocess.run([sys.executable, str(HERE / "host/run.py"), str(cp), str(dest / "gtest"), str(dest / "host")], check=True)
if (HERE / "host/render.py").exists():
    subprocess.run([sys.executable, str(HERE / "host/render.py"), str(cp), str(dest / "layout")], check=True)
receipt = {"result": "PASS", "transport": transport, "refs": {k: lock[k]["commit"] for k in ("cp", "sdk", "gtest")}, "patchOrder": lock["patchOrder"], "host": json.loads((dest / "host/receipt.json").read_text()), "device": "NOT_MEASURED", "firmwareBuilds": 0}
if (dest / "layout/receipt.json").exists():
    receipt["layout"] = json.loads((dest / "layout/receipt.json").read_text())
(dest / "reproduction.json").write_text(json.dumps(receipt, indent=2) + "\n")
