# `std.random`

std.random — operating-system-backed secure random helpers.

The compiler lowers these private intrinsics to the host OS CSPRNG. Calls
fail explicitly when secure system entropy is unavailable. Range selection
uses rejection sampling, never modulo bias.

## Contents

- [Functions](#functions)
- [`RandomError`](#randomerror) (enum)

## Functions

### `next_u64`

```quazi
pub fn next_u64() Result[u64, RandomError]
```

_Undocumented._

### `next_u32`

```quazi
pub fn next_u32() Result[u32, RandomError]
```

_Undocumented._

### `next_u8`

```quazi
pub fn next_u8() Result[u8, RandomError]
```

_Undocumented._

### `next_i64`

```quazi
pub fn next_i64() Result[i64, RandomError]
```

_Undocumented._

### `next_i32`

```quazi
pub fn next_i32() Result[i32, RandomError]
```

_Undocumented._

### `boolean`

```quazi
pub fn boolean() Result[bool, RandomError]
```

_Undocumented._

### `float`

```quazi
pub fn float() Result[f64, RandomError]
```

Uniform f64 in [0.0, 1.0), using 53 random mantissa bits.

### `chance`

```quazi
pub fn chance(probability: f64) Result[bool, RandomError]
```

_Undocumented._

### `range`

```quazi
pub fn range(bounds: Range) Result[i64, RandomError]
```

Uniform integer from an exclusive (`a..b`) or inclusive (`a..=b`) Range.

### `choose`

```quazi
pub fn choose[T](items: Array[T]) Result[T, RandomError]
```

_Undocumented._

### `shuffle`

```quazi
pub fn shuffle[T](items: Array[T]) Result[Array[T], RandomError]
```

Fisher-Yates shuffle. Array storage is shared, so this mutates the supplied
collection and returns it for convenient chaining.

### `random_bytes`

```quazi
pub fn random_bytes(count: usize) Result[Array[u8], RandomError]
```

_Undocumented._

## `RandomError`

```quazi
pub enum RandomError {
    Unavailable,
    InvalidRange,
    EmptyCollection,
    InvalidProbability,
}
```

_Undocumented._

### `RandomError.message`

```quazi
pub fn message(self: RandomError) str
```

_Undocumented._
