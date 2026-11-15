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

_Undocumented._

### `IniDocument.parse`

```quazi
pub fn parse(content: str) Result[IniDocument, IniDecodeError]
```

_Undocumented._

### `IniDocument.get`

```quazi
pub fn get(self: &IniDocument, section: str, key: str) Option[String]
```

_Undocumented._

### `IniDocument.contains`

```quazi
pub fn contains(self: &IniDocument, section: str, key: str) bool
```

_Undocumented._

### `IniDocument.has_section`

```quazi
pub fn has_section(self: &IniDocument, section: str) bool
```

_Undocumented._

### `IniDocument.free`

```quazi
pub fn free(self: IniDocument) void
```

_Undocumented._

### `IniDocument.parse_string`

```quazi
pub fn parse_string(self: &IniDocument!, content: str) Result[bool, IniError]
```

_Undocumented._

### `IniDocument.stringify`

```quazi
pub fn stringify(self: &IniDocument) String
```

_Undocumented._

### `IniDocument.require_string`

```quazi
pub fn require_string(self: &IniDocument, section: str, key: str) Result[String, IniDecodeError]
```

_Undocumented._

### `IniDocument.require_i32`

```quazi
pub fn require_i32(self: &IniDocument, section: str, key: str) Result[i32, IniDecodeError]
```

_Undocumented._

### `IniDocument.require_u64`

```quazi
pub fn require_u64(self: &IniDocument, section: str, key: str) Result[u64, IniDecodeError]
```

_Undocumented._

### `IniDocument.require_bool`

```quazi
pub fn require_bool(self: &IniDocument, section: str, key: str) Result[bool, IniDecodeError]
```

_Undocumented._

## `IniError`

```quazi
pub enum IniError {
    EmptySection(usize),
    InvalidSection(usize),
    MissingSeparator(usize),
    EmptyKey(usize),
}
```

_Undocumented._

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
