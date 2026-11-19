# `std.os`

std.os — operating system abstractions
Cross-platform: uses core intrinsics (void.*) where possible,
falls back to linux.* for Linux-specific calls.

## Contents

- [Functions](#functions)
- [`EnvError`](#enverror) (enum)

## Functions

### `args`

```quazi
pub fn args() Result[Array[String], fs.FsError]
```

Terminate the process with the given exit code. Never returns.
The process arguments, the program name first, as owned UTF-8 strings.
Linux reads /proc/self/cmdline; Windows splits GetCommandLineW like the C
runtime. An argument that is not valid UTF-8 reports InvalidData.

### `exit`

```quazi
pub fn exit(code: i32) void
```

Ends the process now with status `code`; destructors do not run.

### `sleep`

```quazi
pub fn sleep(ms: u64) void
```

Suspend execution for ms milliseconds.

### `yield_cpu`

```quazi
pub fn yield_cpu() void
```

Yield the CPU to other threads/processes.

### `getpid`

```quazi
pub fn getpid() i32
```

Returns the PID of the current process.

### `getppid`

```quazi
pub fn getppid() i32
```

Returns the PID of the parent process.

### `getenv`

```quazi
pub fn getenv(name: str) *u8
```

Returns a pointer to the value of environment variable name, or null if not set.
Result is a null-terminated C string pointer — treat as unsafe.

### `set_env`

```quazi
pub fn set_env(name: str, value: str) Result[bool, EnvError]
```

Sets environment variable `name` to `value` for this process and the
children it starts afterwards. Safe to call from several threads: on
Linux each change publishes a new environment copy (earlier copies stay
allocated, since another thread may be reading them).

### `remove_env`

```quazi
pub fn remove_env(name: str) Result[bool, EnvError]
```

Removes environment variable `name` from this process (and later
children): `Ok(true)` when it was set, `Ok(false)` when it was not.

### `env_present`

```quazi
pub fn env_present(name: str) bool
```

Whether environment variable `name` is set (even to an empty value).

### `env`

```quazi
pub fn env(name: str, fallback: str) String
```

Return an owned copy of an environment variable. Callers do not need to
manage the platform buffer or call free; String is destroyed automatically
at the end of its lexical lifetime.

### `name`

```quazi
pub fn name() str
```

Host operating-system name suitable for display and feature diagnostics.

### `version`

```quazi
pub fn version() String
```

Human-readable OS release. Windows uses authoritative registry build,
edition, and display-version values instead of compatibility-shimmed APIs.

### `cpu_name`

```quazi
pub fn cpu_name() String
```

CPU branding suitable for display. PROCESSOR_IDENTIFIER is only an
architecture identifier, so Windows reads ProcessorNameString instead.

### `shell`

```quazi
pub fn shell() String
```

Best-effort interactive shell and terminal names. Windows environment hints
are checked first, then the parent-process chain is inspected directly.

### `terminal`

```quazi
pub fn terminal() String
```

The terminal: `TERM` on Linux and NetBSD, the console host on Windows,
`unknown` when it cannot be detected.

### `hostname`

```quazi
pub fn hostname() String
```

Return the hostname as an owned UTF-8 string. The compiler-provided
intrinsic uses GetComputerNameA on Windows and uname(2) on Linux.

### `memory_total`

```quazi
pub fn memory_total() u64
```

Physical-memory counters in bytes. Linux availability includes reclaimable
memory through MemAvailable, falling back to sysinfo.free_ram without procfs.
Windows reports MEMORYSTATUSEX.available_physical.

### `memory_available`

```quazi
pub fn memory_available() u64
```

Memory in bytes that can be allocated without swapping (Linux
`MemAvailable`, Windows available physical memory).

### `current_dir`

```quazi
pub fn current_dir() Result[String, fs.FsError]
```

The current working directory as an owned path; see fs.current_dir.

### `set_current_dir`

```quazi
pub fn set_current_dir(path: str) Result[bool, fs.FsError]
```

Change the current working directory for the whole process.

## `EnvError`

```quazi
pub enum EnvError {
    // The name is empty or contains `=` or a NUL byte.
    InvalidName,
    // The value contains a NUL byte.
    InvalidValue,
    AllocationFailed,
    // A platform error code (NetBSD errno, Windows GetLastError).
    Native(i32),
}
```

Why an environment change was rejected.

### `EnvError.message`

```quazi
pub fn message(self: EnvError) str
```

A short English description of the error, for display.
