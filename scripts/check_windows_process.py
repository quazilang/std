#!/usr/bin/env python3
"""Check std.process on Windows (CreateProcessW) under Wine: exit codes,
argv quoting that CommandLineToArgvW reads back exactly, try_wait /
terminate / close, Command PATH lookup and current_dir, and spawn errors.
Usage: check_windows_process.py QZ WINE"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ARGS_PRINTER = """import std.io.println;
import std.os;
fn main() i32 {
    var args: Array[String] = os.args().unwrap();
    const program: String = args.remove(0);
    for (args.len() > 0) {
        const arg: String = args.remove(0);
        println("[{}]", arg);
    }
    ret 0;
}
"""

PARENT = """import std.io.println;
import std.process;
import std.process.ExitStatus;
fn code_of(status: Option[ExitStatus]) i32 {
    ret match status { Some(ExitStatus.Code(code)) => code, _ => -100 };
}
fn main() i32 {
    var exit_args: Array[str] = Array.new();
    exit_args.push("/c");
    exit_args.push("exit 7");
    const exiting = process.spawn("C:\\\\windows\\\\system32\\\\cmd.exe", exit_args).unwrap();
    println("exit {}", code_of(exiting.wait().unwrap()));
    var args: Array[str] = Array.new();
    args.push("plain");
    args.push("with space");
    args.push("quote\\"inside");
    args.push("trail\\\\");
    args.push("back\\\\\\"slash");
    args.push("");
    const printer = process.spawn("PRINTER", args).unwrap();
    println("printer {}", code_of(printer.wait().unwrap()));
    var slow_args: Array[str] = Array.new();
    slow_args.push("/c");
    slow_args.push("ping -n 5 127.0.0.1 >nul");
    var slow = process.spawn("C:\\\\windows\\\\system32\\\\cmd.exe", slow_args).unwrap();
    println("running {}", slow.try_wait().unwrap().is_none());
    println("terminated {}", slow.terminate().unwrap());
    println("closed {}", slow.close().unwrap());
    const status = process.Command.new("cmd.exe").arg("/c").arg("cd").current_dir("C:\\\\windows").status().unwrap();
    println("command {}", match status { ExitStatus.Code(code) => code, ExitStatus.Signal(_) => -1 });
    println("missing {}", process.spawn("C:\\\\definitely\\\\missing.exe", Array.new()).is_err());
    println("env unsupported {}", process.Command.new("cmd.exe").env("A", "1").status().is_err());
    const captured = process.Command.new("cmd.exe").arg("/c").arg("echo hello& echo oops 1>&2& exit 3").output().unwrap();
    println("output {} {} {}", match captured.status { ExitStatus.Code(code) => code, ExitStatus.Signal(_) => -1 }, captured.stdout.len(), captured.stderr.len());
    ret 0;
}
"""

EXPECTED = """exit 7
[plain]
[with space]
[quote"inside]
[trail\\]
[back\\"slash]
[]
printer 0
running true
terminated true
closed true
C:\\windows
command 0
missing true
env unsupported true
output 3 7 7
"""


def build(qz, root, name, source, output):
    path = root / name
    (path / "src").mkdir(parents=True)
    (path / "quazi.toml").write_text(f'[package]\nname="{name}"\n[build]\nentry="src/main.qz"\n')
    (path / "src/main.qz").write_text(source)
    result = subprocess.run([qz, "build", "--target", "x86_64-windows", "--silent",
                             "--no-incremental", "-o", str(output)], cwd=path, text=True,
                            capture_output=True, timeout=600)
    assert result.returncode == 0, result.stdout + result.stderr


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    qz, wine = str(Path(sys.argv[1]).resolve()), sys.argv[2]
    with tempfile.TemporaryDirectory(prefix="quazi-winprocess-") as directory:
        root = Path(directory)
        printer = root / "printer.exe"
        build(qz, root, "printer", ARGS_PRINTER, printer)
        windows_printer = "Z:" + str(printer).replace("/", "\\\\")
        build(qz, root, "parent", PARENT.replace("PRINTER", windows_printer), root / "parent.exe")
        env = dict(os.environ, WINEDEBUG="-all")
        result = subprocess.run([wine, str(root / "parent.exe")], text=True, capture_output=True,
                                timeout=300, env=env)
        output = result.stdout.replace("\r\n", "\n")
        assert result.returncode == 0, result.stdout + result.stderr
        assert output == EXPECTED, output
    print("PASS windows process: CreateProcessW exit codes, exact argv quoting, try_wait/terminate/close, "
          "Command PATH lookup, current_dir and output capture, spawn errors (Wine)")


if __name__ == "__main__":
    main()
