# `std.ini`

std.ini — deterministic, source-backed INI documents.

## Contents

- [Functions](#functions)
- [`IniDocument`](#inidocument) (struct)
- [`IniError`](#inierror) (enum)
- [`IniDecodeError`](#inidecodeerror) (enum)
- [`IniValue`](#inivalue) (trait)
- [`IniSerialize`](#iniserialize) (trait)
- [`IniDeserialize`](#inideserialize) (trait)
- [`IniWriter`](#iniwriter) (struct)

## Functions

### `read`

```quazi
pub fn read[T: IniValue](document: &IniDocument, section: str, key: str) Result[T, IniDecodeError]
```

The value of `key` in `section` as `T`; MissingValue or InvalidValue.

### `read_optional`

```quazi
pub fn read_optional[T: IniValue](document: &IniDocument, section: str, key: str) Result[Option[T], IniDecodeError]
```

The value of `key` in `section` as `T`, or `None` when the key is absent.

## `IniDocument`

```quazi
pub struct IniDocument { /* internal fields */ }
```

An INI document and the file it came from, if any.
Blank lines and full-line `#`/`;` comments are ignored. Whitespace around
section names and keys is ignored; the first `=` splits a key/value pair;
later key definitions win; values retain their interior text. Parsing is
atomic: malformed input never replaces a previously valid document.

### `IniDocument.new`

```quazi
pub fn new() IniDocument
```

An empty document.

### `IniDocument.parse`

```quazi
pub fn parse(content: str) Result[IniDocument, IniDecodeError]
```

A document parsed from INI text (`[section]` headers and `key = value`
lines; `#` and `;` start comments).

### `IniDocument.get`

```quazi
pub fn get(self: &IniDocument, section: str, key: str) Option[String]
```

The value of `key` in `section`, or `None`.

### `IniDocument.contains`

```quazi
pub fn contains(self: &IniDocument, section: str, key: str) bool
```

Whether `section` has `key`.

### `IniDocument.has_section`

```quazi
pub fn has_section(self: &IniDocument, section: str) bool
```

Whether the document has `section`.

### `IniDocument.free`

```quazi
pub fn free(self: IniDocument) void
```

Frees the document; called automatically at the end of scope.

### `IniDocument.parse_string`

```quazi
pub fn parse_string(self: &IniDocument!, content: str) Result[bool, IniError]
```

Replaces the contents with the parsed `content`; on error the previous
contents stay.

### `IniDocument.stringify`

```quazi
pub fn stringify(self: &IniDocument) String
```

The document as INI text.

### `IniDocument.load`

```quazi
pub fn load(path: str) Result[IniDocument, IniDecodeError]
```

The document stored in the file at `path` (D-026).

### `IniDocument.decode`

```quazi
pub fn decode[T: IniDeserialize](self: &IniDocument) Result[T, IniDecodeError]
```

The whole document decoded as `T` (keys before any section are `T`'s
scalar fields; a nested struct field reads the section of its key).

### `IniDocument.encode`

```quazi
pub fn encode[T: IniSerialize](self: &IniDocument!, value: T) Result[bool, IniDecodeError]
```

Replace the document with the INI form of `value`.

### `IniDocument.save`

```quazi
pub fn save(self: &IniDocument) Result[bool, IniDecodeError]
```

Write the document back to the file it was loaded from.

### `IniDocument.save_as`

```quazi
pub fn save_as(self: &IniDocument, path: str) Result[bool, IniDecodeError]
```

Write the document to `path`.

### `IniDocument.require_string`

```quazi
pub fn require_string(self: &IniDocument, section: str, key: str) Result[String, IniDecodeError]
```

The value of `key` in `section`, or `MissingValue(section, key)`.

### `IniDocument.require_i32`

```quazi
pub fn require_i32(self: &IniDocument, section: str, key: str) Result[i32, IniDecodeError]
```

The value of `key` parsed as `i32`.

### `IniDocument.require_u64`

```quazi
pub fn require_u64(self: &IniDocument, section: str, key: str) Result[u64, IniDecodeError]
```

The value of `key` parsed as `u64`.

### `IniDocument.require_bool`

```quazi
pub fn require_bool(self: &IniDocument, section: str, key: str) Result[bool, IniDecodeError]
```

The value of `key` parsed as `true`/`false`.

## `IniError`

```quazi
pub enum IniError {
    EmptySection(usize),
    InvalidSection(usize),
    MissingSeparator(usize),
    EmptyKey(usize),
}
```

Why INI text could not be parsed.

## `IniDecodeError`

```quazi
pub enum IniDecodeError {
    Syntax(IniError),
    MissingValue(String, String),
    InvalidValue(String, String),
    // Reading or writing a document file failed.
    Io(String),
    // A value to encode contains a line break, which INI cannot hold.
    MultilineValue(String),
}
```

Errors produced while decoding a valid INI document into typed fields. The
compiler-generated `IniDecode` implementation never has to inspect source
text itself: it only composes these stable operations.

## `IniValue`

```quazi
pub trait IniValue {
    fn ini_text(self: Self) String;
    @associated fn from_ini_text(text: str) Option[Self];
}
```

A scalar stored as one INI value: integers, floats, `bool` and `String`.

## `IniSerialize`

```quazi
pub trait IniSerialize {
    fn to_ini_writer(self: Self) IniWriter;
}
```

A struct written as INI: its scalar fields as `key = value` lines and its
struct fields as `[key]` sections (`@serde("ini")` generates it).

## `IniDeserialize`

```quazi
pub trait IniDeserialize {
    @associated fn from_ini_section(document: &IniDocument, section: str) Result[Self, IniDecodeError];
}
```

A struct read from one section of an INI document (`""` is the part
before the first section header).

## `IniWriter`

```quazi
pub struct IniWriter { /* internal fields */ }
```

Collects the lines of one struct (used by generated `to_ini_writer`).

### `IniWriter.new`

```quazi
pub fn new() IniWriter
```

An empty writer.

### `IniWriter.entry`

```quazi
pub fn entry[T: IniValue](self: &IniWriter!, key: str, value: T) void
```

Write `key = value`.

### `IniWriter.optional`

```quazi
pub fn optional[T: IniValue](self: &IniWriter!, key: str, value: Option[T]) void
```

Write `key = value` for `Some`, nothing for `None`.

### `IniWriter.section`

```quazi
pub fn section[T: IniSerialize](self: &IniWriter!, name: str, value: T) void
```

Write `value` as the section `[name]`.

### `IniWriter.finish`

```quazi
pub fn finish(self: &IniWriter) Result[String, IniDecodeError]
```

The INI text: entries, then sections.
