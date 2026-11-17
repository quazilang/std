# `std.codec`

std.codec — typed serialization contracts built on JSON wire codecs.

## Contents

- [Functions](#functions)
- [`EncodeError`](#encodeerror) (enum)
- [`DecodeError`](#decodeerror) (enum)
- [`Serialize`](#serialize) (trait)
- [`bool`](#bool) (methods)
- [`i64`](#i64) (methods)
- [`i8`](#i8) (methods)
- [`i16`](#i16) (methods)
- [`i32`](#i32) (methods)
- [`u8`](#u8) (methods)
- [`u16`](#u16) (methods)
- [`u32`](#u32) (methods)
- [`u64`](#u64) (methods)
- [`isize`](#isize) (methods)
- [`usize`](#usize) (methods)
- [`f32`](#f32) (methods)
- [`f64`](#f64) (methods)
- [`str`](#str) (methods)
- [`String`](#string) (methods)
- [`SystemTime`](#systemtime) (methods)

## Functions

### `optional_json`

```quazi
pub fn optional_json[T: Serialize](value: Option[T]) Result[String, EncodeError]
```

`null` for None, the value's JSON otherwise (derived `Option` fields).

### `array_json`

```quazi
pub fn array_json[T: Serialize](values: Array[T]) Result[String, EncodeError]
```

A JSON array of the values' JSON, in order (derived `Array` fields).

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

### `object_fields`

```quazi
pub fn object_fields(source: str, keys: &Array[str]) Result[Array[usize], DecodeError]
```

The value ranges of the expected `keys` of the JSON object `source` (see
`json.object_fields`).

### `field_bool`

```quazi
pub fn field_bool(source: str, spans: &Array[usize], index: usize) Result[bool, DecodeError]
```

A required boolean field.

### `field_i64`

```quazi
pub fn field_i64(source: str, spans: &Array[usize], index: usize) Result[i64, DecodeError]
```

A required `i64` field.

### `field_string`

```quazi
pub fn field_string(source: str, spans: &Array[usize], index: usize) Result[String, DecodeError]
```

A required string field.

### `optional_bool`

```quazi
pub fn optional_bool(source: str, spans: &Array[usize], index: usize) Result[Option[bool], DecodeError]
```

An optional boolean field.

### `optional_i64`

```quazi
pub fn optional_i64(source: str, spans: &Array[usize], index: usize) Result[Option[i64], DecodeError]
```

An optional `i64` field.

### `optional_string`

```quazi
pub fn optional_string(source: str, spans: &Array[usize], index: usize) Result[Option[String], DecodeError]
```

An optional string field.

### `field_raw`

```quazi
pub fn field_raw(source: str, spans: &Array[usize], index: usize) Result[String, DecodeError]
```

The raw JSON value of a required field (derived nested structs decode it).

### `decode_u64`

```quazi
pub fn decode_u64(source: str) Result[u64, DecodeError]
```

Decodes a JSON non-negative integer as `u64`.

### `decode_f64`

```quazi
pub fn decode_f64(source: str) Result[f64, DecodeError]
```

Decodes a JSON number as `f64`.

### `decode_i8`

```quazi
pub fn decode_i8(source: str) Result[i8, DecodeError]
```

Decodes a JSON integer as `i8`; one outside its range is InvalidValue.

### `decode_i16`

```quazi
pub fn decode_i16(source: str) Result[i16, DecodeError]
```

Decodes a JSON integer as `i16`; one outside its range is InvalidValue.

### `decode_i32`

```quazi
pub fn decode_i32(source: str) Result[i32, DecodeError]
```

Decodes a JSON integer as `i32`; one outside its range is InvalidValue.

### `decode_u8`

```quazi
pub fn decode_u8(source: str) Result[u8, DecodeError]
```

Decodes a JSON integer as `u8`; one outside its range is InvalidValue.

### `decode_u16`

```quazi
pub fn decode_u16(source: str) Result[u16, DecodeError]
```

Decodes a JSON integer as `u16`; one outside its range is InvalidValue.

### `decode_u32`

```quazi
pub fn decode_u32(source: str) Result[u32, DecodeError]
```

Decodes a JSON integer as `u32`; one outside its range is InvalidValue.

### `decode_isize`

```quazi
pub fn decode_isize(source: str) Result[isize, DecodeError]
```

Decodes a JSON integer as `isize` (64-bit targets).

### `decode_usize`

```quazi
pub fn decode_usize(source: str) Result[usize, DecodeError]
```

Decodes a JSON non-negative integer as `usize` (64-bit targets).

### `decode_f32`

```quazi
pub fn decode_f32(source: str) Result[f32, DecodeError]
```

Decodes a JSON number as `f32`.

### `optional_raw`

```quazi
pub fn optional_raw(source: str, spans: &Array[usize], index: usize) Result[Option[String], DecodeError]
```

The raw JSON value of an optional field: `None` when missing or `null`.

### `array_items`

```quazi
pub fn array_items(source: str) Result[Array[String], DecodeError]
```

The raw JSON text of each element of the array `source`, in order
(derived `Array` fields decode each element by its type).

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

## `i8`

### `i8.to_json`

```quazi
pub fn to_json(self: i8) Result[String, EncodeError]
```

The JSON number of the value.

## `i16`

### `i16.to_json`

```quazi
pub fn to_json(self: i16) Result[String, EncodeError]
```

The JSON number of the value.

## `i32`

### `i32.to_json`

```quazi
pub fn to_json(self: i32) Result[String, EncodeError]
```

The JSON number of the value.

## `u8`

### `u8.to_json`

```quazi
pub fn to_json(self: u8) Result[String, EncodeError]
```

The JSON number of the value.

## `u16`

### `u16.to_json`

```quazi
pub fn to_json(self: u16) Result[String, EncodeError]
```

The JSON number of the value.

## `u32`

### `u32.to_json`

```quazi
pub fn to_json(self: u32) Result[String, EncodeError]
```

The JSON number of the value.

## `u64`

### `u64.to_json`

```quazi
pub fn to_json(self: u64) Result[String, EncodeError]
```

The JSON number of the value.

## `isize`

### `isize.to_json`

```quazi
pub fn to_json(self: isize) Result[String, EncodeError]
```

The JSON number of the value.

## `usize`

### `usize.to_json`

```quazi
pub fn to_json(self: usize) Result[String, EncodeError]
```

The JSON number of the value.

## `f32`

### `f32.to_json`

```quazi
pub fn to_json(self: f32) Result[String, EncodeError]
```

The shortest JSON number that decodes back to the value; NaN and
infinities have no JSON form.

## `f64`

### `f64.to_json`

```quazi
pub fn to_json(self: f64) Result[String, EncodeError]
```

The shortest JSON number that decodes back to the value; NaN and
infinities have no JSON form.

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
