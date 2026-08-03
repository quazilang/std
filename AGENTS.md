# Standard-library FFI

`src/ffi.qz` owns the public low-level C interoperability vocabulary.

- C aliases describe the Linux x86-64 ABI while fixed-width Quazi types retain
  their usual meanings. Update aliases when adding another target data model.
- `nullptr[T]()` returns a typed raw null pointer and is unsafe.
- `CStr` is a borrowed raw pointer and never frees it. `from_ptr` and `as_ptr`
  are unsafe because lifetime, validity, and termination remain foreign contracts.
- `CString` owns an explicitly allocated NUL-terminated buffer. `from(str)` does
  not hide allocation at an FFI call site; its `free(self)` method participates
  in the compiler's existing local scope cleanup through `std.core`.
- Current `CString.from` relies on the existing NUL-terminated Quazi `str`
  representation and does not diagnose embedded NUL. Add checked construction
  together with byte strings/UTF-8 result APIs rather than silently changing it.
- Planned work: `b"..."`/raw byte literals, checked embedded-NUL conversion,
  borrowed UTF-8 validation, C-string literal ergonomics, ownership adapters,
  and safe wrappers around specific foreign APIs.
