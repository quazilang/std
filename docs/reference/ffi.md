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

The C type `char`.

## `c_schar`

```quazi
pub type c_schar = i8;
```

The C type `signed char`.

## `c_uchar`

```quazi
pub type c_uchar = u8;
```

The C type `unsigned char`.

## `c_short`

```quazi
pub type c_short = i16;
```

The C type `short`.

## `c_ushort`

```quazi
pub type c_ushort = u16;
```

The C type `unsigned short`.

## `c_int`

```quazi
pub type c_int = i32;
```

The C type `int`.

## `c_uint`

```quazi
pub type c_uint = u32;
```

The C type `unsigned int`.

## `c_long`

```quazi
pub type c_long = i64;
```

The C type `long (64-bit on Linux/NetBSD x86_64; Windows `long` is 32-bit, use `c_int`)`.

## `c_ulong`

```quazi
pub type c_ulong = u64;
```

The C type `unsigned long (see `c_long`)`.

## `c_long_long`

```quazi
pub type c_long_long = i64;
```

The C type `long long`.

## `c_ulong_long`

```quazi
pub type c_ulong_long = u64;
```

The C type `unsigned long long`.

## `c_float`

```quazi
pub type c_float = f32;
```

The C type `float`.

## `c_double`

```quazi
pub type c_double = f64;
```

The C type `double`.

## `c_size`

```quazi
pub type c_size = usize;
```

The C type `size_t`.

## `c_ssize`

```quazi
pub type c_ssize = isize;
```

The C type `ssize_t`.

## `c_ptrdiff`

```quazi
pub type c_ptrdiff = isize;
```

The C type `ptrdiff_t`.

## `c_intptr`

```quazi
pub type c_intptr = isize;
```

The C type `intptr_t`.

## `c_uintptr`

```quazi
pub type c_uintptr = usize;
```

The C type `uintptr_t`.

## `c_bool`

```quazi
pub type c_bool = bool;
```

The C type `_Bool`.

## `c_void`

```quazi
pub type c_void = void;
```

The C type `void`.

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

A view of the NUL-terminated C string at `ptr` (not copied, not freed).

### `CStr.as_ptr`

```quazi
pub fn as_ptr(self: &CStr) *c_char
```

The pointer to the first character.

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

The pointer to the NUL-terminated copy, valid while the CString lives.

### `CString.len`

```quazi
pub fn len(self: &CString) usize
```

The length in bytes without the terminating NUL.

### `CString.as_c_str`

```quazi
pub fn as_c_str(self: &CString) CStr
```

A borrowed `CStr` view.

### `CString.clear`

```quazi
pub fn clear(self: &CString!) void
```

Release the allocation while retaining an empty, reusable owner.

### `CString.free`

```quazi
pub fn free(self: CString) void
```

Frees the copy; called automatically at the end of scope.

## `CStringError`

```quazi
pub enum CStringError {
    InteriorNul(usize),
    AllocationFailed,
}
```

Why text could not become a C string (an interior NUL byte, or no
memory).
