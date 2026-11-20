# `std.thread`

std.thread — threading primitives
Cross-platform: Linux uses the compiler's embedded clone/futex runtime
(pthread_create/pthread_join when the project links libc), NetBSD uses
pthreads, Windows uses CreateThread/WaitForSingleObject.
Thread callbacks use the platform C ABI. They must be exported functions;
captured Quazi closures cannot cross this native boundary.

## Contents

- [Functions](#functions)
- [`ThreadCallback`](#threadcallback) (type alias)
- [`ThreadError`](#threaderror) (enum)
- [`Thread`](#thread) (struct)
- [`JoinHandle`](#joinhandle) (struct)
- [`AtomicI64`](#atomici64) (struct)
- [`AtomicI64View`](#atomici64view) (struct)
- [`Mutex`](#mutex) (struct)
- [`MutexView`](#mutexview) (struct)

## Functions

### `thread_spawn`

```quazi
pub fn thread_spawn(f: ThreadCallback) usize
```

Spawn a new thread running f. f must be a function pointer.
Linux: f is called as pthread_start_routine (fn(*u8) *u8).
Windows: f is called as LPTHREAD_START_ROUTINE; its exit code is the
low 32 bits of the result.
Returns a thread handle (opaque usize) or 0 on failure.

### `thread_spawn_arg`

```quazi
pub fn thread_spawn_arg(f: ThreadCallback, arg: *u8) usize
```

Like thread_spawn, but passes `arg` as the callback's argument instead of
NULL. The caller must keep `arg` valid until the thread is joined.

### `thread_join`

```quazi
pub fn thread_join(handle: usize) void
```

Wait for the thread identified by handle to finish.
On Linux also frees the pthread_t storage allocated by thread_spawn.
On Windows closes the thread handle after waiting.
A zero handle (failed spawn) is a no-op.

### `spawn`

```quazi
pub fn spawn[T](f: fn() T) Result[JoinHandle[T], ThreadError]
```

Run `f` on a new OS thread.

### `cancel_requested`

```quazi
pub fn cancel_requested() bool
```

True when code runs on a thread started by `spawn` whose `JoinHandle`
asked it to stop (`cancel`); false elsewhere.

### `sleep`

```quazi
pub fn sleep(ms: u64) void
```

Suspend the current thread for ms milliseconds.

### `yield_now`

```quazi
pub fn yield_now() void
```

Yield the processor to other threads.

### `current_tid`

```quazi
pub fn current_tid() i32
```

Returns the kernel thread ID of the calling thread (Linux `gettid`, NetBSD
`_lwp_self`; Windows returns -1).

## `ThreadCallback`

```quazi
pub type ThreadCallback = fn(*u8) *u8;
```

A native thread entry point: receives the argument pointer and returns
the thread result. One signature serves every target: Windows reads the
low 32 bits of the returned value as the thread exit code.

## `ThreadError`

```quazi
pub enum ThreadError { CreationFailed, Panicked, }
```

Why a thread could not be started or did not produce its result.

## `Thread`

```quazi
pub struct Thread { /* internal fields */ }
```

A native thread started with a `ThreadCallback`; join it with `join`.

### `Thread.spawn`

```quazi
pub fn spawn(f: ThreadCallback) Result[Thread, ThreadError]
```

Spawn a new thread running an exported C-ABI-compatible callback.

### `Thread.join`

```quazi
pub fn join(self: Thread) void
```

Wait for the thread to finish. Consumes the handle.

### `Thread.handle`

```quazi
pub fn handle(self: Thread) usize
```

Returns the opaque thread handle.

## `JoinHandle`

```quazi
pub struct JoinHandle[T] { /* internal fields */ }
```

A thread running a Quazi closure; `join()` waits for it and returns its
result. Dropping the handle also waits for the thread.

### `JoinHandle.join`

```quazi
pub fn join(self: JoinHandle[T]) Result[T, ThreadError]
```

Wait for the thread and return its result, or `Panicked` when it
panicked.

### `JoinHandle.cancel`

```quazi
pub fn cancel(self: &JoinHandle[T]) void
```

Ask the thread to stop: `cancel_requested()` on it returns true from
now on. The thread decides where to check and how to finish.

### `JoinHandle.free`

```quazi
pub fn free(self: JoinHandle[T]) void
```

Waits for the thread when the handle goes out of scope without
`join()`; a finished thread's result is dropped.

## `AtomicI64`

```quazi
pub struct AtomicI64 { /* internal fields */ }
```

A 64-bit integer whose operations are atomic and sequentially consistent.

### `AtomicI64.new`

```quazi
pub fn new(value: i64) AtomicI64
```

An atomic integer with initial `value`.

### `AtomicI64.at`

```quazi
pub fn at(ptr: *u8) AtomicI64View
```

A non-owning view of a cell created elsewhere; the caller guarantees
`ptr` came from `as_ptr()` and outlives the view.

### `AtomicI64.as_ptr`

```quazi
pub fn as_ptr(self: &AtomicI64) *u8
```

The address of the value, for sharing with native threads.

### `AtomicI64.load`

```quazi
pub fn load(self: &AtomicI64) i64
```

The current value (sequentially consistent).

### `AtomicI64.store`

```quazi
pub fn store(self: &AtomicI64, value: i64) void
```

Sets the value.

### `AtomicI64.swap`

```quazi
pub fn swap(self: &AtomicI64, value: i64) i64
```

Sets the value and returns the previous one.

### `AtomicI64.fetch_add`

```quazi
pub fn fetch_add(self: &AtomicI64, delta: i64) i64
```

Add `delta` and return the previous value.

### `AtomicI64.compare_exchange`

```quazi
pub fn compare_exchange(self: &AtomicI64, expected: i64, desired: i64) i64
```

Store `desired` only if the value equals `expected`; return the value seen.

### `AtomicI64.free`

```quazi
pub fn free(self: AtomicI64) void
```

Frees the storage; called automatically at the end of scope.

## `AtomicI64View`

```quazi
pub struct AtomicI64View { /* internal fields */ }
```

Borrowed access to an AtomicI64 owned by another scope or thread.

### `AtomicI64View.load`

```quazi
pub fn load(self: &AtomicI64View) i64
```

The current value.

### `AtomicI64View.store`

```quazi
pub fn store(self: &AtomicI64View, value: i64) void
```

Sets the value.

### `AtomicI64View.swap`

```quazi
pub fn swap(self: &AtomicI64View, value: i64) i64
```

Sets the value and returns the previous one.

### `AtomicI64View.fetch_add`

```quazi
pub fn fetch_add(self: &AtomicI64View, delta: i64) i64
```

Adds `delta` and returns the previous value.

### `AtomicI64View.compare_exchange`

```quazi
pub fn compare_exchange(self: &AtomicI64View, expected: i64, desired: i64) i64
```

Sets the value to `desired` if it equals `expected`; returns the value
found.

## `Mutex`

```quazi
pub struct Mutex { /* internal fields */ }
```

A mutual-exclusion lock. `lock` spins with compare-and-swap and yields the
processor between attempts; it is not reentrant and not fair.

### `Mutex.new`

```quazi
pub fn new() Mutex
```

An unlocked mutex.

### `Mutex.at`

```quazi
pub fn at(ptr: *u8) MutexView
```

A non-owning view of a lock created elsewhere (see AtomicI64.at).

### `Mutex.as_ptr`

```quazi
pub fn as_ptr(self: &Mutex) *u8
```

The address of the lock, for sharing with native threads.

### `Mutex.lock`

```quazi
pub fn lock(self: &Mutex) void
```

Waits until the lock is free and takes it.

### `Mutex.try_lock`

```quazi
pub fn try_lock(self: &Mutex) bool
```

Acquire the lock only if it is free; true on success.

### `Mutex.unlock`

```quazi
pub fn unlock(self: &Mutex) void
```

Releases the lock.

### `Mutex.free`

```quazi
pub fn free(self: Mutex) void
```

Frees the lock; called automatically at the end of scope.

## `MutexView`

```quazi
pub struct MutexView { /* internal fields */ }
```

A borrowed view of a `Mutex` shared with another thread.

### `MutexView.lock`

```quazi
pub fn lock(self: &MutexView) void
```

Waits until the lock is free and takes it.

### `MutexView.try_lock`

```quazi
pub fn try_lock(self: &MutexView) bool
```

Takes the lock if it is free; returns whether it did.

### `MutexView.unlock`

```quazi
pub fn unlock(self: &MutexView) void
```

Releases the lock.
