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
    // The library could not be loaded: the system error code on Windows
    // (GetLastError), 0 where the loader reports none (dlopen).
    OpenFailed(i32),
    SymbolNotFound,
    Native(i32),
}
```

Why a shared library could not be loaded or used.

### `DynamicLibraryError.message`

```quazi
pub fn message(self: DynamicLibraryError) str
```

A short English description of the error, for display.

## `DynamicLibrary`

```quazi
pub struct DynamicLibrary { /* internal fields */ }
```

A loaded shared library (`.so`/`.dll`); unloaded at the end of scope.

### `DynamicLibrary.open`

```quazi
pub fn open(path: str) Result[DynamicLibrary, DynamicLibraryError]
```

Loads the shared library at `path`.

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

Unloads the library now.

### `DynamicLibrary.free`

```quazi
pub fn free(self: DynamicLibrary) void
```

Unloads the library; called automatically at the end of scope.

### `DynamicLibrary.raw_handle`

```quazi
pub fn raw_handle(self: &DynamicLibrary) usize
```

The native library handle.
