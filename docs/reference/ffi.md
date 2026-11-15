# `std.ffi`

std.ffi — x86-64 C ABI types and explicit C string helpers.

Fixed-width Quazi integers keep their normal meaning. These aliases document
that a value crosses the C ABI. Platform-width differences are selected at
source compilation; the resulting QZI still carries target-neutral ABI data.

## Contents

- [Functions](#functions)
- [`c_char`](#c_char) (type alias)
- [`c_schar`](#c_schar) (type alias)
- [`c_uchar`](#c_uchar) (type alias)
- [`c_short`](#c_short) (type alias)
- [`c_ushort`](#c_ushort) (type alias)
- [`c_int`](#c_int) (type alias)
- [`c_uint`](#c_uint) (type alias)
- [`c_long`](#c_long) (type alias)
- [`c_ulong`](#c_ulong) (type alias)
- [`c_long_long`](#c_long_long) (type alias)
- [`c_ulong_long`](#c_ulong_long) (type alias)
- [`c_float`](#c_float) (type alias)
- [`c_double`](#c_double) (type alias)
- [`c_size`](#c_size) (type alias)
- [`c_ssize`](#c_ssize) (type alias)
- [`c_ptrdiff`](#c_ptrdiff) (type alias)
- [`c_intptr`](#c_intptr) (type alias)
- [`c_uintptr`](#c_uintptr) (type alias)
- [`c_bool`](#c_bool) (type alias)
- [`c_void`](#c_void) (type alias)
- [`va_list`](#va_list) (struct)
- [`CStr`](#cstr) (struct)
- [`CString`](#cstring) (struct)
- [`CStringError`](#cstringerror) (enum)

## Functions

### `nullptr`

```quazi
pub fn nullptr[T]() *T
```

Typed raw null pointer. It is deliberately a function rather than a magical
polymorphic constant. Calling it is unsafe because raw-pointer values are
confined to Quazi's unsafe system.

## `c_char`

```quazi
pub type c_char = i8;
```

_Undocumented._

## `c_schar`

```quazi
pub type c_schar = i8;
```

_Undocumented._

## `c_uchar`

```quazi
pub type c_uchar = u8;
```

_Undocumented._

## `c_short`

```quazi
pub type c_short = i16;
```

_Undocumented._

## `c_ushort`

```quazi
pub type c_ushort = u16;
```

_Undocumented._

## `c_int`

```quazi
pub type c_int = i32;
```

_Undocumented._

## `c_uint`

```quazi
pub type c_uint = u32;
```

_Undocumented._

## `c_long`

```quazi
pub type c_long = i64;
```

_Undocumented._

## `c_ulong`

```quazi
pub type c_ulong = u64;
```

_Undocumented._

## `c_long_long`

```quazi
pub type c_long_long = i64;
```

_Undocumented._

## `c_ulong_long`

```quazi
pub type c_ulong_long = u64;
```

_Undocumented._

## `c_float`

```quazi
pub type c_float = f32;
```

_Undocumented._

## `c_double`

```quazi
pub type c_double = f64;
```

_Undocumented._

## `c_size`

```quazi
pub type c_size = usize;
```

_Undocumented._

## `c_ssize`

```quazi
pub type c_ssize = isize;
```

_Undocumented._

## `c_ptrdiff`

```quazi
pub type c_ptrdiff = isize;
```

_Undocumented._

## `c_intptr`

```quazi
pub type c_intptr = isize;
```

_Undocumented._

## `c_uintptr`

```quazi
pub type c_uintptr = usize;
```

_Undocumented._

## `c_bool`

```quazi
pub type c_bool = bool;
```

_Undocumented._

## `c_void`

```quazi
pub type c_void = void;
```

_Undocumented._

## `va_list`

```quazi
pub struct va_list {}
```

Opaque struct representing a C variadic argument list.
Quazi will not marshal va_list internally; this is for ABI documentation.

## `CStr`

```quazi
pub struct CStr { /* internal fields */ }
```

Borrowed view over a NUL-terminated C string. It never frees `ptr`; the
foreign API that supplied the pointer controls its lifetime.

### `CStr.from_ptr`

```quazi
pub fn from_ptr(ptr: *c_char) CStr
```

_Undocumented._

### `CStr.as_ptr`

```quazi
pub fn as_ptr(self: &CStr) *c_char
```

_Undocumented._

## `CString`

```quazi
pub struct CString { /* internal fields */ }
```

Owned NUL-terminated byte buffer. `from` makes an explicit allocation so an
FFI call never hides allocation or pointer lifetime rules.

### `CString.try_from`

```quazi
pub fn try_from(value: bytes) Result[CString, CStringError]
```

Checked construction from exact bytes. Embedded NUL bytes are rejected
because C APIs would otherwise observe a silently truncated string.

### `CString.try_from_str`

```quazi
pub fn try_from_str(value: str) Result[CString, CStringError]
```

Checked construction from UTF-8 text. Unlike from_unchecked, this keeps
the stored byte length and rejects embedded NUL bytes.

### `CString.from_unchecked`

```quazi
pub fn from_unchecked(text: str) CString
```

Legacy str has no stored byte length, so embedded NUL cannot be detected.
Keep this constructor explicit and unsafe rather than claiming it is checked.

### `CString.as_ptr`

```quazi
pub fn as_ptr(self: &CString) *c_char
```

_Undocumented._

### `CString.len`

```quazi
pub fn len(self: &CString) usize
```

_Undocumented._

### `CString.as_c_str`

```quazi
pub fn as_c_str(self: &CString) CStr
```

_Undocumented._

### `CString.clear`

```quazi
pub fn clear(self: &CString!) void
```

Release the allocation while retaining an empty, reusable owner.

### `CString.free`

```quazi
pub fn free(self: CString) void
```

_Undocumented._

## `CStringError`

```quazi
pub enum CStringError {
    InteriorNul(usize),
    AllocationFailed,
}
```

_Undocumented._
