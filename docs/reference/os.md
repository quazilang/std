# `std.os`

std.os — operating system abstractions
Cross-platform: uses core intrinsics (void.*) where possible,
falls back to unix.* for Linux-specific calls.

## Contents

- [Functions](#functions)

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

_Undocumented._

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

_Undocumented._

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

_Undocumented._

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

### `cwd`

```quazi
pub fn cwd(buf: str, size: usize) isize
```

Fill buf with the current working directory path (null-terminated).
Returns number of bytes written (including null) or negative on error.
buf must be at least size bytes long.

### `getuid`

```quazi
pub fn getuid() u32
```

Returns the user ID of the current process.

### `getgid`

```quazi
pub fn getgid() u32
```

Returns the group ID of the current process.

### `geteuid`

```quazi
pub fn geteuid() u32
```

Returns the effective user ID.

### `getegid`

```quazi
pub fn getegid() u32
```

Returns the effective group ID.

### `kill`

```quazi
pub fn kill(pid: i32, sig: i32) i32
```

Send signal sig to process pid. Common signals: SIGTERM=15, SIGKILL=9, SIGINT=2.

### `umask`

```quazi
pub fn umask(mask: u32) u32
```

Set process file-creation mask. Returns previous mask.
