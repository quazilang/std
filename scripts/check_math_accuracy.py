#!/usr/bin/env python3
"""Measure std.math accuracy in units in the last place (ULP).

A Quazi program reads (function, x, y) records as IEEE-754 bit patterns on
stdin and prints each result's bits; this script compares them with the host
C library through Python's `math` module (itself within about 1 ULP), checks
the special-value contract (NaN, infinities, signed zeros, domain errors) and
enforces the per-function bounds documented in docs/MATH_ACCURACY.md.
"""

import argparse
import math
import random
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

PROGRAM = r"""import std.io;
import std.math;
import std.core;

unsafe fn from_bits(cell: *u8, bits: u64) f64 {
    *(cell as *u64) = bits;
    ret *(cell as *f64);
}

unsafe fn to_bits(cell: *u8, value: f64) u64 {
    *(cell as *f64) = value;
    ret *(cell as *u64);
}

fn read_u64() u64 {
    const line = io.readln();
    if (line.is_err()) { ret 0; }
    const text: String = line.unwrap();
    const parsed: Result[u64, ParseError] = text.as_str().trim().as_str().parse[u64]();
    parsed.unwrap_or(0)
}

fn apply(id: u64, x: f64, y: f64) f64 {
    if (id == 0) { ret math.sqrt(x); }
    if (id == 1) { ret math.cbrt(x); }
    if (id == 2) { ret math.sin(x); }
    if (id == 3) { ret math.cos(x); }
    if (id == 4) { ret math.tan(x); }
    if (id == 5) { ret math.atan(x); }
    if (id == 6) { ret math.asin(x); }
    if (id == 7) { ret math.acos(x); }
    if (id == 8) { ret math.exp(x); }
    if (id == 9) { ret math.ln(x); }
    if (id == 10) { ret math.log2(x); }
    if (id == 11) { ret math.log10(x); }
    if (id == 12) { ret math.sinh(x); }
    if (id == 13) { ret math.cosh(x); }
    if (id == 14) { ret math.tanh(x); }
    if (id == 15) { ret math.atan2(x, y); }
    if (id == 16) { ret math.hypot(x, y); }
    if (id == 17) { ret math.pow(x, y); }
    if (id == 18) { ret math.floor(x); }
    if (id == 19) { ret math.ceil(x); }
    if (id == 20) { ret math.round(x); }
    if (id == 21) { ret math.trunc(x); }
    0.0
}

fn main() i32 {
    var cell: *u8 = 0;
    unsafe { cell = core.malloc(8); }
    const count = read_u64();
    for i : 0..count {
        const id = read_u64();
        const xb = read_u64();
        const yb = read_u64();
        unsafe {
            const result = apply(id, from_bits(cell, xb), from_bits(cell, yb));
            io.println("{}", to_bits(cell, result));
        }
    }
    0
}
"""

FUNCTIONS = [
    ("sqrt", math.sqrt), ("cbrt", math.cbrt),
    ("sin", math.sin), ("cos", math.cos), ("tan", math.tan), ("atan", math.atan),
    ("asin", math.asin), ("acos", math.acos), ("exp", math.exp), ("ln", math.log),
    ("log2", math.log2), ("log10", math.log10), ("sinh", math.sinh), ("cosh", math.cosh),
    ("tanh", math.tanh), ("atan2", math.atan2), ("hypot", math.hypot), ("pow", math.pow),
    ("floor", math.floor), ("ceil", math.ceil), ("round", None), ("trunc", math.trunc),
]
INDEX = {name: index for index, (name, _) in enumerate(FUNCTIONS)}


def bits(value):
    return struct.unpack("<Q", struct.pack("<d", value))[0]


def value(pattern):
    return struct.unpack("<d", struct.pack("<Q", pattern))[0]


def ordered(pattern):
    """Map bit patterns to integers that are monotonic in the float value."""
    return pattern if pattern < 1 << 63 else (1 << 63) - pattern


def ulps(actual, expected):
    if math.isnan(actual) and math.isnan(expected):
        return 0
    if math.isnan(actual) or math.isnan(expected):
        return math.inf
    return abs(ordered(bits(actual)) - ordered(bits(expected)))


def reference(name, function, x, y):
    if name == "round":
        # Halves away from zero; x - trunc(x) is exact, unlike x + 0.5.
        whole = float(math.trunc(x))
        rest = x - whole
        if rest >= 0.5:
            whole += 1.0
        elif rest <= -0.5:
            whole -= 1.0
        return math.copysign(whole, x) if whole == 0 else whole
    try:
        result = function(x, y) if name in ("atan2", "hypot", "pow") else function(x)
        return float(result)
    except (ValueError, OverflowError) as error:
        if isinstance(error, OverflowError):
            return math.inf
        return math.nan


def samples(rng):
    def uniform(low, high, count=400):
        return [rng.uniform(low, high) for _ in range(count)]

    def logarithmic(low, high, count=400):
        return [math.exp(rng.uniform(math.log(low), math.log(high))) for _ in range(count)]

    unary = {
        "sqrt": logarithmic(1e-300, 1e300), "cbrt": logarithmic(1e-300, 1e300),
        "sin": uniform(-10, 10) + uniform(-1e5, 1e5, 100), "cos": uniform(-10, 10) + uniform(-1e5, 1e5, 100),
        "tan": uniform(-1.5707963, 1.5707963), "atan": uniform(-1e3, 1e3), "asin": uniform(-1, 1),
        "acos": uniform(-1, 1), "exp": uniform(-700, 700), "ln": logarithmic(1e-300, 1e300),
        "log2": logarithmic(1e-300, 1e300), "log10": logarithmic(1e-300, 1e300),
        "sinh": uniform(-20, 20), "cosh": uniform(-20, 20), "tanh": uniform(-10, 10),
        "floor": uniform(-1e6, 1e6), "ceil": uniform(-1e6, 1e6), "round": uniform(-1e6, 1e6),
        "trunc": uniform(-1e6, 1e6),
    }
    records = [(name, x, 0.0) for name, xs in unary.items() for x in xs]
    records += [("atan2", y, x) for y, x in zip(uniform(-10, 10), uniform(-10, 10))]
    records += [("hypot", x, y) for x, y in zip(logarithmic(1e-150, 1e150), logarithmic(1e-150, 1e150))]
    records += [("pow", x, y) for x, y in zip(logarithmic(0.1, 100), uniform(-10, 10))]
    # Huge arguments (Payne-Hanek reduction) and multiples of pi/2.
    for name in ("sin", "cos", "tan"):
        records += [(name, x, 0.0) for x in logarithmic(1e6, 1e300, 200)]
        records += [(name, k * math.pi / 2, 0.0) for k in range(1, 400)]
    records += [(name, x, 0.0) for name, x in HARD]
    return records


# Inputs that defeated earlier implementations (review of 2026-11-10).
HARD = [
    ("sin", 1e300), ("sin", 1e22), ("cos", 1e22), ("tan", 1e300), ("cos", 1e15), ("sin", 1e10),
    ("cos", 45.553093477052), ("sin", 91.106186954104), ("tan", 182.212373908208),
    ("cos", 321307.9594422229), ("tan", 321307.9594422229), ("tan", 1.5707963267948966),
    ("sin", math.pi), ("cos", math.pi / 2), ("cbrt", 1.7976931348623157e308),
    ("cbrt", -1.7976931348623157e308), ("sinh", 710.0), ("cosh", 710.0), ("sinh", -710.0),
    ("round", 0.49999999999999994), ("round", -0.5), ("round", 4503599627370495.5),
]


# Special values: (function, x, y, expected) where expected may be nan/inf/signed zero.
SPECIAL = [
    ("sqrt", -1.0, 0.0, math.nan), ("sqrt", 0.0, 0.0, 0.0), ("sqrt", -0.0, 0.0, -0.0),
    ("sqrt", math.inf, 0.0, math.inf), ("sqrt", math.nan, 0.0, math.nan),
    ("ln", 0.0, 0.0, -math.inf), ("ln", -1.0, 0.0, math.nan), ("ln", math.inf, 0.0, math.inf),
    ("exp", math.inf, 0.0, math.inf), ("exp", -math.inf, 0.0, 0.0), ("exp", 1000.0, 0.0, math.inf),
    ("exp", math.nan, 0.0, math.nan), ("sin", math.inf, 0.0, math.nan), ("cos", math.nan, 0.0, math.nan),
    ("asin", 2.0, 0.0, math.nan), ("acos", -2.0, 0.0, math.nan), ("atan", math.inf, 0.0, math.pi / 2),
    ("tanh", math.inf, 0.0, 1.0), ("tanh", -math.inf, 0.0, -1.0), ("hypot", math.inf, math.nan, math.inf),
    ("pow", 0.0, -1.0, math.inf), ("pow", -8.0, 1.0 / 3.0, math.nan), ("pow", 1.0, math.nan, 1.0),
    ("floor", -0.5, 0.0, -1.0), ("ceil", -0.5, 0.0, -0.0), ("trunc", -0.0, 0.0, -0.0),
    ("floor", 4.5e15, 0.0, 4.5e15), ("round", 2.5, 0.0, 3.0), ("round", -2.5, 0.0, -3.0),
    ("cbrt", -27.0, 0.0, -3.0), ("sqrt", 5e-324, 0.0, math.sqrt(5e-324)),
]

# Maximum error in ULP over the sampled domains (docs/MATH_ACCURACY.md).
# The reference itself is within about 1 ULP, hence one ULP of slack.
BOUNDS = {
    "sqrt": 0, "cbrt": 3, "sin": 2, "cos": 2, "tan": 3, "atan": 2, "asin": 3, "acos": 2,
    "exp": 4, "ln": 2, "log2": 3, "log10": 4, "sinh": 6, "cosh": 5, "tanh": 3, "atan2": 2,
    "hypot": 2, "pow": 64, "floor": 0, "ceil": 0, "round": 0, "trunc": 0,
}


def run(qz, records):
    with tempfile.TemporaryDirectory(prefix="quazi-math-") as directory:
        root = Path(directory)
        (root / "src").mkdir()
        (root / "quazi.toml").write_text('[package]\nname = "mathaccuracy"\n\n[build]\nentry = "src/main.qz"\n')
        (root / "src/main.qz").write_text(PROGRAM)
        build = subprocess.run([str(qz), "build", "--no-incremental", "--no-progress", "--no-color",
                                "-o", "probe"], cwd=root, capture_output=True, text=True)
        assert build.returncode == 0, build.stderr
        stdin = [str(len(records))]
        for name, x, y in records:
            stdin += [str(INDEX[name]), str(bits(x)), str(bits(y))]
        result = subprocess.run([str(root / "probe")], input="\n".join(stdin) + "\n",
                                capture_output=True, text=True, timeout=300)
        assert result.returncode == 0, result.stderr
        return [value(int(line)) for line in result.stdout.split()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qz", type=Path, required=True)
    parser.add_argument("--report", action="store_true", help="print measured errors only")
    args = parser.parse_args()
    rng = random.Random(20261110)
    records = samples(rng)
    outputs = run(args.qz.resolve(), records + [(n, x, y) for n, x, y, _ in SPECIAL])
    worst = {}
    for (name, x, y), actual in zip(records, outputs):
        error = ulps(actual, reference(name, dict(FUNCTIONS)[name], x, y))
        if error > worst.get(name, (-1, None))[0]:
            worst[name] = (error, (x, y))
    failures = []
    for (name, x, y, expected), actual in zip(SPECIAL, outputs[len(records):]):
        same_zero_sign = not (expected == 0 and actual == 0) or math.copysign(1, expected) == math.copysign(1, actual)
        if ulps(actual, expected) > 1 or not same_zero_sign:
            failures.append(f"special {name}({x}, {y}) = {actual!r}, expected {expected!r}")
    for name, _ in FUNCTIONS:
        error, (x, y) = worst[name]
        print(f"{name:6} max {error:.0f} ULP at ({x!r}, {y!r})")
        if not args.report and name in BOUNDS and error > BOUNDS[name]:
            failures.append(f"{name}: {error} ULP exceeds the documented bound {BOUNDS[name]}")
    if failures:
        print("\n".join(failures))
        if not args.report:
            sys.exit(1)


if __name__ == "__main__":
    main()
