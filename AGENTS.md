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
