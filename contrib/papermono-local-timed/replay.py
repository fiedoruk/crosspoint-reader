"""Apply public exact T1/T2 prerequisites and run host checks in a new directory."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time
from urllib.request import urlopen

BASE = "59555361aef55608cc56fdb5a9fccc167c37db34"
SDK = "7fcd3b34c108f28c086ade3b433924022dbc0998"
T1_SHA = "5adb88dc3f9c78858e4d4b33d7622df4b3c0a3bad3d6cb9276e992bc3a6f17e0"
T2_SHA = "3ef1a817068db2bc2236216b9bb228dfebfe99e58d903925d399e24a7115aca7"
T1_URL = "https://raw.githubusercontent.com/fiedoruk/crosspoint-reader/3529a9dadea4a93cb9e6e9ef87712331c750d7db/contrib/timed-power-handoff/t1-power.patch"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
root = args.destination.resolve()
root.mkdir(parents=True, exist_ok=False)
patch = Path(__file__).resolve().parent / "t2-papermono.patch"
assert hashlib.sha256(patch.read_bytes()).hexdigest() == T2_SHA
receipt = {"status": "RUNNING", "base": BASE, "sdk": SDK, "t1Sha256": T1_SHA, "t2Sha256": T2_SHA}
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
        with urlopen(T1_URL, timeout=30) as response:
            data = response.read(262145)
        assert len(data) <= 262144 and hashlib.sha256(data).hexdigest() == T1_SHA
        t1 = root / "t1-power.patch"
        t1.write_bytes(data)
        cp = root / "crosspoint"
        fetch(cp, "https://github.com/jadehawk/crosspoint-reader.git", BASE)
        fetch(cp / "freeink-sdk", "https://github.com/Free-Ink/freeink-sdk.git", SDK)
        run(["git", "submodule", "init", "freeink-sdk"], cp)
        for item in (t1, patch):
            run(["git", "apply", "--check", str(item)], cp)
            run(["git", "apply", str(item)], cp)
        for test in (["python3", "test/papermono_timer/run.py", "--negative-control"],
                     ["python3", "test/timed_power_wake/run.py"],
                     ["python3", "test/timer_wake_arm/run.py"]):
            run(test, cp)
        receipt["status"] = "HOST_PASS_DEVICE_NOT_MEASURED"
    except Exception as error:
        receipt.update(status="FAIL", error=str(error))
        raise
    finally:
        receipt["wallSeconds"] = round(time.monotonic() - started, 3)
        (root / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
