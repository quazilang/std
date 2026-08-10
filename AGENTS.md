# Standard-library FFI

`src/ffi.qz` owns the public low-level C interoperability vocabulary.

- C aliases describe the x86-64 SysV and Win64 data models while fixed-width
  Quazi types retain their usual meanings. `c_long`/`c_ulong` use `@cfg` because
  Windows is LLP64 and Linux/macOS are LP64.
- `c_float` and `c_double`, including aliases in `@repr(C)` fields and by-value
  aggregates, are lowered by portable QZI ABI metadata and classified separately
  by the SysV and Win64 backends.
- `nullptr[T]()` returns a typed raw null pointer and is unsafe.
- `CStr` is a borrowed raw pointer and never frees it. `from_ptr` and `as_ptr`
  are unsafe because lifetime, validity, and termination remain foreign contracts.
- `CString` owns an explicitly allocated NUL-terminated buffer. Construction is
  explicit and fallible; its `free(self)` method participates in the compiler's
  existing local scope cleanup through `std.core`.
- `CString.try_from(bytes)` rejects embedded NUL with its byte position and
  reports allocation failure. `unsafe CString.from_unchecked(str)` remains for
  legacy `str`, whose NUL-terminated representation cannot expose bytes after
  an embedded NUL.
- Planned work: borrowed UTF-8 validation, C-string literal ergonomics,
  ownership adapters, and safe wrappers around specific foreign APIs.

# Safety and API contracts

- Public APIs must not accept a safe raw pointer plus a caller-controlled byte
  count. Raw buffer operations are `unsafe`; safe byte operations derive their
  length from `bytes`, and safe text operations derive it from `strlen`.
- Low-level `std.unix` calls with caller-provided buffer lengths are explicitly
  `unsafe`; the declaration must match the module's documented syscall contract.
- `std.io.read`, `readln`, and `readkey` return `Result[String, ReadError]`.
  They own and free temporary allocations on every error, validate UTF-8, and
  return an owned `String`. EOF is represented by a successful empty string.
- `String.from_raw(data, len, cap)` is the unsafe ownership-transfer boundary:
  the allocation must be writable, NUL-terminated at `len`, and exclusively
  owned by the resulting `String`.
- Collections report allocation and capacity failures with `Result`; absence is
  represented with `Option`, never by terminating the process.
- Until the language has hash/equality/drop trait bounds for raw table slots,
  `Map` and `Set` intentionally store `usize` values rather than pretending to
  be sound generic containers.
- `std.fs.File` owns an operating-system handle. Its idempotent `free(self)`
  destructor closes the handle automatically at lexical scope exit, including
  early returns; callers should use `close()` only when they need an earlier,
  explicit release. Linux operations use syscalls and Windows operations use
  the pointer-correct internal `std.win32_core` bindings.
- `std.fs.read_to_string(path)` returns an owned `String`, closes its temporary
  `File` automatically, and reports open/read/allocation failures through
  `Result`. Cross-platform application code should prefer `std.fs` and
  `std.os` over importing `std.unix`, `std.windows`, or `std.win32_core`.
- `std.os.env`, `hostname`, `name`, `memory_total`, and `memory_available`
  provide owned or value-based cross-platform system information. Their Linux
  implementations use kernel state/syscalls; their Windows implementations use
  Win32 APIs. Neither contract requires libc or a shell.
