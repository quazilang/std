#!/usr/bin/env python3
"""Run every std test under valgrind memcheck.

A scratch copy of std links libc (so programs use libc's allocator, which
valgrind tracks), `qz test` builds and runs the test runners, and each runner
is run again under valgrind: invalid reads/writes, uninitialised values and
bad frees fail the check. Pass the valgrind executable, for example from
`nix shell nixpkgs#valgrind`."""

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qz", type=Path, required=True, help="matching compiler executable")
    parser.add_argument("--valgrind", type=Path, required=True, help="valgrind executable")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="quazi-std-valgrind-") as directory:
        copy = Path(directory) / "std"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("build", ".quazi", "__pycache__"))
        with (copy / "quazi.toml").open("a") as manifest:
            manifest.write('\n[target.x86_64-linux.link]\nlibc = true\n')
        test = subprocess.run([str(args.qz.resolve()), "test", "--no-color"], cwd=copy, text=True,
                              capture_output=True, timeout=3600)
        assert test.returncode == 0, test.stdout[-2000:] + test.stderr[-2000:]
        runners = sorted(path for path in (copy / "build" / "tests").iterdir() if path.is_file())
        assert runners, "no test runners were built"
        failures = []
        for runner in runners:
            result = subprocess.run([str(args.valgrind), "-q", "--error-exitcode=9", str(runner)],
                                    cwd=copy, text=True, capture_output=True, timeout=600,
                                    stdin=subprocess.DEVNULL)
            if result.returncode == 9:
                failures.append((runner.name, result.stderr[-800:]))
        assert not failures, "\n\n".join(f"{name}:\n{text}" for name, text in failures)
    print(f"PASS valgrind: {len(runners)} std test runners clean under memcheck (libc allocator)")


if __name__ == "__main__":
    main()
