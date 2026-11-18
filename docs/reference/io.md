# `std.io`

std.io — console I/O
UTF-8 contract: all str/&str parameters are valid UTF-8.

## Contents

- [Functions](#functions)
- [`Stdout`](#stdout) (struct)
- [`Stderr`](#stderr) (struct)
- [`ReadError`](#readerror) (enum)
- [`Stdin`](#stdin) (struct)

## Functions

### `stdout`

```quazi
pub fn stdout() Stdout
```

The standard output stream.

### `stderr`

```quazi
pub fn stderr() Stderr
```

The standard error stream.

### `print`

```quazi
pub fn print(template: str, ...args: Display) void
```

Writes formatted text to standard output without a newline. `{}` in
`s` is replaced by the next argument (`print("{} items", count)`).

### `println`

```quazi
pub fn println(template: str, ...args: Display) void
```

Writes formatted text and a newline to standard output.

### `err`

```quazi
pub fn err(template: str, ...args: Display) void
```

Writes formatted text to standard error without a newline.

### `errln`

```quazi
pub fn errln(template: str, ...args: Display) void
```

Writes formatted text and a newline to standard error.

### `writeln`

```quazi
pub fn writeln(fd: i32, s: str) void
```

Writes `s` and a newline to the file descriptor `fd`.

### `read`

```quazi
pub fn read(delimiter: str) Result[String, ReadError]
```

Read from stdin until the UTF-8 `delimiter` or EOF. The delimiter is not
returned. Interactive custom delimiters use immediate input; Enter is
normalized from Windows CRLF/CR to `\n`.
Returns an owned, UTF-8-validated String and frees all buffers on failure.

### `readln`

```quazi
pub fn readln() Result[String, ReadError]
```

Read a full line. The trailing newline is not included.

### `readkey`

```quazi
pub fn readkey() Result[String, ReadError]
```

Read one complete UTF-8 scalar value. EOF returns an empty String.

### `copy`

```quazi
pub fn copy[R: stream.Reader, W: stream.Writer](reader: &R!, writer: &W!) Result[u64, stream.IoError]
```

Copy everything `reader` produces into `writer`, then flush it (see
`stream.copy`).

### `stdin`

```quazi
pub fn stdin() Stdin
```

The standard input stream.

## `Stdout`

```quazi
pub struct Stdout { /* internal fields */ }
```

Standard output; get it with `io.stdout()`.

### `Stdout.write`

```quazi
pub fn write(self: Stdout, s: str) void
```

Writes `s` as it is.

### `Stdout.writeln`

```quazi
pub fn writeln(self: Stdout, s: str) void
```

Writes `s` and a newline.

### `Stdout.writef`

```quazi
pub fn writef(self: Stdout, template: str, ...args: Display) void
```

Writes `template` with each `{}` replaced by the next value.

### `Stdout.writelnf`

```quazi
pub fn writelnf(self: Stdout, template: str, ...args: Display) void
```

Writes formatted text and a newline.

## `Stderr`

```quazi
pub struct Stderr { /* internal fields */ }
```

Standard error; get it with `io.stderr()`.

### `Stderr.write`

```quazi
pub fn write(self: Stderr, s: str) void
```

Writes `s` as it is.

### `Stderr.writeln`

```quazi
pub fn writeln(self: Stderr, s: str) void
```

Writes `s` and a newline.

### `Stderr.writef`

```quazi
pub fn writef(self: Stderr, template: str, ...args: Display) void
```

Writes `template` with each `{}` replaced by the next value.

### `Stderr.writelnf`

```quazi
pub fn writelnf(self: Stderr, template: str, ...args: Display) void
```

Writes formatted text and a newline.

## `ReadError`

```quazi
pub enum ReadError {
    AllocationFailed,
    CapacityOverflow,
    InputFailed,
    InvalidDelimiter,
    InvalidUtf8,
    // Standard input ended before any byte was read (an empty line is Ok("")).
    EndOfInput,
}
```

Why reading standard input failed (`EndOfInput` when the input is
closed).

## `Stdin`

```quazi
pub struct Stdin { fd: i32, }
```

Standard input as a byte stream; get it with `io.stdin()`.
