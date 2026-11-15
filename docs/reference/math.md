# `std.math`

Portable dependency-free f64 mathematics.

These routines are implemented in Quazi, so importing std.math never pulls
in libc or libm. Trigonometric inputs and outputs use radians.

## Contents

- [Constants](#constants)
- [Functions](#functions)
- [`f64`](#f64) (methods)

## Constants

### `PI`

```quazi
pub const PI: f64 = 3.14159265358979323846;
```

Archimedes' constant (the ratio of a circle's circumference to its
diameter).

### `TAU`

```quazi
pub const TAU: f64 = 6.28318530717958647692;
```

2 * PI, a full turn in radians.

### `FRAC_PI_2`

```quazi
pub const FRAC_PI_2: f64 = 1.57079632679489661923;
```

PI / 2, a quarter turn in radians.

### `E`

```quazi
pub const E: f64 = 2.71828182845904523536;
```

Euler's number, the base of natural logarithms.

### `LN_2`

```quazi
pub const LN_2: f64 = 0.693147180559945309417;
```

The natural logarithm of 2.

### `LN_10`

```quazi
pub const LN_10: f64 = 2.30258509299404568402;
```

The natural logarithm of 10.

### `SQRT_2`

```quazi
pub const SQRT_2: f64 = 1.41421356237309504880;
```

The square root of 2.

## Functions

### `gcd`

```quazi
pub fn gcd(a: i64, b: i64) i64
```

The greatest common divisor (non-negative); panics when the result does
not fit `i64`.

### `lcm`

```quazi
pub fn lcm(a: i64, b: i64) i64
```

The least common multiple; 0 when either operand is 0; panics on overflow.

### `factorial`

```quazi
pub fn factorial(value: u32) u64
```

`value!`; panics when the result does not fit `u64`.

### `permutations`

```quazi
pub fn permutations(n: u32, r: u32) u64
```

The number of ordered selections of `r` from `n`; 0 when `r > n`;
panics on overflow.

### `combinations`

```quazi
pub fn combinations(n: u32, r: u32) u64
```

The number of unordered selections of `r` from `n`; 0 when `r > n`;
exact for every result that fits `u64`.

### `abs`

```quazi
pub fn abs(value: f64) f64
```

The absolute value; `-0.0` becomes `0.0`.

### `min`

```quazi
pub fn min(a: f64, b: f64) f64
```

The smaller value (a NaN operand yields the other).

### `max`

```quazi
pub fn max(a: f64, b: f64) f64
```

The larger value (a NaN operand yields the other).

### `clamp`

```quazi
pub fn clamp(value: f64, low: f64, high: f64) f64
```

The value limited to `low..=high`.

### `trunc`

```quazi
pub fn trunc(value: f64) f64
```

Clears the fraction bits below the units place; keeps the sign of zero.

### `floor`

```quazi
pub fn floor(value: f64) f64
```

The largest integer value not greater than the value.

### `ceil`

```quazi
pub fn ceil(value: f64) f64
```

The smallest integer value not less than the value.

### `round`

```quazi
pub fn round(value: f64) f64
```

Halves round away from zero. `value - whole` is exact, so values just below
a half (0.49999999999999994) are not pushed over it.

### `fract`

```quazi
pub fn fract(value: f64) f64
```

The fractional part: `value - trunc(value)`.

### `sign`

```quazi
pub fn sign(value: f64) f64
```

1.0 for positive values, -1.0 for negative values, the value itself for
zeros and NaN.

### `lerp`

```quazi
pub fn lerp(start: f64, end: f64, amount: f64) f64
```

Linear interpolation: `start + (end - start) * amount` (amount is not
limited to 0..=1).

### `map_range`

```quazi
pub fn map_range(value: f64, from_low: f64, from_high: f64,
    to_low: f64, to_high: f64) f64
```

Maps `value` from the range `from_low..from_high` to `to_low..to_high`.

### `radians`

```quazi
pub fn radians(degrees: f64) f64
```

Degrees converted to radians.

### `degrees`

```quazi
pub fn degrees(radians: f64) f64
```

Radians converted to degrees.

### `sqrt`

```quazi
pub fn sqrt(value: f64) f64
```

Correctly rounded (sqrtsd); NaN below zero, -0.0 stays -0.0.

### `cbrt`

```quazi
pub fn cbrt(value: f64) f64
```

The cube root; keeps the sign.

### `hypot`

```quazi
pub fn hypot(x: f64, y: f64) f64
```

`sqrt(x*x + y*y)` without avoidable overflow; infinity if either input is
infinite.

### `sin`

```quazi
pub fn sin(value: f64) f64
```

The sine of an angle in radians.

### `cos`

```quazi
pub fn cos(value: f64) f64
```

The cosine of an angle in radians.

### `tan`

```quazi
pub fn tan(value: f64) f64
```

The tangent of an angle in radians.

### `atan`

```quazi
pub fn atan(value: f64) f64
```

The arctangent in radians, in -pi/2..=pi/2.

### `arctan`

```quazi
pub fn arctan(value: f64) f64
```

Same as `atan`.

### `atan2`

```quazi
pub fn atan2(y: f64, x: f64) f64
```

The angle in radians of the point (x, y), in -pi..=pi (C99 rules for
zeros and infinities).

### `arctan2`

```quazi
pub fn arctan2(y: f64, x: f64) f64
```

Same as `atan2`.

### `asin`

```quazi
pub fn asin(value: f64) f64
```

The arcsine in radians; NaN outside -1..=1.

### `acos`

```quazi
pub fn acos(value: f64) f64
```

Near |v| = 1, pi/2 - asin(v) cancels; the half-angle forms keep the digits.

### `exp`

```quazi
pub fn exp(value: f64) f64
```

e raised to the value.

### `ln`

```quazi
pub fn ln(value: f64) f64
```

The natural logarithm; -infinity at 0, NaN for negative values.

### `log2`

```quazi
pub fn log2(value: f64) f64
```

The base-2 logarithm.

### `log10`

```quazi
pub fn log10(value: f64) f64
```

The base-10 logarithm.

### `sinh`

```quazi
pub fn sinh(value: f64) f64
```

The hyperbolic sine.

### `cosh`

```quazi
pub fn cosh(value: f64) f64
```

The hyperbolic cosine.

### `tanh`

```quazi
pub fn tanh(value: f64) f64
```

The hyperbolic tangent.

### `pow`

```quazi
pub fn pow(base: f64, exponent: f64) f64
```

`base` raised to `exponent`; a negative base needs an integral exponent
(otherwise NaN).

## `f64`

### `f64.trunc`

```quazi
pub fn trunc(self: f64) f64
```

The value with its fraction removed (toward zero).

### `f64.floor`

```quazi
pub fn floor(self: f64) f64
```

The largest integer value not greater than the value.

### `f64.ceil`

```quazi
pub fn ceil(self: f64) f64
```

The smallest integer value not less than the value.

### `f64.round`

```quazi
pub fn round(self: f64) f64
```

The nearest integer value; halves round away from zero.

### `f64.fract`

```quazi
pub fn fract(self: f64) f64
```

The fractional part: `value - trunc(value)`.

### `f64.sign`

```quazi
pub fn sign(self: f64) f64
```

1.0 for positive values, -1.0 for negative values, the value itself for
zeros and NaN.

### `f64.sqrt`

```quazi
pub fn sqrt(self: f64) f64
```

The square root (correctly rounded); NaN for negative values.

### `f64.cbrt`

```quazi
pub fn cbrt(self: f64) f64
```

The cube root; keeps the sign.

### `f64.sin`

```quazi
pub fn sin(self: f64) f64
```

The sine of an angle in radians.

### `f64.cos`

```quazi
pub fn cos(self: f64) f64
```

The cosine of an angle in radians.

### `f64.tan`

```quazi
pub fn tan(self: f64) f64
```

The tangent of an angle in radians.

### `f64.atan`

```quazi
pub fn atan(self: f64) f64
```

The arctangent in radians, in -pi/2..=pi/2.

### `f64.arctan`

```quazi
pub fn arctan(self: f64) f64
```

Same as `atan`.

### `f64.atan2`

```quazi
pub fn atan2(self: f64, x: f64) f64
```

The angle in radians of the point (x, self), in -pi..=pi.

### `f64.arctan2`

```quazi
pub fn arctan2(self: f64, x: f64) f64
```

Same as `atan2`.

### `f64.asin`

```quazi
pub fn asin(self: f64) f64
```

The arcsine in radians; NaN outside -1..=1.

### `f64.acos`

```quazi
pub fn acos(self: f64) f64
```

The arccosine in radians; NaN outside -1..=1.

### `f64.exp`

```quazi
pub fn exp(self: f64) f64
```

e raised to the value.

### `f64.ln`

```quazi
pub fn ln(self: f64) f64
```

The natural logarithm; -infinity at 0, NaN for negative values.

### `f64.log2`

```quazi
pub fn log2(self: f64) f64
```

The base-2 logarithm.

### `f64.log10`

```quazi
pub fn log10(self: f64) f64
```

The base-10 logarithm.

### `f64.sinh`

```quazi
pub fn sinh(self: f64) f64
```

The hyperbolic sine.

### `f64.cosh`

```quazi
pub fn cosh(self: f64) f64
```

The hyperbolic cosine.

### `f64.tanh`

```quazi
pub fn tanh(self: f64) f64
```

The hyperbolic tangent.

### `f64.degrees`

```quazi
pub fn degrees(self: f64) f64
```

Radians converted to degrees.

### `f64.radians`

```quazi
pub fn radians(self: f64) f64
```

Degrees converted to radians.

### `f64.pow`

```quazi
pub fn pow(self: f64, exponent: f64) f64
```

The value raised to `exponent` (see `math.pow`).
