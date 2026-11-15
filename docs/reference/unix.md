# `std.unix`

std.unix — raw Linux x86-64 syscall bindings
Every function maps 1:1 to a Linux syscall via @syscall.
Not available on Windows (@syscall emits a no-op there).
Calls with raw pointers or caller-controlled buffer lengths are explicitly
unsafe and must be wrapped in unsafe {}. Value-only wrappers remain safe.

Pointer conventions:
  *u8   — opaque byte pointer (struct*, void*)
  *u32  — pointer to u32 out-parameter
  *i32  — pointer to i32 out-parameter
  *i64  — pointer to i64 / off_t out-parameter
  str   — pointer to byte buffer or C string (read-only view)

Other type conventions:
  fd:    i32   — file descriptor
  path:  str   — pointer to null-terminated C string
  count: usize — byte count / size_t
  isize       — ssize_t / signed return
  usize       — pointer-sized integer (non-pointer polymorphic values)
  u32         — unsigned int (mode_t, uid_t, gid_t)
  i64         — off_t, time_t

## Contents

- [Functions](#functions)

## Functions

### `read`

```quazi
pub fn read(fd: i32, buf: *u8, count: usize) isize
```

_Undocumented._

### `write`

```quazi
pub fn write(fd: i32, buf: *u8, count: usize) isize
```

_Undocumented._

### `open`

```quazi
pub fn open(path: str, flags: i32, mode: u32) i32
```

flags: O_RDONLY=0, O_WRONLY=1, O_RDWR=2, O_CREAT=64, O_TRUNC=512, O_APPEND=1024

### `close`

```quazi
pub fn close(fd: i32) i32
```

_Undocumented._

### `stat`

```quazi
pub fn stat(path: str, statbuf: *u8) i32
```

statbuf: pointer to struct stat (144 bytes on x86-64)

### `fstat`

```quazi
pub fn fstat(fd: i32, statbuf: *u8) i32
```

_Undocumented._

### `lstat`

```quazi
pub fn lstat(path: str, statbuf: *u8) i32
```

_Undocumented._

### `poll`

```quazi
pub fn poll(fds: *u8, nfds: usize, timeout: i32) i32
```

fds: pointer to struct pollfd[]; nfds: count; timeout: ms (-1 = forever)

### `lseek`

```quazi
pub fn lseek(fd: i32, offset: i64, whence: i32) i64
```

whence: SEEK_SET=0, SEEK_CUR=1, SEEK_END=2

### `pread64`

```quazi
pub fn pread64(fd: i32, buf: str, count: usize, offset: i64) isize
```

pread64 / pwrite64 — positional read/write (no seek side effect)

### `pwrite64`

```quazi
pub fn pwrite64(fd: i32, buf: str, count: usize, offset: i64) isize
```

_Undocumented._

### `readv`

```quazi
pub fn readv(fd: i32, iov: *u8, iovcnt: i32) isize
```

iov: pointer to struct iovec[]; iovcnt: vector count

### `writev`

```quazi
pub fn writev(fd: i32, iov: *u8, iovcnt: i32) isize
```

_Undocumented._

### `access`

```quazi
pub fn access(path: str, mode: i32) i32
```

mode: R_OK=4, W_OK=2, X_OK=1, F_OK=0

### `pipe`

```quazi
pub fn pipe(pipefd: *u8) i32
```

pipe — pipefd: pointer to i32[2]; [0]=read end, [1]=write end

### `pipe2`

```quazi
pub fn pipe2(pipefd: *u8, flags: i32) i32
```

_Undocumented._

### `select`

```quazi
pub fn select(nfds: i32, readfds: *u8, writefds: *u8, exceptfds: *u8, timeout: *u8) i32
```

readfds/writefds/exceptfds: pointer to fd_set; timeout: pointer to struct timeval

### `dup`

```quazi
pub fn dup(oldfd: i32) i32
```

_Undocumented._

### `dup2`

```quazi
pub fn dup2(oldfd: i32, newfd: i32) i32
```

_Undocumented._

### `dup3`

```quazi
pub fn dup3(oldfd: i32, newfd: i32, flags: i32) i32
```

_Undocumented._

### `ioctl`

```quazi
pub fn ioctl(fd: i32, request: usize, arg: usize) i32
```

request/arg are polymorphic per ioctl — keep as usize

### `ioctl_ptr`

```quazi
pub fn ioctl_ptr(fd: i32, request: usize, arg: *u8) i32
```

Pointer-valued ioctl argument. Unsafe because the request controls how much
memory the kernel reads or writes through `arg`.

### `fcntl`

```quazi
pub fn fcntl(fd: i32, cmd: i32, arg: i64) i32
```

cmd: F_DUPFD=0, F_GETFD=1, F_SETFD=2, F_GETFL=3, F_SETFL=4

### `flock`

```quazi
pub fn flock(fd: i32, operation: i32) i32
```

operation: LOCK_SH=1, LOCK_EX=2, LOCK_NB=4, LOCK_UN=8

### `fsync`

```quazi
pub fn fsync(fd: i32) i32
```

_Undocumented._

### `fdatasync`

```quazi
pub fn fdatasync(fd: i32) i32
```

_Undocumented._

### `truncate`

```quazi
pub fn truncate(path: str, length: i64) i32
```

_Undocumented._

### `ftruncate`

```quazi
pub fn ftruncate(fd: i32, length: i64) i32
```

_Undocumented._

### `getdents`

```quazi
pub fn getdents(fd: i32, dirp: *u8, count: usize) isize
```

dirp: pointer to struct dirent buffer; count: buffer size

### `getdents64`

```quazi
pub fn getdents64(fd: i32, dirp: *u8, count: usize) isize
```

_Undocumented._

### `getcwd`

```quazi
pub fn getcwd(buf: str, size: usize) isize
```

_Undocumented._

### `chdir`

```quazi
pub fn chdir(path: str) i32
```

_Undocumented._

### `fchdir`

```quazi
pub fn fchdir(fd: i32) i32
```

_Undocumented._

### `rename`

```quazi
pub fn rename(oldpath: str, newpath: str) i32
```

_Undocumented._

### `renameat`

```quazi
pub fn renameat(olddirfd: i32, oldpath: str, newdirfd: i32, newpath: str) i32
```

_Undocumented._

### `mkdir`

```quazi
pub fn mkdir(path: str, mode: u32) i32
```

_Undocumented._

### `mkdirat`

```quazi
pub fn mkdirat(dirfd: i32, path: str, mode: u32) i32
```

_Undocumented._

### `rmdir`

```quazi
pub fn rmdir(path: str) i32
```

_Undocumented._

### `creat`

```quazi
pub fn creat(path: str, mode: u32) i32
```

_Undocumented._

### `link`

```quazi
pub fn link(oldpath: str, newpath: str) i32
```

_Undocumented._

### `linkat`

```quazi
pub fn linkat(olddirfd: i32, oldpath: str, newdirfd: i32, newpath: str, flags: i32) i32
```

_Undocumented._

### `unlink`

```quazi
pub fn unlink(path: str) i32
```

_Undocumented._

### `unlinkat`

```quazi
pub fn unlinkat(dirfd: i32, path: str, flags: i32) i32
```

_Undocumented._

### `symlink`

```quazi
pub fn symlink(target: str, linkpath: str) i32
```

_Undocumented._

### `symlinkat`

```quazi
pub fn symlinkat(target: str, newdirfd: i32, linkpath: str) i32
```

_Undocumented._

### `readlink`

```quazi
pub fn readlink(path: str, buf: str, bufsiz: usize) isize
```

_Undocumented._

### `readlinkat`

```quazi
pub fn readlinkat(dirfd: i32, path: str, buf: str, bufsiz: usize) isize
```

_Undocumented._

### `chmod`

```quazi
pub fn chmod(path: str, mode: u32) i32
```

_Undocumented._

### `fchmod`

```quazi
pub fn fchmod(fd: i32, mode: u32) i32
```

_Undocumented._

### `fchmodat`

```quazi
pub fn fchmodat(dirfd: i32, path: str, mode: u32, flags: i32) i32
```

_Undocumented._

### `chown`

```quazi
pub fn chown(path: str, owner: u32, group: u32) i32
```

_Undocumented._

### `fchown`

```quazi
pub fn fchown(fd: i32, owner: u32, group: u32) i32
```

_Undocumented._

### `lchown`

```quazi
pub fn lchown(path: str, owner: u32, group: u32) i32
```

_Undocumented._

### `fchownat`

```quazi
pub fn fchownat(dirfd: i32, path: str, owner: u32, group: u32, flags: i32) i32
```

_Undocumented._

### `umask`

```quazi
pub fn umask(mask: u32) u32
```

_Undocumented._

### `faccessat`

```quazi
pub fn faccessat(dirfd: i32, path: str, mode: i32, flags: i32) i32
```

dirfd: AT_FDCWD=-100 to use cwd

### `openat`

```quazi
pub fn openat(dirfd: i32, path: str, flags: i32, mode: u32) i32
```

_Undocumented._

### `sendfile`

```quazi
pub fn sendfile(out_fd: i32, in_fd: i32, offset: *i64, count: usize) isize
```

offset: pointer to off_t (i64) — updated with new file position; pass null to ignore

### `preadv`

```quazi
pub fn preadv(fd: i32, iov: *u8, iovcnt: i32, offset: i64) isize
```

iov: pointer to struct iovec[]

### `pwritev`

```quazi
pub fn pwritev(fd: i32, iov: *u8, iovcnt: i32, offset: i64) isize
```

_Undocumented._

### `statx`

```quazi
pub fn statx(dirfd: i32, path: str, flags: i32, mask: u32, statxbuf: *u8) i32
```

statxbuf: pointer to struct statx

### `mknod`

```quazi
pub fn mknod(path: str, mode: u32, dev: u64) i32
```

mknod — create special file (device, FIFO, socket)

### `splice`

```quazi
pub fn splice(fd_in: i32, off_in: *i64, fd_out: i32, off_out: *i64, len: usize, flags: u32) isize
```

off_in / off_out: pointer to off_t (updated after call); pass null to use fd position

### `tee`

```quazi
pub fn tee(fd_in: i32, fd_out: i32, len: usize, flags: u32) isize
```

_Undocumented._

### `copy_file_range`

```quazi
pub fn copy_file_range(fd_in: i32, off_in: *i64, fd_out: i32, off_out: *i64, len: usize, flags: u32) isize
```

_Undocumented._

### `fallocate`

```quazi
pub fn fallocate(fd: i32, mode: i32, offset: i64, len: i64) i32
```

fallocate — preallocate file space

### `sync`

```quazi
pub fn sync() void
```

_Undocumented._

### `syncfs`

```quazi
pub fn syncfs(fd: i32) i32
```

_Undocumented._

### `mmap`

```quazi
pub fn mmap(addr: *u8, length: usize, prot: i32, flags: i32, fd: i32, offset: i64) *u8
```

prot: PROT_NONE=0, PROT_READ=1, PROT_WRITE=2, PROT_EXEC=4
flags: MAP_SHARED=1, MAP_PRIVATE=2, MAP_ANONYMOUS=32, MAP_FIXED=16
addr: hint address (pass null for kernel choice); returns mapped address or MAP_FAILED

### `munmap`

```quazi
pub fn munmap(addr: *u8, length: usize) i32
```

_Undocumented._

### `mprotect`

```quazi
pub fn mprotect(addr: *u8, len: usize, prot: i32) i32
```

_Undocumented._

### `mremap`

```quazi
pub fn mremap(old_addr: *u8, old_size: usize, new_size: usize, flags: i32, new_addr: *u8) *u8
```

flags: MREMAP_MAYMOVE=1, MREMAP_FIXED=2
new_addr: only used when MREMAP_FIXED is set

### `madvise`

```quazi
pub fn madvise(addr: *u8, length: usize, advice: i32) i32
```

advice: MADV_NORMAL=0, MADV_RANDOM=1, MADV_SEQUENTIAL=2, MADV_DONTNEED=4, MADV_FREE=8

### `msync`

```quazi
pub fn msync(addr: *u8, length: usize, flags: i32) i32
```

flags: MS_ASYNC=1, MS_SYNC=4, MS_INVALIDATE=2

### `mlock`

```quazi
pub fn mlock(addr: *u8, len: usize) i32
```

_Undocumented._

### `munlock`

```quazi
pub fn munlock(addr: *u8, len: usize) i32
```

_Undocumented._

### `mlockall`

```quazi
pub fn mlockall(flags: i32) i32
```

flags: MCL_CURRENT=1, MCL_FUTURE=2

### `munlockall`

```quazi
pub fn munlockall() i32
```

_Undocumented._

### `brk`

```quazi
pub fn brk(addr: *u8) *u8
```

brk — set program break (end of data segment); returns new break

### `memfd_create`

```quazi
pub fn memfd_create(name: str, flags: u32) i32
```

memfd_create — anonymous file in memory

### `getrandom`

```quazi
pub fn getrandom(buf: str, buflen: usize, flags: u32) isize
```

getrandom — kernel CSPRNG; buf is a write buffer

### `fork`

```quazi
pub fn fork() i32
```

_Undocumented._

### `vfork`

```quazi
pub fn vfork() i32
```

_Undocumented._

### `execve`

```quazi
pub fn execve(path: str, argv: *u8, envp: *u8) i32
```

argv/envp: pointer to null-terminated array of C strings

### `execveat`

```quazi
pub fn execveat(dirfd: i32, path: str, argv: *u8, envp: *u8, flags: i32) i32
```

_Undocumented._

### `wait4`

```quazi
pub fn wait4(pid: i32, wstatus: *u32, options: i32, rusage: *u8) i32
```

wstatus: pointer to i32 exit status; rusage: pointer to struct rusage or null

### `waitid`

```quazi
pub fn waitid(idtype: i32, id: u32, infop: *u8, options: i32) i32
```

infop: pointer to siginfo_t

### `exit`

```quazi
pub fn exit(status: i32) void
```

_Undocumented._

### `exit_group`

```quazi
pub fn exit_group(status: i32) void
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

### `gettid`

```quazi
pub fn gettid() i32
```

_Undocumented._

### `setsid`

```quazi
pub fn setsid() i32
```

_Undocumented._

### `getsid`

```quazi
pub fn getsid(pid: i32) i32
```

_Undocumented._

### `setpgid`

```quazi
pub fn setpgid(pid: i32, pgid: i32) i32
```

_Undocumented._

### `getpgid`

```quazi
pub fn getpgid(pid: i32) i32
```

_Undocumented._

### `getpgrp`

```quazi
pub fn getpgrp() i32
```

_Undocumented._

### `kill`

```quazi
pub fn kill(pid: i32, sig: i32) i32
```

sig: SIGTERM=15, SIGKILL=9, SIGINT=2, SIGHUP=1, SIGUSR1=10, SIGUSR2=12

### `tkill`

```quazi
pub fn tkill(tid: i32, sig: i32) i32
```

_Undocumented._

### `tgkill`

```quazi
pub fn tgkill(tgid: i32, tid: i32, sig: i32) i32
```

_Undocumented._

### `clone`

```quazi
pub fn clone(flags: u64, stack: *u8, parent_tid: *u32, child_tid: *u32, tls: *u8) i32
```

clone — low-level thread/process creation
stack: top of new stack; parent_tid/child_tid: pointers to TID storage; tls: TLS base

### `prctl`

```quazi
pub fn prctl(option: i32, arg2: usize, arg3: usize, arg4: usize, arg5: usize) i32
```

prctl — args are polymorphic (int or pointer per option); keep as usize

### `arch_prctl`

```quazi
pub fn arch_prctl(op: i32, addr: *u8) i32
```

arch_prctl — x86-64 specific; op: ARCH_SET_FS=0x1002, ARCH_GET_FS=0x1003
addr: pointer to u64 for GET, value for SET

### `sched_yield`

```quazi
pub fn sched_yield() i32
```

_Undocumented._

### `sched_setaffinity`

```quazi
pub fn sched_setaffinity(pid: i32, cpusetsize: usize, mask: *u8) i32
```

mask: pointer to cpu_set_t

### `sched_getaffinity`

```quazi
pub fn sched_getaffinity(pid: i32, cpusetsize: usize, mask: *u8) i32
```

_Undocumented._

### `getcpu`

```quazi
pub fn getcpu(cpu: *u32, node: *u32) i32
```

cpu/node: pointers to u32 out-parameters

### `ptrace`

```quazi
pub fn ptrace(request: i32, pid: i32, addr: *u8, data: *u8) isize
```

ptrace — addr/data are polymorphic per request

### `set_tid_address`

```quazi
pub fn set_tid_address(tidptr: *u32) i32
```

tidptr: pointer to u32 (cleared on thread exit, triggers futex wake)

### `rt_sigaction`

```quazi
pub fn rt_sigaction(signum: i32, act: *u8, oldact: *u8, sigsetsize: usize) i32
```

act/oldact: pointer to struct sigaction (or null)

### `rt_sigprocmask`

```quazi
pub fn rt_sigprocmask(how: i32, set: *u8, oldset: *u8, sigsetsize: usize) i32
```

set/oldset: pointer to sigset_t (or null)
how: SIG_BLOCK=0, SIG_UNBLOCK=1, SIG_SETMASK=2

### `rt_sigpending`

```quazi
pub fn rt_sigpending(set: *u8, sigsetsize: usize) i32
```

set: pointer to sigset_t output

### `rt_sigsuspend`

```quazi
pub fn rt_sigsuspend(mask: *u8, sigsetsize: usize) i32
```

mask: pointer to sigset_t to block while waiting

### `pause`

```quazi
pub fn pause() i32
```

_Undocumented._

### `alarm`

```quazi
pub fn alarm(seconds: u32) u32
```

_Undocumented._

### `sigaltstack`

```quazi
pub fn sigaltstack(ss: *u8, old_ss: *u8) i32
```

ss/old_ss: pointer to stack_t struct (or null)

### `gettimeofday`

```quazi
pub fn gettimeofday(tv: *u8, tz: *u8) i32
```

tv: pointer to struct timeval { i64 sec, i64 usec }; tz: pointer to struct timezone or null

### `settimeofday`

```quazi
pub fn settimeofday(tv: *u8, tz: *u8) i32
```

_Undocumented._

### `nanosleep`

```quazi
pub fn nanosleep(req: *u8, rem: *u8) i32
```

req/rem: pointer to struct timespec { i64 sec, i64 nsec }

### `clock_gettime`

```quazi
pub fn clock_gettime(clockid: i32, tp: *u8) i32
```

clockid: CLOCK_REALTIME=0, CLOCK_MONOTONIC=1, CLOCK_PROCESS_CPUTIME_ID=2
tp: pointer to struct timespec output

### `clock_settime`

```quazi
pub fn clock_settime(clockid: i32, tp: *u8) i32
```

_Undocumented._

### `clock_getres`

```quazi
pub fn clock_getres(clockid: i32, res: *u8) i32
```

res: pointer to struct timespec output

### `clock_nanosleep`

```quazi
pub fn clock_nanosleep(clockid: i32, flags: i32, req: *u8, rem: *u8) i32
```

_Undocumented._

### `getitimer`

```quazi
pub fn getitimer(which: i32, curr_value: *u8) i32
```

curr_value: pointer to struct itimerval output

### `setitimer`

```quazi
pub fn setitimer(which: i32, new_value: *u8, old_value: *u8) i32
```

new_value/old_value: pointer to struct itimerval

### `times`

```quazi
pub fn times(buf: *u8) isize
```

buf: pointer to struct tms output

### `time`

```quazi
pub fn time(tloc: *i64) i64
```

tloc: pointer to time_t output (or null); returns seconds since epoch

### `socket`

```quazi
pub fn socket(domain: i32, stype: i32, protocol: i32) i32
```

domain: AF_UNIX=1, AF_INET=2, AF_INET6=10
type: SOCK_STREAM=1, SOCK_DGRAM=2, SOCK_RAW=3

### `bind`

```quazi
pub fn bind(sockfd: i32, addr: *u8, addrlen: u32) i32
```

addr: pointer to sockaddr variant; addrlen: sizeof(sockaddr_*)

### `listen`

```quazi
pub fn listen(sockfd: i32, backlog: i32) i32
```

_Undocumented._

### `accept`

```quazi
pub fn accept(sockfd: i32, addr: *u8, addrlen: *u32) i32
```

addr: pointer to sockaddr output; addrlen: pointer to socklen_t (in/out)

### `accept4`

```quazi
pub fn accept4(sockfd: i32, addr: *u8, addrlen: *u32, flags: i32) i32
```

_Undocumented._

### `connect`

```quazi
pub fn connect(sockfd: i32, addr: *u8, addrlen: u32) i32
```

_Undocumented._

### `sendto`

```quazi
pub fn sendto(sockfd: i32, buf: *u8, len: usize, flags: i32, dest_addr: *u8, addrlen: u32) isize
```

_Undocumented._

### `recvfrom`

```quazi
pub fn recvfrom(sockfd: i32, buf: *u8, len: usize, flags: i32, src_addr: *u8, addrlen: *u32) isize
```

src_addr: pointer to sockaddr output; addrlen: pointer to socklen_t (in/out)

### `sendmsg`

```quazi
pub fn sendmsg(sockfd: i32, msg: *u8, flags: i32) isize
```

msg: pointer to struct msghdr

### `recvmsg`

```quazi
pub fn recvmsg(sockfd: i32, msg: *u8, flags: i32) isize
```

_Undocumented._

### `shutdown`

```quazi
pub fn shutdown(sockfd: i32, how: i32) i32
```

how: SHUT_RD=0, SHUT_WR=1, SHUT_RDWR=2

### `getsockname`

```quazi
pub fn getsockname(sockfd: i32, addr: *u8, addrlen: *u32) i32
```

addr: pointer to sockaddr output; addrlen: pointer to socklen_t (in/out)

### `getpeername`

```quazi
pub fn getpeername(sockfd: i32, addr: *u8, addrlen: *u32) i32
```

_Undocumented._

### `socketpair`

```quazi
pub fn socketpair(domain: i32, stype: i32, protocol: i32, sv: *u8) i32
```

sv: pointer to i32[2] (two connected sockets)

### `setsockopt`

```quazi
pub fn setsockopt(sockfd: i32, level: i32, optname: i32, optval: *u8, optlen: u32) i32
```

optval: pointer to option value buffer; optlen: size of buffer

### `getsockopt`

```quazi
pub fn getsockopt(sockfd: i32, level: i32, optname: i32, optval: *u8, optlen: *u32) i32
```

optval: pointer to option value output; optlen: pointer to socklen_t (in/out)

### `epoll_create1`

```quazi
pub fn epoll_create1(flags: i32) i32
```

_Undocumented._

### `epoll_ctl`

```quazi
pub fn epoll_ctl(epfd: i32, op: i32, fd: i32, event: *u8) i32
```

op: EPOLL_CTL_ADD=1, EPOLL_CTL_DEL=2, EPOLL_CTL_MOD=3; event: pointer to struct epoll_event

### `epoll_wait`

```quazi
pub fn epoll_wait(epfd: i32, events: *u8, maxevents: i32, timeout: i32) i32
```

events: pointer to struct epoll_event[maxevents]

### `epoll_pwait`

```quazi
pub fn epoll_pwait(epfd: i32, events: *u8, maxevents: i32, timeout: i32, sigmask: *u8) i32
```

sigmask: pointer to sigset_t (or null)

### `eventfd2`

```quazi
pub fn eventfd2(initval: u32, flags: i32) i32
```

_Undocumented._

### `timerfd_create`

```quazi
pub fn timerfd_create(clockid: i32, flags: i32) i32
```

clockid: CLOCK_REALTIME=0, CLOCK_MONOTONIC=1

### `timerfd_settime`

```quazi
pub fn timerfd_settime(fd: i32, flags: i32, new_value: *u8, old_value: *u8) i32
```

new_value/old_value: pointer to struct itimerspec

### `timerfd_gettime`

```quazi
pub fn timerfd_gettime(fd: i32, curr_value: *u8) i32
```

curr_value: pointer to struct itimerspec output

### `inotify_init1`

```quazi
pub fn inotify_init1(flags: i32) i32
```

_Undocumented._

### `inotify_add_watch`

```quazi
pub fn inotify_add_watch(fd: i32, path: str, mask: u32) i32
```

_Undocumented._

### `inotify_rm_watch`

```quazi
pub fn inotify_rm_watch(fd: i32, wd: i32) i32
```

_Undocumented._

### `signalfd4`

```quazi
pub fn signalfd4(fd: i32, mask: *u8, sizemask: usize, flags: i32) i32
```

mask: pointer to sigset_t

### `futex`

```quazi
pub fn futex(uaddr: *u32, op: i32, val: u32, timeout: *u8, uaddr2: *u32, val3: u32) i32
```

uaddr/uaddr2: pointer to u32 futex word; timeout: pointer to struct timespec or null
op: FUTEX_WAIT=0, FUTEX_WAKE=1, FUTEX_FD=2, FUTEX_REQUEUE=3

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

### `setuid`

```quazi
pub fn setuid(uid: u32) i32
```

_Undocumented._

### `setgid`

```quazi
pub fn setgid(gid: u32) i32
```

_Undocumented._

### `setreuid`

```quazi
pub fn setreuid(ruid: u32, euid: u32) i32
```

_Undocumented._

### `setregid`

```quazi
pub fn setregid(rgid: u32, egid: u32) i32
```

_Undocumented._

### `setresuid`

```quazi
pub fn setresuid(ruid: u32, euid: u32, suid: u32) i32
```

_Undocumented._

### `getresuid`

```quazi
pub fn getresuid(ruid: *u32, euid: *u32, suid: *u32) i32
```

ruid/euid/suid: pointers to u32 output

### `setresgid`

```quazi
pub fn setresgid(rgid: u32, egid: u32, sgid: u32) i32
```

_Undocumented._

### `getresgid`

```quazi
pub fn getresgid(rgid: *u32, egid: *u32, sgid: *u32) i32
```

rgid/egid/sgid: pointers to u32 output

### `getgroups`

```quazi
pub fn getgroups(size: i32, list: *u32) i32
```

list: pointer to gid_t[] output; size: capacity

### `setgroups`

```quazi
pub fn setgroups(size: usize, list: *u32) i32
```

list: pointer to gid_t[] input

### `setfsuid`

```quazi
pub fn setfsuid(fsuid: u32) i32
```

_Undocumented._

### `setfsgid`

```quazi
pub fn setfsgid(fsgid: u32) i32
```

_Undocumented._

### `uname`

```quazi
pub fn uname(buf: *u8) i32
```

buf: pointer to struct utsname output

### `sysinfo`

```quazi
pub fn sysinfo(info: *u8) i32
```

info: pointer to struct sysinfo output

### `getrusage`

```quazi
pub fn getrusage(who: i32, usage: *u8) i32
```

who: RUSAGE_SELF=0, RUSAGE_CHILDREN=-1; usage: pointer to struct rusage output

### `getrlimit`

```quazi
pub fn getrlimit(resource: i32, rlim: *u8) i32
```

resource: RLIMIT_NOFILE=7, RLIMIT_STACK=3, RLIMIT_AS=9; rlim: pointer to struct rlimit

### `setrlimit`

```quazi
pub fn setrlimit(resource: i32, rlim: *u8) i32
```

_Undocumented._

### `prlimit64`

```quazi
pub fn prlimit64(pid: i32, resource: i32, new_limit: *u8, old_limit: *u8) i32
```

new_limit/old_limit: pointer to struct rlimit64 (or null)

### `syslog`

```quazi
pub fn syslog(stype: i32, buf: str, len: i32) i32
```

_Undocumented._

### `sethostname`

```quazi
pub fn sethostname(name: str, len: usize) i32
```

_Undocumented._

### `setdomainname`

```quazi
pub fn setdomainname(name: str, len: usize) i32
```

_Undocumented._

### `reboot`

```quazi
pub fn reboot(magic1: i32, magic2: i32, cmd: u32, arg: *u8) i32
```

arg: optional pointer (depends on cmd); pass null if unused

### `chroot`

```quazi
pub fn chroot(path: str) i32
```

_Undocumented._

### `mount`

```quazi
pub fn mount(source: str, target: str, fstype: str, mountflags: usize, data: *u8) i32
```

data: filesystem-specific mount options pointer (or null)

### `umount2`

```quazi
pub fn umount2(target: str, flags: i32) i32
```

_Undocumented._

### `swapon`

```quazi
pub fn swapon(path: str, swapflags: i32) i32
```

_Undocumented._

### `swapoff`

```quazi
pub fn swapoff(path: str) i32
```

_Undocumented._

### `acct`

```quazi
pub fn acct(filename: str) i32
```

_Undocumented._

### `setxattr`

```quazi
pub fn setxattr(path: str, name: str, value: *u8, size: usize, flags: i32) i32
```

value: pointer to attribute value buffer

### `lsetxattr`

```quazi
pub fn lsetxattr(path: str, name: str, value: *u8, size: usize, flags: i32) i32
```

_Undocumented._

### `fsetxattr`

```quazi
pub fn fsetxattr(fd: i32, name: str, value: *u8, size: usize, flags: i32) i32
```

_Undocumented._

### `getxattr`

```quazi
pub fn getxattr(path: str, name: str, value: *u8, size: usize) isize
```

value: pointer to output buffer for attribute value

### `lgetxattr`

```quazi
pub fn lgetxattr(path: str, name: str, value: *u8, size: usize) isize
```

_Undocumented._

### `fgetxattr`

```quazi
pub fn fgetxattr(fd: i32, name: str, value: *u8, size: usize) isize
```

_Undocumented._

### `listxattr`

```quazi
pub fn listxattr(path: str, list: str, size: usize) isize
```

_Undocumented._

### `llistxattr`

```quazi
pub fn llistxattr(path: str, list: str, size: usize) isize
```

_Undocumented._

### `flistxattr`

```quazi
pub fn flistxattr(fd: i32, list: str, size: usize) isize
```

_Undocumented._

### `removexattr`

```quazi
pub fn removexattr(path: str, name: str) i32
```

_Undocumented._

### `lremovexattr`

```quazi
pub fn lremovexattr(path: str, name: str) i32
```

_Undocumented._

### `fremovexattr`

```quazi
pub fn fremovexattr(fd: i32, name: str) i32
```

_Undocumented._

### `readahead`

```quazi
pub fn readahead(fd: i32, offset: i64, count: usize) isize
```

_Undocumented._

### `seccomp`

```quazi
pub fn seccomp(op: u32, flags: u32, args: *u8) i32
```

args: pointer to seccomp_data struct

### `bpf`

```quazi
pub fn bpf(cmd: i32, attr: *u8, size: u32) i32
```

attr: pointer to union bpf_attr

### `setns`

```quazi
pub fn setns(fd: i32, nstype: i32) i32
```

_Undocumented._

### `unshare`

```quazi
pub fn unshare(flags: i32) i32
```

_Undocumented._

### `pivot_root`

```quazi
pub fn pivot_root(new_root: str, put_old: str) i32
```

_Undocumented._

### `membarrier`

```quazi
pub fn membarrier(cmd: i32, flags: u32, cpu_id: i32) i32
```

_Undocumented._

### `process_vm_readv`

```quazi
pub fn process_vm_readv(pid: i32, lvec: *u8, liovcnt: usize, rvec: *u8, riovcnt: usize, flags: usize) isize
```

lvec/rvec: pointer to struct iovec[]

### `process_vm_writev`

```quazi
pub fn process_vm_writev(pid: i32, lvec: *u8, liovcnt: usize, rvec: *u8, riovcnt: usize, flags: usize) isize
```

_Undocumented._
