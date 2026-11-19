# Quazi Standard Library (`std`)

Welcome to the standard library for the **Quazi** programming language!

This repository contains the core modules, abstractions, and platform-specific bindings that provide essential functionality for Quazi programs.

**Plan completion: 92.7%.**

**Remaining work: 7.3%.**

Completion of unfinished plan items:

| Plan item | Implemented requirements | Complete | Remaining |
| --- | --- | --- | --- |
| Filesystem / I/O | 15/16 | 93.8% | 6.2% |
| Operating-system APIs | 9/10 | 90.0% | 10.0% |
| Processes | 15/16 | 93.8% | 6.2% |
| Networking / TLS | 16/17 | 94.1% | 5.9% |
| Mathematics | 11/11 | 100.0% | 0.0% |
| Panic handling | 9/10 | 90.0% | 10.0% |
| Concurrency | 10/12 | 83.3% | 16.7% |
| Time | 19/19 | 100.0% | 0.0% |
| Serialization | 14/15 | 93.3% | 6.7% |
| Library-wide safety / other modules | 8/9 | 88.9% | 11.1% |

Counted on 2026-11-19 from the [requirement checklist](docs/PLAN_PROGRESS.md).
Each item has equal weight; its percentage is implemented requirements
divided by listed requirements. The overall percentage averages those
fractions before rounding. Pending or failing requirements receive no
credit. These figures measure checklist coverage, not remaining effort
or production readiness.

On Linux, `qz test` passes all 101 standard-library tests, including the
TCP and UDP cases that need local sockets. `scripts/check_tls.py` runs the
TLS client against a local TLS server (trusted and untrusted certificates,
wrong host name, truncation).

## Modules Overview

Every public function, type and method is listed with its signature and
description in the generated [API reference](docs/reference/README.md)
(`qz doc -o docs/reference`; `scripts/check_reference.py` keeps it current).

- `core`: Platform-neutral intrinsics (I/O, memory, process, and system information).
- `collections`: Fallible, non-panicking `usize` `Map`/`Set` and generic `HashMap`/`HashSet` (`K: Hash + Eq`).
- `fs`: Cross-platform owned files, whole-file reads, directory listing (`read_dir` returns `Array[DirEntry]`), `Path` methods (`is_dir`, `read_dir`, ...), and metadata operations.
- `io`: Standard input, output, and error streams handling.
- `stream`: `Reader`/`Writer` byte streams with `IoError`, `copy`, and `BufReader`/`BufWriter` adapters.
- `path`: Lexical `Path` manipulation (join, parent, names, extensions, normalize).
- `json`: Bounded JSON syntax validation and safe JSON string-token encoding.
- `math`: Lightweight dependency-free `f64` roots, trigonometry, logarithms, and powers.
- `random`: Secure values, integer ranges, collection choice/shuffling, and random bytes.
- `net`: Networking and sockets.
- `tls`: TLS client streams and HTTPS over the system TLS library (Linux).
- `os`: Cross-platform host, memory, process, and environment information and changes.
- `posix`: Unix-specific identities, signals, umask, and raw cwd (Linux, NetBSD).
- `process`: Child processes; `Command` builder with PATH lookup, working directory, environment, and captured output (Linux, Windows).
- `thread`: Threading and concurrency primitives.
- `time` / `timezone`: Durations, clocks, civil time, RFC 3339, and named IANA time zones (TZif, POSIX TZ rules).
- `linux` / `netbsd` / `windows`: OS-specific platform bindings (`posix` is the shared Unix layer).

Application code should normally use `std.fs` and `std.os`. Their Linux paths
use direct syscalls and their Windows paths use Win32 handles/APIs, without
shelling out or requiring libc. The low-level platform modules are intended for
implementing facilities that the portable surface does not yet expose.

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

On Windows, stdout/stderr connected to a console are converted from UTF-8 to
UTF-16 and written with `WriteConsoleW`; redirected files and pipes retain UTF-8
bytes. This makes Unicode output independent of the active Windows code page.

## Mathematics

`std.math` provides integer `gcd`, `lcm`, factorial, permutation, and
combination helpers. Its floating-point surface includes rounding,
interpolation, degree/radian conversion, square/cube roots, `hypot`,
trigonometric and hyperbolic functions, exponentials, logarithms, and powers.
Angles use radians unless explicitly converted. The routines are written in
pure Quazi and do not link libc or libm; they are lightweight approximations
rather than correctly rounded scientific-library replacements.

## Filesystem and system information

`std.fs.File` is an owning value. A successfully opened handle closes
automatically when its lexical scope ends or returns early; `close()` is only
needed when the handle must be released before then. Whole-file reads return an
owned string:

```quazi
import std.fs;
import std.os;

fn describe() Result[String, fs.FsError] {
    const hostname: String = os.hostname();
    const text: String = fs.read_to_string("system.txt")?;
    ret Ok(text);
}
```

Portable system queries include `os.env`, `os.name`, `os.hostname`,
`os.version`, `os.cpu_name`, `os.shell`, `os.terminal`, `os.memory_total`, and
`os.memory_available`. `fs.read_dir` lists immediate non-dot directory
entries (`fs.read_dir(path)?.len()` counts them) with `getdents64`, NetBSD
`readdir` or Win32 enumeration handles. On Linux these APIs are
backed by kernel state and syscalls; on Windows they use CPUID, shared kernel
release data, process snapshots, and Win32. They do not execute shell commands
and do not require callers to manually free returned `String` values.

## Collections

`HashMap[K, V]` and `HashSet[K]` own their entries. Keys implement
`Hash + Eq`, insertion returns a storage error when growth fails, and
`HashMap.find` gives an index for borrowed key and value access.

`Map` currently stores `usize -> usize`, and `Set` stores `usize`. Constructors
and insertion are fallible; lookup uses `Option` instead of exiting the process:

```quazi
import std.collections.Map;
import std.collections.MapError;

fn example() Result[usize, MapError] {
    var map: Map = Map.new()?;
    map.insert(7, 42)?;
    ret Ok(map.get(7).unwrap());
}
```

`Map` and `Set` keep concrete `usize` elements; generic keys and values use
`HashMap[K, V]` and `HashSet[K]`, which require `K: Hash + Eq` and own their
entries in drop-aware storage.

## JSON

`std.json` currently provides a bounded syntax gate for untrusted JSON, helpers
for emitting scalar JSON tokens, bounded JSON-string decoding, and top-level
object-field and array-element extraction. `std.codec` provides bounded
decoders for `bool`, every integer width, `f32`, `f64`, and owned `String`, and
the helpers behind compiler-derived `Serialize`/`Deserialize` (scalar,
`String`, nested struct, `Option`, and `Array` fields). Derived enums use
externally tagged JSON (`"Unit"`, `{"Variant": payload}`) with optional
`@serde` keys per variant (`"name"`, `"*:name"`, `"json:name"`; В27Б). Neither module constructs a dynamic JSON tree;
maps remain future serialization work.

```quazi
import std.json;

fn main() i32 {
    const name: String = json.quote("Ada\\nLovelace");
    if (json.validate_with_limits(name.as_str(), 1024, 8).is_err()) {
        ret 1;
    }
    ret 0;
}
```

`validate_with_limits(source, max_input, max_depth)` rejects oversized input,
excessive array/object nesting, malformed strings/numbers, and trailing data.
`quote` accepts valid Quazi UTF-8 text and returns exactly one JSON string
token, escaping quotes, backslashes, and control characters. `boolean` emits
`true` or `false`; `null` emits `null`.

Use `std.codec` when decoding the supported scalar surface:

```quazi
import std.codec;

fn main() i32 {
    const enabled: bool = codec.decode_bool("true").unwrap();
    const count: i64 = codec.decode_i64("42").unwrap();
    const name: String = codec.decode_string("\"Ada\"").unwrap();
    if (!enabled || count != 42 || name.as_str() != "Ada") { ret 1; }
    ret 0;
}
```
