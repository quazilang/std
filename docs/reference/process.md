# `std.process`

std.process — shell-free child-process management.

The compiler runtime owns platform creation, command-line marshalling,
waiting, and native handles. This module keeps the public lifetime contract
independent of those platform details. Linux uses the runtime; Windows uses
CreateProcessW with a UTF-16 command line quoted for CommandLineToArgvW.

## Contents

- [Functions](#functions)
- [`ProcessError`](#processerror) (enum)
- [`ExitStatus`](#exitstatus) (enum)
- [`Child`](#child) (struct)
- [`Command`](#command) (struct)
- [`Output`](#output) (struct)

## Functions

### `spawn`

```quazi
pub fn spawn(program: str, args: Array[str]) Result[Child, ProcessError]
```

Convenience entry point for one borrowed program path and argument vector.

## `ProcessError`

```quazi
pub enum ProcessError {
    SpawnFailed(i32),
    WaitFailed(i32),
    TerminateFailed(i32),
    CloseFailed(i32),
}
```

Why a process operation failed; each variant carries the native error
code (`errno` or Windows error).

### `ProcessError.native_code`

```quazi
pub fn native_code(self: ProcessError) i32
```

The operating-system error code of the failure.

### `ProcessError.message`

```quazi
pub fn message(self: ProcessError) str
```

A short English description of the error, for display.

## `ExitStatus`

```quazi
pub enum ExitStatus {
    Code(i32),
    Signal(i32),
}
```

How a child process ended: `Code(n)` from its exit status, or
`Signal(n)` when a Unix signal killed it.

## `Child`

```quazi
pub struct Child { /* internal fields */ }
```

An owned child-process handle. `wait` and `close` consume the owner, and
scope cleanup closes a child that neither reached (terminate and reap).
`try_wait` borrows it exclusively and clears an exited handle, so later
operations on that same local are harmless no-ops.

### `Child.spawn`

```quazi
pub fn spawn(program: str, args: Array[str]) Result[Child, ProcessError]
```

Launch an exact executable path without a shell or PATH lookup. `args`
excludes argv[0]; the runtime supplies `program` as the first argument.

### `Child.wait`

```quazi
pub fn wait(self: Child) Result[Option[ExitStatus], ProcessError]
```

Wait for completion and consume this child. A previously consumed child
returns Ok(None), preserving the repeat-safe handle contract.

### `Child.try_wait`

```quazi
pub fn try_wait(self: &Child!) Result[Option[ExitStatus], ProcessError]
```

Observe a child without blocking. A live child remains available; an
exited child is cleared before its status is returned.

### `Child.terminate`

```quazi
pub fn terminate(self: &Child!) Result[bool, ProcessError]
```

Forcefully request termination without consuming the child. A cleared
handle is a no-op and returns false.

### `Child.close`

```quazi
pub fn close(self: Child) Result[bool, ProcessError]
```

Consume this child. The runtime terminates a live child and reaps it,
so closing cannot leave a Linux zombie behind.

### `Child.free`

```quazi
pub fn free(self: Child) void
```

Scope cleanup: a child that was neither waited for nor closed is
closed (a live child is terminated, then reaped). Close errors are
discarded; call `close` to observe them.

### `Child.wait_timeout`

```quazi
pub fn wait_timeout(self: &Child!, timeout: Duration) Result[Option[ExitStatus], ProcessError]
```

Wait up to `timeout` for the child to exit: its status, or None when it
is still running (it stays available for another wait or terminate).

### `Child.wait_or_terminate`

```quazi
pub fn wait_or_terminate(self: &Child!, timeout: Duration) Result[Option[ExitStatus], ProcessError]
```

Wait up to `timeout`, then terminate a child that is still running and
wait for it; always returns its final status.

### `Child.handle`

```quazi
pub fn handle(self: &Child) usize
```

The native process handle: the process id on Linux and NetBSD, a
process `HANDLE` on Windows.

## `Command`

```quazi
pub struct Command { /* internal fields */ }
```

A program to run, built step by step like a shell command line but without
a shell: `process.Command.new("git").arg("status").current_dir(dir).status()`.

### `Command.new`

```quazi
pub fn new(program: str) Command
```

A command running `program`. A name without `/` is searched in the `PATH`
the child will see; a path is used as it is.

### `Command.arg`

```quazi
pub fn arg(self: Command, value: str) Command
```

Appends one argument.

### `Command.args`

```quazi
pub fn args(self: Command, values: Array[str]) Command
```

Appends every argument of `values`.

### `Command.current_dir`

```quazi
pub fn current_dir(self: Command, directory: str) Command
```

The child's working directory (default: the parent's).

### `Command.env`

```quazi
pub fn env(self: Command, name: str, value: str) Command
```

Sets NAME=VALUE in the child's environment.

### `Command.env_remove`

```quazi
pub fn env_remove(self: Command, name: str) Command
```

Removes the variable `name` from the child's environment.

### `Command.env_clear`

```quazi
pub fn env_clear(self: Command) Command
```

Starts the child with only the variables set through `env`.

### `Command.spawn`

```quazi
pub fn spawn(self: &Command) Result[Child, ProcessError]
```

Starts the program and returns its Child.

### `Command.output`

```quazi
pub fn output(self: &Command) Result[Output, ProcessError]
```

Runs the program to completion, capturing its standard output and
standard error (read concurrently, so a large output cannot block it).

### `Command.status`

```quazi
pub fn status(self: &Command) Result[ExitStatus, ProcessError]
```

Runs the program to completion and returns its exit status.

## `Output`

```quazi
pub struct Output {
    status: ExitStatus,
    stdout: Array[u8],
    stderr: Array[u8],
}
```

The exit status and the bytes a child wrote to its standard output and
standard error (`Command.output`).
