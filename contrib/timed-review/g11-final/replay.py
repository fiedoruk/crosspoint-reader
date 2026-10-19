#!/usr/bin/env python3
"""Replay the two pinned review scopes without building, flashing or publishing."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

packet = Path(__file__).resolve().parent
manifest = json.loads((packet / "manifest.json").read_text())
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path)
parser.add_argument("--through", choices=("w06", "timed"), default="timed")
parser.add_argument("--cp-source", default=manifest["cpSource"])
parser.add_argument("--sdk-source", default=manifest["sdkSource"])
args = parser.parse_args()
destination = args.destination.resolve()
if destination.exists():
    parser.error("destination must not exist")
for name, expected in manifest["patches"].items():
    if hashlib.sha256((packet / "patches" / name).read_bytes()).hexdigest() != expected:
        raise SystemExit("Patch checksum mismatch: " + name)


def git(path, *command):
    return subprocess.check_output(["git", *command], cwd=path, text=True).strip()


def checkout(path, source, commit):
    path.mkdir(parents=True)
    git(path, "init", "--quiet")
    git(path, "remote", "add", "origin", source)
    git(path, "fetch", "--quiet", "--depth", "1", "origin", commit)
    git(path, "checkout", "--quiet", "--detach", commit)


checkout(destination, args.cp_source, manifest["cpBase"])
if git(destination, "rev-parse", "HEAD^{tree}") != manifest["cpBaseTree"]:
    raise SystemExit("Unexpected CP base tree")
if git(destination, "ls-tree", "HEAD", "freeink-sdk").split()[2] != manifest["sdkBase"]:
    raise SystemExit("Unexpected SDK gitlink")
sdk = destination / "freeink-sdk"
if sdk.exists():
    sdk.rmdir()  # Empty gitlink placeholder only.
checkout(sdk, args.sdk_source, manifest["sdkBase"])
git(sdk, "apply", "--index", str(packet / "patches/sdk-verified.patch"))
if git(sdk, "write-tree") != manifest["sdkTree"]:
    raise SystemExit("SDK result tree mismatch")
for step in manifest["steps"]:
    git(destination, "apply", "--index", str(packet / "patches" / step["patch"]))
    actual = git(destination, "write-tree")
    if actual != step["tree"]:
        raise SystemExit("Result tree mismatch: " + step["stage"])
    if step["stage"] == args.through:
        break
print(json.dumps({"status": "APPLIED_VERIFIED", "through": args.through,
                  "cpTree": actual, "sdkTree": manifest["sdkTree"],
                  "build": "NOT_RUN", "device": "NOT_MEASURED"}, indent=2))
