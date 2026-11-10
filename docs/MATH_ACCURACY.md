# std.math accuracy

Audience: library users and maintainers.

`scripts/check_math_accuracy.py --qz <qz>` builds a probe program, evaluates
each function on seeded random inputs (400 per function; `sin`/`cos` also on
100 inputs up to 1e5) and compares the IEEE-754 results with the host C
library through Python's `math` (itself within about 1 ULP). It also checks
the special-value contract and fails when a function exceeds its bound.

Measured maximum error on 2026-11-10 (the enforced bound adds one ULP of
slack for the reference):

| Function | Domain sampled | Max error (ULP) |
| --- | --- | --- |
| sqrt | 1e-300..1e300 | 0 (correctly rounded `sqrtsd`) |
| cbrt | 1e-300..1e300 | 2 |
| sin, cos | -10..10 and -1e5..1e5 | 1 |
| tan | -1.5..1.5 | 2 |
| atan, atan2 | -1e3..1e3; -10..10 | 1 |
| asin, acos | -1..1 | 2, 1 |
| exp | -700..700 | 3 |
| ln, log2, log10 | 1e-300..1e300 | 1, 2, 3 |
| sinh, cosh, tanh | -20..20, -10..10 | 5, 4, 2 |
| hypot | 1e-150..1e150 | 1 |
| pow | base 0.1..100, exponent -10..10 | 43 |
| floor, ceil, round, trunc | -1e6..1e6 | 0 (exact) |

Range reduction for `sin`/`cos`/`tan` splits pi/2 in three parts and is exact
for |x| < 2^20 * pi/2 (about 1.6e6); accuracy degrades gradually beyond.
`pow` computes `exp(y * ln(x))` and its error grows with |y * ln(x)|.

Special values checked: NaN propagation, `sqrt(-1)`/`ln(-1)`/`asin(2)` are
NaN, signed zeros (`sqrt(-0.0)`, `trunc(-0.0)`, `ceil(-0.5)` keep `-0.0`),
infinities (`exp(inf)`, `exp(-inf)`, `atan(inf)`, `tanh(±inf)`,
`hypot(inf, NaN)`), overflow (`exp(1000)`), `pow` corner cases, halves
rounding away from zero, subnormal `sqrt` and exact cube roots.
