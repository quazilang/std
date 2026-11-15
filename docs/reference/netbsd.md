# `std.netbsd`

std.netbsd — NetBSD 11.0/amd64 libc adapters.

Unlike std.unix, these are NOT Linux syscalls. NetBSD libc returns -1 and
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

_Undocumented._

### `open`

```quazi
pub fn open(path: str, flags: i32, mode: u32) i32
```

_Undocumented._

### `close`

```quazi
pub fn close(fd: i32) i32
```

_Undocumented._

### `read`

```quazi
pub fn read(fd: i32, data: *u8, size: usize) isize
```

_Undocumented._

### `write`

```quazi
pub fn write(fd: i32, data: *u8, size: usize) isize
```

_Undocumented._

### `lseek`

```quazi
pub fn lseek(fd: i32, offset: i64, whence: i32) i64
```

_Undocumented._

### `fsync`

```quazi
pub fn fsync(fd: i32) i32
```

_Undocumented._

### `ftruncate`

```quazi
pub fn ftruncate(fd: i32, len: i64) i32
```

_Undocumented._

### `access`

```quazi
pub fn access(path: str, mode: i32) i32
```

_Undocumented._

### `unlink`

```quazi
pub fn unlink(path: str) i32
```

_Undocumented._

### `mkdir`

```quazi
pub fn mkdir(path: str, mode: u32) i32
```

_Undocumented._

### `rmdir`

```quazi
pub fn rmdir(path: str) i32
```

_Undocumented._

### `rename`

```quazi
pub fn rename(old: str, new: str) i32
```

_Undocumented._

### `chdir`

```quazi
pub fn chdir(path: str) i32
```

_Undocumented._

### `getcwd`

```quazi
pub fn getcwd(buf: str, size: usize) isize
```

_Undocumented._

### `sched_yield`

```quazi
pub fn sched_yield() i32
```

_Undocumented._

### `getuid`

```quazi
pub fn getuid() u32
```

_Undocumented._

### `getgid`

```quazi
pub fn getgid() u32
```

_Undocumented._

### `geteuid`

```quazi
pub fn geteuid() u32
```

_Undocumented._

### `getegid`

```quazi
pub fn getegid() u32
```

_Undocumented._

### `umask`

```quazi
pub fn umask(mask: u32) u32
```

_Undocumented._

### `kill`

```quazi
pub fn kill(pid: i32, sig: i32) i32
```

_Undocumented._

### `clock_gettime`

```quazi
pub fn clock_gettime(clock_id: i32, result: *u8) i32
```

_Undocumented._

### `opendir`

```quazi
pub fn opendir(path: str) *u8
```

_Undocumented._

### `readdir`

```quazi
pub fn readdir(handle: *u8) *u8
```

_Undocumented._

### `closedir`

```quazi
pub fn closedir(handle: *u8) i32
```

_Undocumented._

### `link`

```quazi
pub fn link(old: str, new_path: str) i32
```

_Undocumented._

### `symlink`

```quazi
pub fn symlink(target: str, link_path: str) i32
```

_Undocumented._

### `chmod`

```quazi
pub fn chmod(path: str, mode: u32) i32
```

_Undocumented._

### `getpid`

```quazi
pub fn getpid() i32
```

_Undocumented._

### `getppid`

```quazi
pub fn getppid() i32
```

_Undocumented._

### `socket`

```quazi
pub fn socket(domain: i32, kind: i32, protocol: i32) i32
```

_Undocumented._

### `setsockopt`

```quazi
pub fn setsockopt(fd: i32, level: i32, name: i32, value: *u8, length: u32) i32
```

_Undocumented._

### `listen`

```quazi
pub fn listen(fd: i32, backlog: i32) i32
```

_Undocumented._

### `accept`

```quazi
pub fn accept(fd: i32, addr: *u8, len: *u32) i32
```

_Undocumented._

### `sendto`

```quazi
pub fn sendto(fd: i32, buf: *u8, count: usize, flags: i32, address: *u8, address_size: u32) isize
```

_Undocumented._

### `recvfrom`

```quazi
pub fn recvfrom(fd: i32, buf: *u8, count: usize, flags: i32, address: *u8, address_size: *u32) isize
```

_Undocumented._

### `shutdown`

```quazi
pub fn shutdown(fd: i32, mode: i32) i32
```

_Undocumented._
