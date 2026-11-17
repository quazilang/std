# `std.json`

std.json — bounded validation primitives for JSON text.
This initial module deliberately validates syntax without constructing a
dynamic value tree; typed decoding is supplied by derived codecs later.

## Contents

- [Functions](#functions)
- [`JsonError`](#jsonerror) (enum)

## Functions

### `validate_with_limits`

```quazi
pub fn validate_with_limits(source: str, max_input: usize, max_depth: usize) Result[bool, JsonError]
```

Checks that `source` is valid JSON no longer than `max_input` bytes and
no deeper than `max_depth`.

### `validate`

```quazi
pub fn validate(source: str) Result[bool, JsonError]
```

Checks that `source` is valid JSON (default size and depth limits).

### `quote`

```quazi
pub fn quote(value: str) String
```

Encode a valid UTF-8 string as one JSON string token. Non-ASCII scalars are
emitted directly; JSON is defined over Unicode and the input str invariant
ensures their byte boundaries are safe to preserve.

### `boolean`

```quazi
pub fn boolean(value: bool) str
```

The JSON text of `value` (`true` or `false`).

### `null`

```quazi
pub fn null() str
```

Return the JSON null literal without allocating an owned string.

### `object`

```quazi
pub fn object(keys: Array[str], values: Array[String]) Result[String, JsonError]
```

Compose a JSON object from ordered keys and already-encoded JSON values.
Keys are always escaped as JSON strings; values must each contain exactly one
valid JSON value. The output preserves the supplied order, so callers can
use it for deterministic wire formats.

### `object_with_limits`

```quazi
pub fn object_with_limits(keys: Array[str], values: Array[String], max_output: usize, max_depth: usize) Result[String, JsonError]
```

Compose a JSON object with an explicit total-output and nesting policy.
It rejects mismatched or duplicate keys and validates each raw value before
appending it. The output cap includes punctuation and escaped keys.

### `decode_string_with_limits`

```quazi
pub fn decode_string_with_limits(source: str, max_input: usize, max_depth: usize) Result[String, JsonError]
```

Decode exactly one JSON string token after validating its syntax and limits.

### `decode_string`

```quazi
pub fn decode_string(source: str) Result[String, JsonError]
```

The text of a JSON string literal, with escapes decoded.

### `object_field_with_limits`

```quazi
pub fn object_field_with_limits(source: str, key: str, max_input: usize, max_depth: usize) Result[Option[String], JsonError]
```

Return the raw JSON value for one object key. The returned token is validated
JSON and can be passed to a typed scalar decoder. Duplicate matching keys are
rejected instead of selecting an implementation-defined winner.

### `object_field`

```quazi
pub fn object_field(source: str, key: str) Result[Option[String], JsonError]
```

The raw JSON text of field `key` in the object `source`, or `None` when
the object has no such field.

### `object_fields_with_limits`

```quazi
pub fn object_fields_with_limits(source: str, keys: &Array[str], max_input: usize, max_depth: usize) Result[Array[usize], JsonError]
```

Where each expected key's value lies in the object `source`: entries
`2 * i` and `2 * i + 1` are the byte range of `keys[i]`'s raw JSON value,
both zero when the object does not contain the key. A key outside `keys`
is `UnknownKey` and a repeated key is `DuplicateKey` (maintainer answer
В19В: an error rather than silence).

### `object_fields`

```quazi
pub fn object_fields(source: str, keys: &Array[str]) Result[Array[usize], JsonError]
```

`object_fields_with_limits` with the default limits (1 MiB, depth 64).

### `array_items_with_limits`

```quazi
pub fn array_items_with_limits(source: str, max_input: usize, max_depth: usize) Result[Array[usize], JsonError]
```

Where each element of the array `source` lies: entries `2 * i` and
`2 * i + 1` are the byte range of element `i`'s raw JSON value. A valid
value that is not an array is `InvalidToken`.

### `array_items`

```quazi
pub fn array_items(source: str) Result[Array[usize], JsonError]
```

`array_items_with_limits` with the default limits (1 MiB, depth 64).

## `JsonError`

```quazi
pub enum JsonError {
    InputLimit,
    DepthLimit,
    UnexpectedEnd,
    InvalidToken,
    InvalidString,
    InvalidEscape,
    InvalidNumber,
    TrailingData,
    DuplicateKey,
    UnknownKey,
    ObjectLengthMismatch,
    OutputLimit,
}
```

Why JSON validation or decoding failed.

### `JsonError.message`

```quazi
pub fn message(self: JsonError) str
```

A short English description of the error, for display.
