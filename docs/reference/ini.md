# `std.ini`

std.ini — deterministic, source-backed INI documents.

Blank lines and full-line `#`/`;` comments are ignored. Whitespace around
section names and keys is ignored; the first `=` splits a key/value pair;
later key definitions win; values retain their interior text. Parsing is
atomic: malformed input never replaces a previously valid document.

## Contents

- [`IniDocument`](#inidocument) (struct)
- [`IniError`](#inierror) (enum)
- [`IniDecodeError`](#inidecodeerror) (enum)

## `IniDocument`

```quazi
pub struct IniDocument { /* internal fields */ }
```

std.ini — deterministic, source-backed INI documents.

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
}
```

Errors produced while decoding a valid INI document into typed fields. The
compiler-generated `IniDecode` implementation never has to inspect source
text itself: it only composes these stable operations.
