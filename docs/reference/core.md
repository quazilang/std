# `std.core`

std.core — platform-neutral intrinsics
Import this for cross-platform I/O, memory, and process primitives.
These lower to the appropriate syscall/Win32/libc call per target at AOT time.
@no_std disables automatic std availability.

UTF-8 contract:
  str / &str / String are ALWAYS valid UTF-8.
  Do NOT pass arbitrary bytes through str — use *u8 or [u8; N] for raw data.

## Contents

- [Functions](#functions)

## Functions

### `write`

```quazi
pub fn write(fd: i32, buf: str, count: usize) isize
```

Raw text write. Unsafe because `count` may exceed the readable string bytes.

### `write_bytes`

```quazi
pub fn write_bytes(fd: i32, buf: *u8, count: usize) isize
```

Write raw bytes to fd. Unsafe — buf may contain non-UTF-8 bytes.

### `read`

```quazi
pub fn read(fd: i32, buf: *u8, count: usize) isize
```

Read raw bytes from fd into buf. Unsafe — caller must validate UTF-8 if converting to str.

### `stderr_write`

```quazi
pub fn stderr_write(buf: str, len: usize) isize
```

_Undocumented._

### `exit`

```quazi
pub fn exit(code: i32) i32
```

_Undocumented._

### `sleep_ms`

```quazi
pub fn sleep_ms(ms: u64) void
```

_Undocumented._

### `process_spawn`

```quazi
pub fn process_spawn(program: str, args: *str, args_len: usize, handle_out: *usize, error_out: *i32) i32
```

Private child-process runtime ABI. These operations use only scalar
out-pointers so the compiler runtime never depends on an Array layout.
A zero return is success; -1 leaves the platform error in `error_out`.

### `process_wait`

```quazi
pub fn process_wait(handle: usize, kind_out: *i32, value_out: *i32, error_out: *i32) i32
```

_Undocumented._

### `process_try_wait`

```quazi
pub fn process_try_wait(handle: usize, exited_out: *i32, kind_out: *i32, value_out: *i32, error_out: *i32) i32
```

_Undocumented._

### `process_terminate`

```quazi
pub fn process_terminate(handle: usize, error_out: *i32) i32
```

_Undocumented._

### `process_close`

```quazi
pub fn process_close(handle: usize, error_out: *i32) i32
```

_Undocumented._

### `getenv`

```quazi
pub fn getenv(name: str) *u8
```

Returns pointer to null-terminated C string, or null on not found.

### `hostname`

```quazi
pub fn hostname(buf: *u8, capacity: usize) isize
```

Fill `buf` with the platform hostname and return its byte length. Returns -1
when the buffer is empty/too small or the operating-system query fails.

### `memory_total`

```quazi
pub fn memory_total() u64
```

Cross-platform physical-memory totals in bytes. A return value of zero means
the host query failed.

### `memory_available`

```quazi
pub fn memory_available() u64
```

_Undocumented._

### `cpu_name`

```quazi
pub fn cpu_name(buf: *u8, capacity: usize) isize
```

Fill `buf` with the processor's CPUID brand string and return its byte
length, or -1 when the CPU does not expose a brand or the buffer is too small.

### `windows_build`

```quazi
pub fn windows_build() u32
```

Windows release metadata. Non-Windows targets return zero.

### `windows_product`

```quazi
pub fn windows_product() u32
```

_Undocumented._

### `malloc`

```quazi
pub fn malloc(size: usize) *u8
```

Returns pointer to allocated heap block, or null on failure.

### `free`

```quazi
pub fn free(ptr: *u8) void
```

_Undocumented._

### `realloc`

```quazi
pub fn realloc(ptr: *u8, size: usize) *u8
```

Returns pointer to resized block (may differ from ptr), or null on failure.

### `memcpy`

```quazi
pub fn memcpy(dst: *u8, src: *u8, n: usize) *u8
```

_Undocumented._

### `memset`

```quazi
pub fn memset(ptr: *u8, val: i32, n: usize) *u8
```

_Undocumented._

### `memmove`

```quazi
pub fn memmove(dst: *u8, src: *u8, n: usize) *u8
```

_Undocumented._

### `memcmp`

```quazi
pub fn memcmp(a: *u8, b: *u8, n: usize) i32
```

_Undocumented._

### `strlen`

```quazi
pub fn strlen(s: str) usize
```

Returns byte length of null-terminated C string. str is valid UTF-8 here.

### `str_concat`

```quazi
pub fn str_concat(s1: str, s2: str) String
```

Owned text results. Their buffers and compiler-owned headers are destroyed
through String; callers never adopt raw formatter allocations themselves.

### `int_to_str`

```quazi
pub fn int_to_str(n: i64) String
```

_Undocumented._

### `float_to_str`

```quazi
pub fn float_to_str(f: f64) String
```

_Undocumented._

### `atomic_add`

```quazi
pub fn atomic_add(target: *i64, delta: i64) i64
```

Sequentially consistent atomic read-modify-write on an 8-byte aligned i64.
`atomic_add` returns the previous value; `atomic_cas` stores `desired` only
if the current value equals `expected` and returns the value it observed.

### `atomic_cas`

```quazi
pub fn atomic_cas(target: *i64, expected: i64, desired: i64) i64
```

_Undocumented._

### `context_switch`

```quazi
pub fn context_switch(save: *u8, restore: *u8) void
```

Save the current execution context into `save` (272 bytes) and resume the
one stored in `restore`. Building block for green threads; see the backend
AGENTS notes for the context layout. Misuse corrupts the stack.

### `str_byte_at`

```quazi
pub fn str_byte_at(s: str, i: usize) u8
```

Return the byte at index i in s (no bounds check — caller ensures i < strlen(s)).

### `str_from_byte`

```quazi
pub fn str_from_byte(b: u8) String
```

A single non-ASCII byte is not valid UTF-8. NUL preserves the legacy
null-terminated empty-text result; use bytes for arbitrary binary data.

### `str_as_ptr`

```quazi
pub fn str_as_ptr(s: str) *u8
```

Borrow the address of immutable UTF-8 text for pointer-correct native API
calls. The pointer is valid only as long as `s` remains alive and must never
be freed or written through.

### `str_from_ptr`

```quazi
pub fn str_from_ptr(ptr: *u8) str
```

Representation-only view of a NUL-terminated pointer after the caller has
established that the bytes are valid UTF-8. The returned str is borrowed.

### `is_valid_utf8`

```quazi
pub fn is_valid_utf8(buf: *u8, len: usize) bool
```

Validate arbitrary bytes before promoting them to String ownership. This is
unsafe because the caller must supply a readable buffer of exactly `len`.

### `utf8_incomplete_tail`

```quazi
pub fn utf8_incomplete_tail(buf: *u8, len: usize) usize
```

Return how many continuation bytes a final, otherwise valid UTF-8 prefix
still needs. A zero result means either complete input or a malformed tail;
callers must run is_valid_utf8 after filling a non-zero tail.
