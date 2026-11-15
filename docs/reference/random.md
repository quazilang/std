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

A uniformly random `u64` from the operating system's secure generator.

### `next_u32`

```quazi
pub fn next_u32() Result[u32, RandomError]
```

A uniformly random `u32`.

### `next_u8`

```quazi
pub fn next_u8() Result[u8, RandomError]
```

A uniformly random `u8`.

### `next_i64`

```quazi
pub fn next_i64() Result[i64, RandomError]
```

A uniformly random `i64`.

### `next_i32`

```quazi
pub fn next_i32() Result[i32, RandomError]
```

A uniformly random `i32`.

### `boolean`

```quazi
pub fn boolean() Result[bool, RandomError]
```

`true` or `false` with equal probability.

### `float`

```quazi
pub fn float() Result[f64, RandomError]
```

Uniform f64 in [0.0, 1.0), using 53 random mantissa bits.

### `chance`

```quazi
pub fn chance(probability: f64) Result[bool, RandomError]
```

`true` with the given probability (0.0..=1.0); `InvalidProbability`
otherwise.

### `range`

```quazi
pub fn range(bounds: Range) Result[i64, RandomError]
```

Uniform integer from an exclusive (`a..b`) or inclusive (`a..=b`) Range.

### `choose`

```quazi
pub fn choose[T](items: Array[T]) Result[T, RandomError]
```

One element of `items`, chosen uniformly; `EmptyCollection` for an empty
array.

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

`count` secure random bytes.

## `RandomError`

```quazi
pub enum RandomError {
    Unavailable,
    InvalidRange,
    EmptyCollection,
    InvalidProbability,
}
```

Why random generation failed.

### `RandomError.message`

```quazi
pub fn message(self: RandomError) str
```

A short English description of the error, for display.
