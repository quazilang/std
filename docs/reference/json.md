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

_Undocumented._

### `validate`

```quazi
pub fn validate(source: str) Result[bool, JsonError]
```

_Undocumented._

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

_Undocumented._

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

_Undocumented._

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

_Undocumented._

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
    ObjectLengthMismatch,
    OutputLimit,
}
```

_Undocumented._

### `JsonError.message`

```quazi
pub fn message(self: JsonError) str
```

_Undocumented._
