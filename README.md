# Quazi Standard Library (`std`)

Welcome to the standard library for the **Quazi** programming language!

This repository contains the core modules, abstractions, and platform-specific bindings that provide essential functionality for Quazi programs.

## Modules Overview

- `core`: Platform-neutral intrinsics (I/O, memory management, process primitives).
- `collections`: Core data structures (`map`, `set`, etc.).
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
import std.collections.map;

fn main() i32 {
    io.println("Hello from Quazi!");
    ret 0;
}
```

## Contributing

The standard library is written entirely in Quazi and is closely tied to the compiler's internal intrinsics and type system. When adding new intrinsics or platform-specific syscalls, ensure that both `core.qz` and the corresponding compiler backend (e.g., `x86_64`) are updated simultaneously.
