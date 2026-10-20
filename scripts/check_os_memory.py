#!/usr/bin/env python3
"""Test the private procfs parser without loading unrelated STD modules."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qz", type=Path, help="matching compiler executable")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="quazi-os-memory-") as directory:
        work = Path(directory)
        (work / "src").mkdir()
        (work / "quazi.toml").write_text(
            '[package]\nname="os_memory_tests"\nversion="0.1.0"\n'
            '[lib]\npath="src/tests.qz"\n'
        )
        shutil.copyfile(root / "src/os_memory.qz", work / "src/os_memory.qz")
        shutil.copyfile(root / "tests/os_memory.qz", work / "src/tests.qz")
        subprocess.run(
            [str(args.qz.resolve()), "test", "--no-color", "--no-unicode"],
            cwd=work, check=True, timeout=120,
        )


if __name__ == "__main__":
    main()
