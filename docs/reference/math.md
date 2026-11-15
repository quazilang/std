# `std.math`

Portable dependency-free f64 mathematics.

These routines are implemented in Quazi, so importing std.math never pulls
in libc or libm. Trigonometric inputs and outputs use radians.

## Contents

- [Functions](#functions)
- [`f64`](#f64) (methods)

## Functions

### `gcd`

```quazi
pub fn gcd(a: i64, b: i64) i64
```

_Undocumented._

### `lcm`

```quazi
pub fn lcm(a: i64, b: i64) i64
```

_Undocumented._

### `factorial`

```quazi
pub fn factorial(value: u32) u64
```

_Undocumented._

### `permutations`

```quazi
pub fn permutations(n: u32, r: u32) u64
```

_Undocumented._

### `combinations`

```quazi
pub fn combinations(n: u32, r: u32) u64
```

_Undocumented._

### `abs`

```quazi
pub fn abs(value: f64) f64
```

_Undocumented._

### `min`

```quazi
pub fn min(a: f64, b: f64) f64
```

_Undocumented._

### `max`

```quazi
pub fn max(a: f64, b: f64) f64
```

_Undocumented._

### `clamp`

```quazi
pub fn clamp(value: f64, low: f64, high: f64) f64
```

_Undocumented._

### `trunc`

```quazi
pub fn trunc(value: f64) f64
```

Clears the fraction bits below the units place; keeps the sign of zero.

### `floor`

```quazi
pub fn floor(value: f64) f64
```

_Undocumented._

### `ceil`

```quazi
pub fn ceil(value: f64) f64
```

_Undocumented._

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

_Undocumented._

### `sign`

```quazi
pub fn sign(value: f64) f64
```

_Undocumented._

### `lerp`

```quazi
pub fn lerp(start: f64, end: f64, amount: f64) f64
```

_Undocumented._

### `map_range`

```quazi
pub fn map_range(value: f64, from_low: f64, from_high: f64,
    to_low: f64, to_high: f64) f64
```

_Undocumented._

### `radians`

```quazi
pub fn radians(degrees: f64) f64
```

_Undocumented._

### `degrees`

```quazi
pub fn degrees(radians: f64) f64
```

_Undocumented._

### `sqrt`

```quazi
pub fn sqrt(value: f64) f64
```

Correctly rounded (sqrtsd); NaN below zero, -0.0 stays -0.0.

### `cbrt`

```quazi
pub fn cbrt(value: f64) f64
```

_Undocumented._

### `hypot`

```quazi
pub fn hypot(x: f64, y: f64) f64
```

_Undocumented._

### `sin`

```quazi
pub fn sin(value: f64) f64
```

_Undocumented._

### `cos`

```quazi
pub fn cos(value: f64) f64
```

_Undocumented._

### `tan`

```quazi
pub fn tan(value: f64) f64
```

_Undocumented._

### `atan`

```quazi
pub fn atan(value: f64) f64
```

_Undocumented._

### `arctan`

```quazi
pub fn arctan(value: f64) f64
```

_Undocumented._

### `atan2`

```quazi
pub fn atan2(y: f64, x: f64) f64
```

_Undocumented._

### `arctan2`

```quazi
pub fn arctan2(y: f64, x: f64) f64
```

_Undocumented._

### `asin`

```quazi
pub fn asin(value: f64) f64
```

_Undocumented._

### `acos`

```quazi
pub fn acos(value: f64) f64
```

Near |v| = 1, pi/2 - asin(v) cancels; the half-angle forms keep the digits.

### `exp`

```quazi
pub fn exp(value: f64) f64
```

_Undocumented._

### `ln`

```quazi
pub fn ln(value: f64) f64
```

_Undocumented._

### `log2`

```quazi
pub fn log2(value: f64) f64
```

_Undocumented._

### `log10`

```quazi
pub fn log10(value: f64) f64
```

_Undocumented._

### `sinh`

```quazi
pub fn sinh(value: f64) f64
```

_Undocumented._

### `cosh`

```quazi
pub fn cosh(value: f64) f64
```

_Undocumented._

### `tanh`

```quazi
pub fn tanh(value: f64) f64
```

_Undocumented._

### `pow`

```quazi
pub fn pow(base: f64, exponent: f64) f64
```

_Undocumented._

## `f64`

### `f64.trunc`

```quazi
pub fn trunc(self: f64) f64
```

_Undocumented._

### `f64.floor`

```quazi
pub fn floor(self: f64) f64
```

_Undocumented._

### `f64.ceil`

```quazi
pub fn ceil(self: f64) f64
```

_Undocumented._

### `f64.round`

```quazi
pub fn round(self: f64) f64
```

_Undocumented._

### `f64.fract`

```quazi
pub fn fract(self: f64) f64
```

_Undocumented._

### `f64.sign`

```quazi
pub fn sign(self: f64) f64
```

_Undocumented._

### `f64.sqrt`

```quazi
pub fn sqrt(self: f64) f64
```

_Undocumented._

### `f64.cbrt`

```quazi
pub fn cbrt(self: f64) f64
```

_Undocumented._

### `f64.sin`

```quazi
pub fn sin(self: f64) f64
```

_Undocumented._

### `f64.cos`

```quazi
pub fn cos(self: f64) f64
```

_Undocumented._

### `f64.tan`

```quazi
pub fn tan(self: f64) f64
```

_Undocumented._

### `f64.atan`

```quazi
pub fn atan(self: f64) f64
```

_Undocumented._

### `f64.arctan`

```quazi
pub fn arctan(self: f64) f64
```

_Undocumented._

### `f64.atan2`

```quazi
pub fn atan2(self: f64, x: f64) f64
```

_Undocumented._

### `f64.arctan2`

```quazi
pub fn arctan2(self: f64, x: f64) f64
```

_Undocumented._

### `f64.asin`

```quazi
pub fn asin(self: f64) f64
```

_Undocumented._

### `f64.acos`

```quazi
pub fn acos(self: f64) f64
```

_Undocumented._

### `f64.exp`

```quazi
pub fn exp(self: f64) f64
```

_Undocumented._

### `f64.ln`

```quazi
pub fn ln(self: f64) f64
```

_Undocumented._

### `f64.log2`

```quazi
pub fn log2(self: f64) f64
```

_Undocumented._

### `f64.log10`

```quazi
pub fn log10(self: f64) f64
```

_Undocumented._

### `f64.sinh`

```quazi
pub fn sinh(self: f64) f64
```

_Undocumented._

### `f64.cosh`

```quazi
pub fn cosh(self: f64) f64
```

_Undocumented._

### `f64.tanh`

```quazi
pub fn tanh(self: f64) f64
```

_Undocumented._

### `f64.degrees`

```quazi
pub fn degrees(self: f64) f64
```

_Undocumented._

### `f64.radians`

```quazi
pub fn radians(self: f64) f64
```

_Undocumented._

### `f64.pow`

```quazi
pub fn pow(self: f64, exponent: f64) f64
```

_Undocumented._
