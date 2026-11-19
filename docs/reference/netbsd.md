# `std.netbsd`

std.netbsd — NetBSD 11.0/amd64 libc adapters.

Unlike std.linux, these are NOT Linux syscalls. NetBSD libc returns -1 and
stores errno in thread-local state. These wrappers expose negative errno to
Quazi APIs that historically expect the Linux syscall error convention.
Only imported when @cfg(target_os="netbsd") is active.

## Contents

- [Functions](#functions)

## Functions

### `errno_value`

```quazi
pub fn errno_value() i32
```

NetBSD libc `errno_value`, returning a negative errno on failure like the
Linux system call of the same name.

### `open`

```quazi
pub fn open(path: str, flags: i32, mode: u32) i32
```

NetBSD libc `open`, returning a negative errno on failure like the
Linux system call of the same name.

### `close`

```quazi
pub fn close(fd: i32) i32
```

NetBSD libc `close`, returning a negative errno on failure like the
Linux system call of the same name.

### `read`

```quazi
pub fn read(fd: i32, data: *u8, size: usize) isize
```

NetBSD libc `read`, returning a negative errno on failure like the
Linux system call of the same name.

### `write`

```quazi
pub fn write(fd: i32, data: *u8, size: usize) isize
```

NetBSD libc `write`, returning a negative errno on failure like the
Linux system call of the same name.

### `lseek`

```quazi
pub fn lseek(fd: i32, offset: i64, whence: i32) i64
```

NetBSD libc `lseek`, returning a negative errno on failure like the
Linux system call of the same name.

### `fsync`

```quazi
pub fn fsync(fd: i32) i32
```

NetBSD libc `fsync`, returning a negative errno on failure like the
Linux system call of the same name.

### `ftruncate`

```quazi
pub fn ftruncate(fd: i32, len: i64) i32
```

NetBSD libc `ftruncate`, returning a negative errno on failure like the
Linux system call of the same name.

### `access`

```quazi
pub fn access(path: str, mode: i32) i32
```

NetBSD libc `access`, returning a negative errno on failure like the
Linux system call of the same name.

### `unlink`

```quazi
pub fn unlink(path: str) i32
```

NetBSD libc `unlink`, returning a negative errno on failure like the
Linux system call of the same name.

### `mkdir`

```quazi
pub fn mkdir(path: str, mode: u32) i32
```

NetBSD libc `mkdir`, returning a negative errno on failure like the
Linux system call of the same name.

### `rmdir`

```quazi
pub fn rmdir(path: str) i32
```

NetBSD libc `rmdir`, returning a negative errno on failure like the
Linux system call of the same name.

### `rename`

```quazi
pub fn rename(old: str, new: str) i32
```

NetBSD libc `rename`, returning a negative errno on failure like the
Linux system call of the same name.

### `chdir`

```quazi
pub fn chdir(path: str) i32
```

NetBSD libc `chdir`, returning a negative errno on failure like the
Linux system call of the same name.

### `getcwd`

```quazi
pub fn getcwd(buf: str, size: usize) isize
```

NetBSD libc `getcwd`, returning a negative errno on failure like the
Linux system call of the same name.

### `sched_yield`

```quazi
pub fn sched_yield() i32
```

NetBSD libc `sched_yield`, returning a negative errno on failure like the
Linux system call of the same name.

### `getuid`

```quazi
pub fn getuid() u32
```

NetBSD libc `getuid`, returning a negative errno on failure like the
Linux system call of the same name.

### `getgid`

```quazi
pub fn getgid() u32
```

NetBSD libc `getgid`, returning a negative errno on failure like the
Linux system call of the same name.

### `geteuid`

```quazi
pub fn geteuid() u32
```

NetBSD libc `geteuid`, returning a negative errno on failure like the
Linux system call of the same name.

### `getegid`

```quazi
pub fn getegid() u32
```

NetBSD libc `getegid`, returning a negative errno on failure like the
Linux system call of the same name.

### `umask`

```quazi
pub fn umask(mask: u32) u32
```

NetBSD libc `umask`, returning a negative errno on failure like the
Linux system call of the same name.

### `kill`

```quazi
pub fn kill(pid: i32, sig: i32) i32
```

NetBSD libc `kill`, returning a negative errno on failure like the
Linux system call of the same name.

### `clock_gettime`

```quazi
pub fn clock_gettime(clock_id: i32, result: *u8) i32
```

NetBSD libc `clock_gettime`, returning a negative errno on failure like the
Linux system call of the same name.

### `opendir`

```quazi
pub fn opendir(path: str) *u8
```

NetBSD libc `opendir`, returning a negative errno on failure like the
Linux system call of the same name.

### `readdir`

```quazi
pub fn readdir(handle: *u8) *u8
```

NetBSD libc `readdir`, returning a negative errno on failure like the
Linux system call of the same name.

### `closedir`

```quazi
pub fn closedir(handle: *u8) i32
```

NetBSD libc `closedir`, returning a negative errno on failure like the
Linux system call of the same name.

### `link`

```quazi
pub fn link(old: str, new_path: str) i32
```

NetBSD libc `link`, returning a negative errno on failure like the
Linux system call of the same name.

### `symlink`

```quazi
pub fn symlink(target: str, link_path: str) i32
```

NetBSD libc `symlink`, returning a negative errno on failure like the
Linux system call of the same name.

### `chmod`

```quazi
pub fn chmod(path: str, mode: u32) i32
```

NetBSD libc `chmod`, returning a negative errno on failure like the
Linux system call of the same name.

### `getpid`

```quazi
pub fn getpid() i32
```

NetBSD libc `getpid`, returning a negative errno on failure like the
Linux system call of the same name.

### `getppid`

```quazi
pub fn getppid() i32
```

NetBSD libc `getppid`, returning a negative errno on failure like the
Linux system call of the same name.

### `socket`

```quazi
pub fn socket(domain: i32, kind: i32, protocol: i32) i32
```

NetBSD libc `socket`, returning a negative errno on failure like the
Linux system call of the same name.

### `setsockopt`

```quazi
pub fn setsockopt(fd: i32, level: i32, name: i32, value: *u8, length: u32) i32
```

NetBSD libc `setsockopt`, returning a negative errno on failure like the
Linux system call of the same name.

### `listen`

```quazi
pub fn listen(fd: i32, backlog: i32) i32
```

NetBSD libc `listen`, returning a negative errno on failure like the
Linux system call of the same name.

### `accept`

```quazi
pub fn accept(fd: i32, addr: *u8, len: *u32) i32
```

NetBSD libc `accept`, returning a negative errno on failure like the
Linux system call of the same name.

### `sendto`

```quazi
pub fn sendto(fd: i32, buf: *u8, count: usize, flags: i32, address: *u8, address_size: u32) isize
```

NetBSD libc `sendto`, returning a negative errno on failure like the
Linux system call of the same name.

### `recvfrom`

```quazi
pub fn recvfrom(fd: i32, buf: *u8, count: usize, flags: i32, address: *u8, address_size: *u32) isize
```

NetBSD libc `recvfrom`, returning a negative errno on failure like the
Linux system call of the same name.

### `shutdown`

```quazi
pub fn shutdown(fd: i32, mode: i32) i32
```

NetBSD libc `shutdown`, returning a negative errno on failure like the
Linux system call of the same name.

### `setenv`

```quazi
pub fn setenv(name: *u8, value: *u8) i32
```

Set (overwriting) an environment variable; 0 or negative errno.

### `unsetenv`

```quazi
pub fn unsetenv(name: *u8) i32
```

Remove an environment variable; 0 or negative errno.

### `fork`

```quazi
pub fn fork() i32
```

NetBSD libc `fork`: the child's pid in the parent, 0 in the child, or a
negative errno.

### `execve`

```quazi
pub fn execve(path: str, argv: *u8, envp: *u8) i32
```

NetBSD libc `execve`; returns only on failure, with a negative errno.

### `dup2`

```quazi
pub fn dup2(old: i32, new_fd: i32) i32
```

NetBSD libc `dup2`, returning a negative errno on failure.

### `pipe2`

```quazi
pub fn pipe2(fds: *u8, flags: i32) i32
```

NetBSD libc `pipe2`. `flags` uses the Linux O_CLOEXEC value (0x80000),
translated to NetBSD's (0x400000).

### `poll`

```quazi
pub fn poll(fds: *u8, count: usize, timeout: i32) i32
```

NetBSD libc `poll` (same `struct pollfd` layout and POLLIN as Linux).

### `waitpid`

```quazi
pub fn waitpid(pid: i32, status: *i32, options: i32) i32
```

NetBSD libc `waitpid` (WNOHANG = 1; status encoded like Linux).

### `exit_now`

```quazi
pub fn exit_now(status: i32) void
```

NetBSD libc `_exit`: ends the process without running atexit handlers or
flushing stdio (safe in a forked child).

### `stat`

```quazi
pub fn stat(path: str, buffer: *u8) i32
```

NetBSD libc `stat` (`__stat50`, the 64-bit time_t `struct stat`:
st_mode u32 at 8, st_mtimespec at 64, st_size at 112); -errno on failure.

### `lstat`

```quazi
pub fn lstat(path: str, buffer: *u8) i32
```

NetBSD libc `lstat` (`__lstat50`); -errno on failure.

### `realpath`

```quazi
pub fn realpath(path: str, resolved: *u8) i32
```

NetBSD libc `realpath` into `resolved` (PATH_MAX = 1024 bytes); -errno on
failure.

### `lwp_self`

```quazi
pub fn lwp_self() i32
```

The calling thread's LWP id.
