#!/usr/bin/env python3
"""Check std.process on every POSIX target from one host.

Linux runs a `Command` program (PATH lookup, working directory, environment,
captured output, exit status, Child try_wait/terminate/wait). NetBSD links
the same program into an executable with the built-in NetBSD linker; its
fork/execve/waitpid/kill/pipe2/poll calls must be libc imports. NetBSD cannot
run here, so only the link is checked."""

import argparse
import subprocess
import tempfile
from pathlib import Path

PROGRAM = r"""import std.io;
import std.os;
import std.process;
import std.process.ExitStatus;

fn main() i32 {
    os.set_env("QUAZI_PROCESS_TARGETS", "inherited").unwrap();
    const out = process.Command.new("sh").arg("-c").arg("printf '%s %s ' \"$QUAZI_PROCESS_TARGETS\" \"$EXTRA\"; pwd; exit 3")
        .current_dir("/").env("EXTRA", "set").output().unwrap();
    io.println("{}", out.stdout.len());
    const code: i32 = match out.status { ExitStatus.Code(value) => value, ExitStatus.Signal(_) => -1 };
    var sleeper = process.Command.new("sleep").arg("5").spawn().unwrap();
    const early = sleeper.try_wait().unwrap();
    sleeper.terminate().unwrap();
    const ended = sleeper.wait().unwrap();
    const killed: bool = match ended.unwrap() { ExitStatus.Signal(_) => true, ExitStatus.Code(_) => false };
    io.println("{} {} {}", code, early.is_none(), killed);
    0
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qz", type=Path, required=True, help="matching compiler executable")
    qz = str(parser.parse_args().qz.resolve())
    with tempfile.TemporaryDirectory(prefix="quazi-process-targets-") as directory:
        root = Path(directory)
        (root / "src").mkdir()
        (root / "quazi.toml").write_text('[package]\nname="targets"\n[build]\nentry="src/main.qz"\n')
        (root / "src/main.qz").write_text(PROGRAM)
        common = ["--no-incremental", "--no-color", "--silent"]
        build = subprocess.run([qz, "build", *common, "-o", str(root / "linux")], cwd=root,
                               text=True, capture_output=True, timeout=600)
        assert build.returncode == 0, build.stdout + build.stderr
        result = subprocess.run([str(root / "linux")], cwd=root, text=True, capture_output=True,
                                timeout=60)
        assert result.returncode == 0 and result.stdout == "16\n3 true true\n", (
            result.returncode, result.stdout, result.stderr)
        build = subprocess.run([qz, "build", *common, "--target", "x86_64-netbsd", "-o",
                                str(root / "netbsd")], cwd=root, text=True, capture_output=True,
                               timeout=600)
        assert build.returncode == 0, build.stdout + build.stderr
        image = (root / "netbsd").read_bytes()
        assert image[:4] == b"\x7fELF" and b"/usr/libexec/ld.elf_so" in image
        for symbol in (b"fork", b"execve", b"waitpid", b"kill", b"pipe2", b"poll", b"_exit"):
            assert symbol + b"\0" in image, symbol
    print("PASS process targets: Linux Command/Child run; NetBSD executable links libc process calls")


if __name__ == "__main__":
    main()
