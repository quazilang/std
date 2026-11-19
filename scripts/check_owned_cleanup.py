#!/usr/bin/env python3
"""Check that std owners release everything they hold when dropped.

Each case runs a loop 2,000 and 60,000 times; the peak resident memory must
not grow with the iteration count. Covered: HashMap insert/clear (field
replacement inside `clear`), BufReader/BufWriter (buffer replacement),
fs.LineReader and fs.BufferedWriter (their `free` hooks must destroy the
inner File, not only close it)."""

import argparse
import subprocess
import tempfile
from pathlib import Path

BODIES = {
    "hash_map": ("import std.collections.HashMap;",
                 "var m: HashMap[i64, i64] = HashMap.new(); m.insert(1, 2).unwrap(); "
                 "m.insert(3, 4).unwrap(); m.clear(); m.insert(5, 6).unwrap();"),
    "buffered_streams": ("import std.stream.{BufReader, BufWriter, ByteSource, ByteSink};",
                         "var data: Array[u8] = Array.new(); data.push(97); data.push(10); data.push(98); "
                         "var reader = BufReader.with_capacity(ByteSource.new(data), 2); "
                         "const line = reader.read_until(10).unwrap(); "
                         "var writer = BufWriter.with_capacity(ByteSink.new(), 2); "
                         "var payload: Array[u8] = Array.new(); payload.push(1); payload.push(2); payload.push(3); "
                         "writer.write_bytes(&payload).unwrap(); writer.flush().unwrap();"),
    "line_reader": ("import std.fs;", 'var lines = fs.LineReader.open("input.txt").unwrap();'),
    "buffered_writer": ("import std.fs;",
                        'var out = fs.BufferedWriter.create("output.txt").unwrap(); out.write_str("x").unwrap();'),
}


def peak(qz, root, name, header, body, rounds):
    case = root / f"{name}_{rounds}"
    (case / "src").mkdir(parents=True)
    (case / "quazi.toml").write_text(f'[package]\nname="{name}"\n[build]\nentry="src/main.qz"\n')
    (case / "input.txt").write_text("a\nb\n")
    (case / "src/main.qz").write_text(
        f"{header}\nfn main() i32 {{\n    var round: usize = 0;\n"
        f"    for (round < {rounds}) {{\n        {body}\n        round = round + 1;\n    }}\n    0\n}}\n")
    build = subprocess.run([str(qz), "build", "--no-incremental", "--no-color", "--silent", "-o",
                            str(case / "program")], cwd=case, text=True, capture_output=True,
                           timeout=600)
    assert build.returncode == 0, build.stdout + build.stderr
    result = subprocess.run(["/usr/bin/env", "time", "-f", "%M", str(case / "program")], cwd=case,
                            text=True, capture_output=True, timeout=300)
    assert result.returncode == 0, (name, result.stderr[-500:])
    return int(result.stderr.strip().splitlines()[-1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qz", type=Path, required=True, help="matching compiler executable")
    qz = parser.parse_args().qz.resolve()
    with tempfile.TemporaryDirectory(prefix="quazi-owned-cleanup-") as directory:
        root = Path(directory)
        for name, (header, body) in BODIES.items():
            small = peak(qz, root, name, header, body, 2000)
            large = peak(qz, root, name, header, body, 60000)
            # A leak of even 16 bytes per round would add about 900 KiB.
            assert large - small < 512, (name, small, large)
    print(f"PASS owned cleanup: {len(BODIES)} owners release their storage (flat peak memory)")


if __name__ == "__main__":
    main()
