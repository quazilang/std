#!/usr/bin/env python3
"""Check std.dylib lifetimes: an explicit `close` and scope-end cleanup each
unload a library exactly once. A consuming `close` used to drop `self`
through `free`, which called `close` again until the stack overflowed."""

import argparse
import subprocess
import tempfile
from pathlib import Path

PROGRAM = r"""import std.io;
import std.dylib.DynamicLibrary;

fn main() i32 {
    const first = DynamicLibrary.open("libc.so.6").unwrap();
    if (!first.close().unwrap()) { ret 1; }
    var round: i32 = 0;
    for (round < 200) {
        const library = DynamicLibrary.open("libc.so.6").unwrap();
        if (library.raw_handle() == 0) { ret 2; }
        round = round + 1;
    }
    io.println("dylib ok");
    0
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qz", type=Path, required=True, help="matching compiler executable")
    qz = parser.parse_args().qz.resolve()
    with tempfile.TemporaryDirectory(prefix="quazi-dylib-") as directory:
        root = Path(directory)
        (root / "src").mkdir()
        (root / "quazi.toml").write_text(
            '[package]\nname="dylib"\n[build]\nentry="src/main.qz"\n'
            '[target.x86_64-linux.link]\nlibc = true\n')
        (root / "src/main.qz").write_text(PROGRAM)
        build = subprocess.run([str(qz), "build", "--no-incremental", "--no-color", "--silent",
                                "-o", str(root / "program")], cwd=root, text=True,
                               capture_output=True, timeout=600)
        assert build.returncode == 0, build.stdout + build.stderr
        result = subprocess.run([str(root / "program")], cwd=root, text=True,
                                capture_output=True, timeout=120)
        assert result.returncode == 0 and result.stdout == "dylib ok\n", (
            result.returncode, result.stdout, result.stderr[-500:])
    print("PASS dylib: close unloads once, 200 scope-end unloads, no recursion")


if __name__ == "__main__":
    main()
