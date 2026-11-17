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
