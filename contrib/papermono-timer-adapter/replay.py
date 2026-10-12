"""Apply the PaperMono adapter to public timer/SDK refs and run scoped host tests."""
from pathlib import Path
import argparse, hashlib, json, subprocess, time

CP = "c3568c7abaaedb427f35421e73a712ac77fcc996"
OLD_SDK = "425d200a8ea447326b4b9696e4e47dc84ad9d7f6"
SDK = "1a5448dfa705d6499fbff20371539bf553865dd2"
PATCH = "0fa79deb5230ed58ac738eed630264eff3a2a2b01f56ff7b045b517c8c78f791"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
root = args.destination.resolve()
root.mkdir(parents=True, exist_ok=False)
patch = Path(__file__).resolve().parent / "papermono-timer-adapter.patch"
assert hashlib.sha256(patch.read_bytes()).hexdigest() == PATCH
receipt = {"status": "RUNNING", "cp": CP, "sdk": SDK, "patchSha256": PATCH}
started = time.monotonic()
with (root / "replay.log").open("w") as log:
    def run(command, cwd):
        log.write("$ " + " ".join(command) + "\n")
        log.flush()
        subprocess.run(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, check=True)

    def fetch(path, url, ref):
        path.mkdir(exist_ok=True)
        run(["git", "init", "-q"], path)
        run(["git", "remote", "add", "origin", url], path)
        run(["git", "fetch", "--depth=1", "origin", ref], path)
        run(["git", "checkout", "--detach", "FETCH_HEAD"], path)
        assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=path, text=True).strip() == ref

    try:
        cp = root / "crosspoint"
        fetch(cp, "https://github.com/crosspoint-reader/crosspoint-reader.git", CP)
        sdk = cp / "freeink-sdk"
        fetch(sdk, "https://github.com/Free-Ink/freeink-sdk.git", OLD_SDK)
        run(["git", "submodule", "init", "freeink-sdk"], cp)
        run(["git", "apply", "--index", "--check", str(patch)], cp)
        run(["git", "apply", "--index", str(patch)], cp)
        run(["git", "fetch", "--depth=1", "origin", SDK], sdk)
        run(["git", "checkout", "--detach", SDK], sdk)
        assert subprocess.check_output(["git", "submodule", "status"], cwd=cp, text=True).startswith(" " + SDK)
        run(["python3", "test/papermono_timer/run.py", "--negative-control"], cp)
        run(["python3", "test/timer_wake_arm/run.py"], cp)
        build = root / "host-build"
        run(["cmake", "-S", str(cp / "test"), "-B", str(build)], root)
        cache = (build / "CMakeCache.txt").read_text()
        ctest = next(line.split("=", 1)[1] for line in cache.splitlines() if line.startswith("CMAKE_CTEST_COMMAND:"))
        run([ctest, "--test-dir", str(build), "-R", "^PaperMonoTimer$", "--output-on-failure"], root)
        receipt.update(status="PASS", cases="13 wake/reset +6 shutdown +RTC API cases; original negative42; ESP EXT1=0/1; CTest discovery")
    except Exception as error:
        receipt.update(status="FAIL", error=str(error))
        raise
    finally:
        receipt["wallSeconds"] = round(time.monotonic() - started, 3)
        (root / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
