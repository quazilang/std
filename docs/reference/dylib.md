# `std.dylib`

std.dylib — explicit runtime loading of native shared libraries.
Symbols are untyped addresses. Cast them to an @repr(C) callback only inside
unsafe code, while this DynamicLibrary remains open.

## Contents

- [`DynamicLibraryError`](#dynamiclibraryerror) (enum)
- [`DynamicLibrary`](#dynamiclibrary) (struct)

## `DynamicLibraryError`

```quazi
pub enum DynamicLibraryError {
    InvalidName(usize),
    AllocationFailed,
    OpenFailed,
    SymbolNotFound,
    Native(i32),
}
```

_Undocumented._

### `DynamicLibraryError.message`

```quazi
pub fn message(self: DynamicLibraryError) str
```

_Undocumented._

## `DynamicLibrary`

```quazi
pub struct DynamicLibrary { /* internal fields */ }
```

_Undocumented._

### `DynamicLibrary.open`

```quazi
pub fn open(path: str) Result[DynamicLibrary, DynamicLibraryError]
```

_Undocumented._

### `DynamicLibrary.symbol`

```quazi
pub fn symbol(self: &DynamicLibrary, name: str) Result[usize, DynamicLibraryError]
```

Address stays valid only while the library remains open. Cast to an
exact @repr(C) callback signature before invoking it.

### `DynamicLibrary.close`

```quazi
pub fn close(self: DynamicLibrary) Result[bool, DynamicLibraryError]
```

_Undocumented._

### `DynamicLibrary.free`

```quazi
pub fn free(self: DynamicLibrary) void
```

_Undocumented._

### `DynamicLibrary.raw_handle`

```quazi
pub fn raw_handle(self: &DynamicLibrary) usize
```

_Undocumented._
