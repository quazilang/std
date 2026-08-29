# Standard-library checkpoint resume

Audience: the next assistant continuing the coordinated runtime-`any` and
thread-safety checkpoint.

## Current change

`src/thread.qz` no longer accepts `any` function slots. It defines:

- Linux: `@repr(C) pub type ThreadCallback = fn(*u8) *u8`.
- Windows: `@repr(C) pub type ThreadCallback = fn(*u8) u32`.

`thread_spawn` and `Thread.spawn` accept `ThreadCallback`. Callbacks must be
signature-compatible exported functions; ordinary Quazi closures cannot cross
the native OS thread ABI. Same-module intrinsic calls currently use the
qualified `thread.thread_spawn` / `thread.thread_join` form because unqualified
calls from impl methods were rejected by current library scoping.

`AGENTS.md` records the callback contract. Preserve other STD changes.

## Verified smoke evidence

A temporary project under `/tmp/quazi-thread-project` compiled successfully as:

- Linux ELF relocatable object with `qz build -c`.
- Windows x86-64 COFF object with `qz build -c --target x86_64-windows`.

The built-in Linux linker correctly refused unresolved `pthread_create` and
`pthread_join`; external native library selection remains required. This was an
expected link limitation, not a compile failure.

## Current verified behavior

The coordinated compiler backend now returns zero when Linux allocation or
`pthread_create` fails, frees temporary storage after create failure, and only
returns the storage pointer on success. `thread_join(0)` is a no-op on both
targets, preventing a failed spawn wrapped by `Thread` from dereferencing null.
Focused backend tests cover the failure branches, cleanup relocation, and join
guard. Linux ELF and Windows COFF smoke objects build with the current compiler.

The high-level API remains experimental: `Thread.spawn` returns a `Thread`
containing handle zero instead of `Result[Thread, ThreadError]`. Typed creation
errors, panic/result propagation, synchronization, cancellation, and structured
cleanup need an explicit compatibility design rather than an ad hoc addition.

The reference-safety checkpoint also changed `std.random.choose` to consume an
`Array[T]`. The former `&Array[T]` implementation immediately dereferenced the
aggregate and created a shallow mutable alias, which the compiler now rejects.
`random_bytes` uses an explicit `Array[u8]` cast because zero-argument generic
associated constructors do not yet infer their struct type from the surrounding
annotation. `examples/29-guess-the-number` checks and builds with the current
compiler and STD.

Run `git diff --check` and inspect `git status --short` in this repository
independently from `quazistrap`.
