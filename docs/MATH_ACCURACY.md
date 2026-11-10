# std.math accuracy

Audience: library users and maintainers.

`scripts/check_math_accuracy.py --qz <qz>` builds a probe program, evaluates
each function on seeded random inputs (400 per function; `sin`/`cos`/`tan`
also on 200 inputs from 1e6 to 1e300 and on 399 multiples of pi/2), plus inputs
that defeated earlier versions and compares the IEEE-754 results with the host C
library through Python's `math` (itself within about 1 ULP). It also checks
the special-value contract and fails when a function exceeds its bound.

Measured maximum error on 2026-11-10 (the enforced bound adds one ULP of
slack for the reference):

| Function | Domain sampled | Max error (ULP) |
| --- | --- | --- |
| sqrt | 1e-300..1e300 | 0 (correctly rounded `sqrtsd`) |
| cbrt | 1e-300..1e300 | 2 |
| sin, cos, tan | -10..10, -1e5..1e5, 1e6..1e300, multiples of pi/2 | 1 |
| atan, atan2 | -1e3..1e3; -10..10 | 1 |
| asin, acos | -1..1 | 2, 1 |
| exp | -700..700 | 3 |
| ln, log2, log10 | 1e-300..1e300 | 1, 2, 3 |
| sinh, cosh, tanh | -20..20, -10..10 | 5, 4, 2 |
| hypot | 1e-150..1e150 | 1 |
| pow | base 0.1..100 with exponent -10..10; negative bases with integral exponents; results near overflow; bases next to 1 with large exponents | 3 |
| floor, ceil, round, trunc | -1e6..1e6 | 0 (exact) |

Range reduction for `sin`/`cos`/`tan` follows fdlibm: a three-step
Cody-Waite reduction with low-part tails below 2^20 * pi/2 and Payne-Hanek
reduction with 2/pi to 1584 bits above, so results stay within 1 ULP over the
whole finite range. `sinh`/`cosh` stay finite up to |x| = 710.47 and `cbrt`
covers the full range including subnormals and DBL_MAX.
`pow` carries ln(x) and y * ln(x) as double-doubles (Veltkamp/Dekker
products, no FMA), so its error stays near `exp`'s instead of growing with
|y * ln(x)|.

Special values checked: NaN propagation, `sqrt(-1)`/`ln(-1)`/`asin(2)` are
NaN, signed zeros (`sqrt(-0.0)`, `trunc(-0.0)`, `ceil(-0.5)` keep `-0.0`),
infinities (`exp(inf)`, `exp(-inf)`, `atan(inf)`, `tanh(±inf)`,
`hypot(inf, NaN)`), overflow (`exp(1000)`), `pow` corner cases, halves
rounding away from zero, subnormal `sqrt` and exact cube roots.
