# `std.posix`

std.posix — Unix-specific process facilities (Linux and NetBSD).
These wrap native calls and return raw native results; std.os holds the
portable surface. On other targets the signed-result functions return -1
and the unsigned ones return u32::MAX as an unsupported-target sentinel.

## Contents

- [Functions](#functions)

## Functions

### `linux_environment`

```quazi
pub fn linux_environment() *u8
```

The current Linux environment: a null-terminated array of `NAME=VALUE`
C string pointers. Arrays are never freed, so it stays readable.

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

### `fork`

```quazi
pub fn fork() i32
```

Duplicate the process: the child's pid, 0 in the child, or -errno.

### `execve`

```quazi
pub fn execve(path: str, argv: *u8, envp: *u8) i32
```

Replace the process image; returns only on failure (-errno).

### `chdir`

```quazi
pub fn chdir(path: str) i32
```

Change the working directory (-errno on failure).

### `dup2`

```quazi
pub fn dup2(old: i32, new_fd: i32) i32
```

Make `new_fd` a copy of `old` (-errno on failure).

### `pipe`

```quazi
pub fn pipe(fds: *u8, cloexec: bool) i32
```

A pipe into `fds` (two i32); `cloexec` sets close-on-exec on both ends.

### `poll`

```quazi
pub fn poll(fds: *u8, count: usize, timeout: i32) i32
```

Wait for readiness of `count` `struct pollfd` entries.

### `read`

```quazi
pub fn read(fd: i32, data: *u8, count: usize) isize
```

Read from a descriptor (-errno on failure).

### `write`

```quazi
pub fn write(fd: i32, data: *u8, count: usize) isize
```

Write to a descriptor (-errno on failure).

### `close`

```quazi
pub fn close(fd: i32) i32
```

Close a descriptor (-errno on failure).

### `access`

```quazi
pub fn access(path: str, mode: i32) i32
```

`access(path, mode)` (-errno when not accessible).

### `open`

```quazi
pub fn open(path: str, flags: i32, mode: u32) i32
```

`open` with Linux flag values (NetBSD translates them); -errno on failure.

### `exit_child`

```quazi
pub fn exit_child(status: i32) void
```

End a forked child at once (no atexit handlers, no stdio flush).

### `waitpid`

```quazi
pub fn waitpid(pid: i32, status: *i32, no_hang: bool) i32
```

Reap or poll child `pid`: its pid when it exited (with `status` set), 0
when `no_hang` and it still runs, or -errno.
