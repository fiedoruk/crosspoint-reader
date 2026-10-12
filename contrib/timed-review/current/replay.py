"""Reproduce the complete SD timer consumer from an ordered public series from pinned public refs; no firmware or device operation."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
root = args.destination.resolve()
root.mkdir(parents=True, exist_ok=False)
packet = Path(__file__).resolve().parent
manifest = json.loads((packet / "manifest.json").read_text())
for name, digest in manifest["files"].items():
    assert hashlib.sha256((packet / name).read_bytes()).hexdigest() == digest, name
started = time.monotonic()
series = json.loads((packet / "series.json").read_text())
receipt = {"status": "RUNNING", "publicRefs": series["refs"]}
with (root / "replay.log").open("w") as log:
    def run(command, cwd, env=None):
        log.write("$ " + " ".join(map(str, command)) + "\n")
        log.flush()
        subprocess.run(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, check=True, env=env)

    def fetch(path, spec):
        path.mkdir(exist_ok=True)
        run(["git", "init", "-q"], path)
        run(["git", "remote", "add", "origin", spec["url"]], path)
        run(["git", "fetch", "--depth=1", "origin", spec["commit"]], path)
        run(["git", "checkout", "--detach", "FETCH_HEAD"], path)
        assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=path, text=True).strip() == spec["commit"]

    try:
        cp = root / "crosspoint"
        fetch(cp, series["refs"]["cp"])
        sdk = cp / "freeink-sdk"
        fetch(sdk, series["refs"]["sdk"])
        repos = {"cp": cp, "sdk": sdk}
        for step in series["steps"]:
            patch = packet / step["file"]
            assert hashlib.sha256(patch.read_bytes()).hexdigest() == step["sha256"]
            run(["git", "apply", "--check", str(patch)], repos[step["repository"]])
            run(["git", "apply", str(patch)], repos[step["repository"]])
        for name, repo in repos.items():
            for path, digest in series["finalSources"][name].items():
                assert hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest, path
        scratch = root / "negative-source"
        (scratch / "src").mkdir(parents=True)
        baseline = scratch / "src/main.cpp"
        baseline.write_bytes((cp / "src/main.cpp").read_bytes())
        run(["git", "init", "-q"], scratch)
        run(["git", "apply", "--reverse", str(packet / series["permissionNegative"]["reversePatch"])], scratch)
        assert hashlib.sha256(baseline.read_bytes()).hexdigest() == series["permissionNegative"]["baselineMainSha256"]
        aj = root / "ArduinoJson"
        fetch(aj, series["refs"]["arduinojson"])
        include = str(aj / "src")
        env = dict(os.environ, CROSSPOINT_ARDUINOJSON_INCLUDE=include)
        checks = [
            ["python3", "test/timer_plugin_permission/run.py", "--arduinojson", include, "--baseline-main", str(baseline)],
            ["python3", "test/trusted_time_fresh/run.py"],
            ["python3", "test/plugin_verified_http/run.py", "--arduinojson", include, "--sanitize"],
            ["python3", "test/plugin_event_budget/run.py", "--arduinojson", include, "--sanitize"],
            ["python3", "test/timed_sync/run.py", "--sanitize"],
            ["python3", "test/papermono_timer/run.py"],
        ]
        for check in checks:
            run(check, cp, env)
        receipt.update(status="PASS", tests="ordered seven-patch assembly/source hashes, permission and baseline negative42, trusted time, verified/bounded events, completeTIMED and PaperMono host cases")
    except Exception as error:
        receipt.update(status="FAIL", error=str(error))
        raise
    finally:
        receipt["wallSeconds"] = round(time.monotonic() - started, 3)
        (root / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
