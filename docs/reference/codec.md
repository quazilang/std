# `std.codec`

std.codec — typed serialization contracts built on JSON wire codecs.

## Contents

- [Functions](#functions)
- [`EncodeError`](#encodeerror) (enum)
- [`DecodeError`](#decodeerror) (enum)
- [`Serialize`](#serialize) (trait)
- [`bool`](#bool) (methods)
- [`i64`](#i64) (methods)
- [`str`](#str) (methods)
- [`String`](#string) (methods)
- [`SystemTime`](#systemtime) (methods)

## Functions

### `object`

```quazi
pub fn object(keys: Array[str], values: Array[String]) Result[String, EncodeError]
```

Compose a typed JSON object from ordered, already-encoded field values.
Compiler-generated Serialize implementations use this instead of exposing a
JsonError in their public Result type.

### `decode_bool_with_limits`

```quazi
pub fn decode_bool_with_limits(source: str, max_input: usize, max_depth: usize) Result[bool, DecodeError]
```

Decodes a JSON boolean, with input size and nesting limits.

### `decode_bool`

```quazi
pub fn decode_bool(source: str) Result[bool, DecodeError]
```

Decodes a JSON boolean.

### `decode_string_with_limits`

```quazi
pub fn decode_string_with_limits(source: str, max_input: usize, max_depth: usize) Result[String, DecodeError]
```

Decodes a JSON string, with input size and nesting limits.

### `decode_string`

```quazi
pub fn decode_string(source: str) Result[String, DecodeError]
```

Decodes a JSON string.

### `decode_i64_with_limits`

```quazi
pub fn decode_i64_with_limits(source: str, max_input: usize, max_depth: usize) Result[i64, DecodeError]
```

Decodes a JSON integer as `i64`, with input size and nesting limits.

### `decode_i64`

```quazi
pub fn decode_i64(source: str) Result[i64, DecodeError]
```

Decodes a JSON integer as `i64`.

### `decode_system_time`

```quazi
pub fn decode_system_time(source: str) Result[SystemTime, DecodeError]
```

Decode a JSON string holding an RFC 3339 timestamp (offsets are normalized
to UTC). Non-strings are TypeMismatch; malformed or out-of-range text is
InvalidValue.

## `EncodeError`

```quazi
pub enum EncodeError {
    UnsupportedType,
    OutputLimit,
    DepthLimit,
    InvalidValue,
}
```

Why a value could not be encoded.

### `EncodeError.message`

```quazi
pub fn message(self: EncodeError) str
```

A short English description of the error, for display.

## `DecodeError`

```quazi
pub enum DecodeError {
    InputLimit,
    DepthLimit,
    InvalidJson,
    TypeMismatch,
    MissingField,
    DuplicateField,
    UnknownField,
    InvalidValue,
}
```

Why decoding failed.

### `DecodeError.message`

```quazi
pub fn message(self: DecodeError) str
```

A short English description of the error, for display.

## `Serialize`

```quazi
pub trait Serialize {
    fn to_json(self: Self) Result[String, EncodeError];
}
```

Implementations must produce exactly one JSON value. Future compiler derives
implement this trait for supported non-generic structs.

## `bool`

### `bool.to_json`

```quazi
pub fn to_json(self: bool) Result[String, EncodeError]
```

The JSON text of the value.

## `i64`

### `i64.to_json`

```quazi
pub fn to_json(self: i64) Result[String, EncodeError]
```

The JSON text of the value.

## `str`

### `str.to_json`

```quazi
pub fn to_json(self: str) Result[String, EncodeError]
```

The JSON string literal of the text, with escapes.

## `String`

### `String.to_json`

```quazi
pub fn to_json(self: String) Result[String, EncodeError]
```

The JSON string literal of the text, with escapes.

## `SystemTime`

### `SystemTime.to_json`

```quazi
pub fn to_json(self: SystemTime) Result[String, EncodeError]
```

The time as a JSON string in RFC 3339 format.
