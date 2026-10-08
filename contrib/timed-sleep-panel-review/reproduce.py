#!/usr/bin/env python3
"""Reconstruct the pinned review series; optionally run its host checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args, cwd, env=None):
    subprocess.run(args, cwd=cwd, env=env, check=True)


def checkout(spec, target):
    target.mkdir()
    run(["git", "init", "-q"], target)
    run(["git", "fetch", "--quiet", "--depth=1", spec["url"], spec["commit"]], target)
    run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], target)
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=target, text=True).strip()
    if actual != spec["commit"]:
        raise RuntimeError("Unexpected revision: " + actual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="new directory; existing paths are refused")
    parser.add_argument("--test", action="store_true", help="fetch pinned ArduinoJson and run host tests")
    args = parser.parse_args()
    lock = json.loads((HERE / "series.json").read_text())
    for patch in lock["patches"]:
        if sha(HERE / patch["file"]) != patch["sha256"]:
            raise RuntimeError("Patch checksum mismatch: " + patch["file"])
    destination = args.destination.absolute()
    destination.mkdir()  # Do not reuse, reset or remove an existing checkout.
    started = time.monotonic()
    cp, sdk = destination / "crosspoint", destination / "crosspoint/freeink-sdk"
    checkout(lock["sources"]["crosspoint"], cp)
    # The submodule path is empty after checking out the parent repository.
    if sdk.exists():
        sdk.rmdir()
    checkout(lock["sources"]["sdk"], sdk)
    for patch in lock["patches"]:
        repo = cp if patch["repository"] == "crosspoint" else sdk
        path = str(HERE / patch["file"])
        run(["git", "apply", "--check", path], repo)
        run(["git", "apply", path], repo)
    for repository, files in lock["resultFiles"].items():
        base = cp if repository == "crosspoint" else sdk
        for name, expected in files.items():
            if sha(base / name) != expected:
                raise RuntimeError("Result checksum mismatch: " + name)
        run(["git", "diff", "--check"], base)
    receipt = {"sourceReconstruction": "PASS", "hostTests": "NOT_RUN",
               "crosspoint": lock["sources"]["crosspoint"]["commit"],
               "sdk": lock["sources"]["sdk"]["commit"],
               "seriesSha256": sha(HERE / "series.json"), "checks": []}
    if args.test:
        json_repo = destination / "ArduinoJson"
        checkout(lock["sources"]["arduinojson"], json_repo)
        include = str(json_repo / "src")
        env = dict(os.environ, CROSSPOINT_ARDUINOJSON_INCLUDE=include)
        checks = [
            ["test/trusted_time_fresh/run.py"],
            ["test/plugin_verified_http/run.py", "--arduinojson", include, "--sanitize"],
            ["test/plugin_event_budget/run.py", "--arduinojson", include, "--sanitize"],
            ["test/timed_wake_guard/run.py", "--sanitize"],
            ["test/timed_sync/run.py", "--sanitize"],
        ]
        for check in checks:
            print("CHECK " + check[0], flush=True)
            run([sys.executable, *check], cp, env)
            receipt["checks"].append({"script": check[0], "result": "PASS"})
        receipt["hostTests"] = "PASS"
    receipt["seconds"] = round(time.monotonic() - started, 3)
    receipt["firmwareBuild"] = "NOT_RUN"
    receipt["device"] = "NOT_TESTED"
    (destination / "reproduction.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
