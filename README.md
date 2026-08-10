# Quazi Standard Library (`std`)

Welcome to the standard library for the **Quazi** programming language!

This repository contains the core modules, abstractions, and platform-specific bindings that provide essential functionality for Quazi programs.

## Modules Overview

- `core`: Platform-neutral intrinsics (I/O, memory management, process primitives).
- `collections`: Fallible, non-panicking `usize` map and set types.
- `fs`: File system operations.
- `io`: Standard input, output, and error streams handling.
- `net`: Networking and sockets.
- `os`: Operating system utilities and environment variables.
- `thread`: Threading and concurrency primitives.
- `unix` / `windows`: OS-specific platform bindings.

## Usage

This library is automatically linked by the Quazi compiler (`qz`) when building projects. By default, the compiler resolves imports starting with `std.` by looking in this directory (usually `~/.quazi/std/src`).

To import a module, simply use:
```quazi
import std.io;
import std.collections.Map;

fn main() i32 {
    io.println("Hello from Quazi!");
    ret 0;
}
```

## Contributing

The standard library is written entirely in Quazi and is closely tied to the compiler's internal intrinsics and type system. When adding new intrinsics or platform-specific syscalls, ensure that both `core.qz` and the corresponding compiler backend (e.g., `x86_64`) are updated simultaneously.

## C interoperability

`std.ffi` provides Linux x86-64 C ABI aliases (`c_int`, `c_long`, `c_size`,
`c_void`, and related types), typed `nullptr[T]()`, borrowed `CStr`, and owned
`CString`. Foreign calls remain explicit and unsafe:

```quazi
import std.ffi.*;

@api("puts")
unsafe fn puts(text: *c_char) c_int;

fn main() void {
    var text = CString.try_from(b"hello from Quazi").unwrap();
    unsafe { puts(text.as_ptr()); }
}
```

`CString.try_from(bytes)` rejects an embedded NUL and reports allocation failure,
then appends the C terminator. Local `CString` values use the compiler's existing
`free(self)` scope cleanup. `unsafe CString.from_unchecked(str)` is available for
legacy strings when the caller accepts their NUL-terminated representation.
`CStr.from_ptr` borrows a foreign pointer and is unsafe; it does not take
ownership. Borrowed UTF-8 validation remains explicit follow-up work rather than
an implicit conversion at the ABI boundary.

## I/O

Input returns owned, UTF-8-validated strings and makes failure explicit:

```quazi
import std.io;

fn main() i32 {
    var line: String = io.readln().unwrap();
    io.println("you entered: {}", line.as_str());
    ret 0;
}
```

`io.read`, `io.readln`, and `io.readkey` return
`Result[String, io.ReadError]`. File and socket byte writes take `bytes` and use
its exact stored length. Raw pointer reads/writes remain available as explicitly
`unsafe` operations.

## Collections

`Map` currently stores `usize -> usize`, and `Set` stores `usize`. Constructors
and insertion are fallible; lookup uses `Option` instead of exiting the process:

```quazi
import std.collections.Map;
import std.collections.MapError;

fn example() Result[usize, MapError] {
    var map: Map = Map.new()?;
    map = map.insert(7, 42)?;
    ret Ok(map.get(7).unwrap());
}
```

The deliberately concrete element types avoid unsound generic raw storage until
Quazi can express hash/equality bounds and drop-aware slots.
