#!/usr/bin/env python3
"""Check the std.thread lifecycle contract (D-007, maintainer answer В29А).

A panic on a thread started by `thread.spawn` is reported and ends only that
thread: `join()` returns `Err(ThreadError.Panicked)` and the program goes on.
A handle dropped without `join()` waits for its thread. `JoinHandle.cancel`
is cooperative and seen through `thread.cancel_requested()`. A panic on the
main thread stays fatal (status 101), a custom `@panic_handler` runs only for
fatal panics, and a panic inside a thread's panic report aborts.

`Channel[T]` carries owned values between threads.

Runs with the libc-free clone runtime, with pthreads (`libc = true`) and
under `qz run --jit`; concurrent panics must neither deadlock nor leak.
With `--wine`, the programs also run as Windows executables under Wine;
NetBSD objects must build (no runtime here).
"""

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

LIFECYCLE = r"""import std.io;
import std.thread;
import std.thread.ThreadError;

fn boom(n: i32) i32 {
    if (n > 3) { panic("thread failed with {}", n); }
    n
}

fn deep(n: i32) i32 {
    if (n == 0) { ret boom(9); }
    ret deep(n - 1) + 1;
}

fn wait_for_cancel() i32 {
    for (!thread.cancel_requested()) { thread.yield_now(); }
    7
}

fn main() i32 {
    io.println("main cancel {}", thread.cancel_requested());
    const ok = thread.spawn(|| boom(2)).unwrap();
    io.println("ok {}", ok.join().unwrap());
    const bad = thread.spawn(|| boom(5)).unwrap();
    match bad.join() {
        Ok(_) => io.println("unexpected"),
        Err(ThreadError.Panicked) => io.println("panicked reported"),
        Err(_) => io.println("other"),
    };
    const nested = thread.spawn(|| deep(200)).unwrap();
    io.println("deep panicked {}", nested.join().is_err());
    const worker = thread.spawn(|| wait_for_cancel()).unwrap();
    worker.cancel();
    io.println("cancelled {}", worker.join().unwrap());
    var round: i32 = 0;
    for (round < 40) {
        const dropped = thread.spawn(|| boom(round % 2 + 3)).unwrap();
        round = round + 1;
    }
    io.println("dropped handles joined");
    panic("main still fatal");
}
"""
LIFECYCLE_STDOUT = ("main cancel false\nok 2\npanicked reported\ndeep panicked true\n"
                    "cancelled 7\ndropped handles joined\n")

HANDLER = r"""import std.io;
import std.core;
import std.thread;

@panic_handler
fn handler(info: PanicInfo) ! {
    io.errln("handled: {}", info.message());
    core.exit(42);
}

fn fail() i32 { panic("worker failure"); }

fn main() i32 {
    const worker = thread.spawn(|| fail()).unwrap();
    io.println("worker error {}", worker.join().is_err());
    panic("main failure");
}
"""

# Eight threads panic at once, many times: no deadlock in the isolation
# registry, every join reports the panic, and memory stays flat.
CONCURRENT = r"""import std.io;
import std.thread;

fn fail(n: i32) i32 {
    if (n >= 0) { panic("concurrent {}", n); }
    n
}

fn main() i32 {
    var failures: i32 = 0;
    var round: i32 = 0;
    for (round < 300) {
        const a = thread.spawn(|| fail(1)).unwrap();
        const b = thread.spawn(|| fail(2)).unwrap();
        const c = thread.spawn(|| fail(3)).unwrap();
        const d = thread.spawn(|| fail(4)).unwrap();
        const e = thread.spawn(|| fail(-5)).unwrap();
        if (a.join().is_ok()) { failures = failures + 1; }
        if (b.join().is_ok()) { failures = failures + 1; }
        if (c.join().is_ok()) { failures = failures + 1; }
        if (d.join().is_ok()) { failures = failures + 1; }
        if (e.join().is_err()) { failures = failures + 1; }
        round = round + 1;
    }
    io.println("failures {}", failures);
    0
}
"""


# A panic abandons the frames that own the thread's closures; the thread
# entry must still free them. Captured state makes a leak measurable: the
# same number of panicking threads with and without captures must peak alike.
LEAK = r"""import std.thread;

fn fail(a: i64, b: i64, c: i64, d: i64) i64 {
    if (a >= 0) { panic("leak probe"); }
    a + b + c + d
}

fn main() i32 {
    var round: i64 = 0;
    for (round < 40000) {
        const a: i64 = round;
        const b: i64 = round + 1;
        const c: i64 = round + 2;
        const d: i64 = round + 3;
        const worker = thread.spawn(|| CALL).unwrap();
        worker.join().is_err();
        round = round + 1;
    }
    0
}
"""


# Channel[T] is the communication surface between threads: two producer
# threads and a consumer thread exchange owned Strings; the sum of their
# lengths is exact and memory stays flat over 50 rounds.
CHANNELS = r"""import std.io;
import std.thread;

fn produce(out: &Channel[String], id: i64, n: i64) i64 {
    var i: i64 = 0;
    for (i < n) {
        const text: String = "w{id}-{i}";
        out.send(text);
        i = i + 1;
    }
    n
}

fn consume(input: &Channel[String]) i64 {
    var total: i64 = 0;
    for (true) {
        const next = input.receive();
        if (next.is_none()) { break; }
        const text: String = next.unwrap();
        total = total + text.len() as i64;
    }
    total
}

fn main() i32 {
    var round: i32 = 0;
    for (round < 50) {
        const ch: Channel[String] = Channel.new(8);
        const a = ch.clone();
        const b = ch.clone();
        const c = ch.clone();
        const reader = thread.spawn(|| consume(&c)).unwrap();
        const first = thread.spawn(|| produce(&a, 1, 2000)).unwrap();
        const second = thread.spawn(|| produce(&b, 2, 2000)).unwrap();
        const sent = first.join().unwrap() + second.join().unwrap();
        ch.close();
        const total = reader.join().unwrap();
        if (round == 0) { io.println("sent {} total {}", sent, total); }
        round = round + 1;
    }
    0
}
"""


def run(command, cwd, timeout=300):
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)


def build(qz, root, name, source, libc=False, extra=()):
    case = root / name
    (case / "src").mkdir(parents=True)
    toml = f'[package]\nname="{name}"\n[build]\nentry="src/main.qz"\n'
    if libc:
        toml += '[target.x86_64-linux.link]\nlibc = true\n'
    (case / "quazi.toml").write_text(toml)
    (case / "src/main.qz").write_text(source)
    binary = case / "native"
    result = run([str(qz), "build", "--no-incremental", "--no-color", "--no-unicode",
                  "--silent", *extra, "-o", str(binary)], case)
    assert result.returncode == 0, f"{name}: build failed\n{result.stdout}{result.stderr}"
    return case, binary


def check_lifecycle(result, label):
    assert result.returncode == 101, (label, result.returncode, result.stderr)
    assert result.stdout == LIFECYCLE_STDOUT, (label, result.stdout)
    lines = result.stderr.splitlines()
    thread_reports = [line for line in lines if line.startswith("thread panicked at 'thread failed with")]
    assert len(thread_reports) == 22, (label, len(thread_reports), result.stderr[-2000:])
    assert "thread 'main' panicked at 'main still fatal'" in result.stderr, (label, result.stderr)


def peak_kib(binary, cwd):
    result = run(["/usr/bin/env", "time", "-f", "%M", str(binary)], cwd)
    return result, int(result.stderr.strip().splitlines()[-1])


def check(qz, root, wine=None):
    for libc in (False, True):
        case, binary = build(qz, root, f"lifecycle_{'libc' if libc else 'clone'}", LIFECYCLE, libc)
        if libc:
            assert b"pthread_create" in binary.read_bytes(), "libc build must use pthreads"
        for _ in range(3):
            check_lifecycle(run([str(binary)], case), f"native libc={libc}")
    jit = run([str(qz), "run", "--jit", "--no-incremental", "--no-color", "--no-unicode",
               "--silent"], root / "lifecycle_clone")
    check_lifecycle(jit, "--jit")
    print("PASS thread lifecycle: isolated panics join as Err(Panicked), drop joins, "
          "cooperative cancel, main panic fatal (clone runtime, pthreads, --jit)")

    case, binary = build(qz, root, "handler", HANDLER)
    result = run([str(binary)], case)
    assert result.returncode == 42, (result.returncode, result.stderr)
    assert result.stdout == "worker error true\n", result.stdout
    assert "thread panicked at 'worker failure'" in result.stderr, result.stderr
    assert "handled: worker failure" not in result.stderr, result.stderr
    assert "handled: main failure" in result.stderr, result.stderr
    print("PASS custom panic handler runs only for the fatal main-thread panic")

    for libc in (False, True):
        case, binary = build(qz, root, f"concurrent_{'libc' if libc else 'clone'}", CONCURRENT, libc)
        result, peak = peak_kib(binary, case)
        assert result.returncode == 0, (libc, result.returncode, result.stderr[-2000:])
        assert result.stdout == "failures 0\n", (libc, result.stdout)
        # Reports from concurrent panics interleave (each is several writes);
        # the prefix is one write.
        assert result.stderr.count("thread panicked at '") == 1200, libc
        # 1200 panics; a leaked isolation record or thread block per panic
        # would show, but the bound mostly guards against leaked stacks.
        assert peak < 64 * 1024, (libc, peak)
    print("PASS concurrent thread panics: 1200 isolated panics, no deadlock, bounded memory")

    peaks = {}
    for name, call in (("captures", "fail(a, b, c, d)"), ("plain", "fail(0, 1, 2, 3)")):
        case, binary = build(qz, root, f"leak_{name}", LEAK.replace("CALL", call))
        result, peaks[name] = peak_kib(binary, case)
        assert result.returncode == 0, (name, result.returncode, result.stderr[-1000:])
    # Without the fix the captures run peaks about 1 MiB higher; correct
    # runs measured equal.
    assert peaks["captures"] - peaks["plain"] < 512, peaks
    print(f"PASS panicking threads release their closures (peak {peaks['captures']} vs {peaks['plain']} KiB)")

    for libc in (False, True):
        case, binary = build(qz, root, f"channels_{'libc' if libc else 'clone'}", CHANNELS, libc)
        result, peak = peak_kib(binary, case)
        assert result.returncode == 0, (libc, result.returncode, result.stderr[-1000:])
        assert result.stdout == "sent 4000 total 25780\n", (libc, result.stdout)
        assert peak < 16 * 1024, (libc, peak)
    print("PASS Channel[T] between OS threads: 2 producers, 1 consumer, owned Strings, flat memory")

    if wine:
        check_windows(qz, root, wine)

    for target, magic in (("x86_64-windows", b"\x64\x86"), ("x86_64-netbsd", b"\x7fELF")):
        case = root / "lifecycle_clone"
        output = case / f"object-{target}"
        result = run([str(qz), "build", "--no-incremental", "--no-color", "--no-unicode", "--silent",
                      "-c", "--target", target, "-o", str(output)], case)
        assert result.returncode == 0, (target, result.stdout, result.stderr)
        assert output.read_bytes()[:len(magic)] == magic, target
    print("PASS thread lifecycle objects build for Windows and NetBSD (not run here)")


def check_windows(qz, root, wine):
    """The same programs as Windows PE32+ executables under Wine."""
    environment = dict(os.environ, WINEDEBUG="-all", WINEPREFIX=str(root / "wineprefix"))

    def windows(name, source):
        case, binary = build(qz, root, f"win_{name}", source, extra=("--target", "x86_64-windows"))
        exe = binary.rename(case / "program.exe")
        result = subprocess.run([str(wine), str(exe)], cwd=case, text=True, capture_output=True,
                                timeout=600, env=environment)
        result.stdout = result.stdout.replace("\r\n", "\n")
        result.stderr = result.stderr.replace("\r\n", "\n")
        return result

    check_lifecycle(windows("lifecycle", LIFECYCLE), "windows")
    result = windows("handler", HANDLER)
    assert result.returncode == 42 and result.stdout == "worker error true\n", (result.returncode, result.stdout)
    assert "handled: worker failure" not in result.stderr and "handled: main failure" in result.stderr
    result = windows("concurrent", CONCURRENT)
    assert result.returncode == 0 and result.stdout == "failures 0\n", (result.returncode, result.stdout)
    assert result.stderr.count("thread panicked at '") == 1200
    result = windows("channels", CHANNELS)
    assert result.returncode == 0 and result.stdout == "sent 4000 total 25780\n", (result.returncode, result.stdout)
    print("PASS Windows under Wine: lifecycle, handler, 1200 concurrent panics, channels")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qz", type=Path, required=True, help="matching compiler executable")
    parser.add_argument("--wine", type=Path, help="Wine executable for the Windows column")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        check(args.qz.resolve(), Path(directory), args.wine)


if __name__ == "__main__":
    main()
