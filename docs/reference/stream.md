# `std.stream`

std.stream — byte streams: `Reader`, `Writer` and their `IoError`
(D-025, maintainer answer В26А). Files, TCP streams and the standard
streams implement them; `copy` moves bytes from any Reader to any Writer.

## Contents

- [Functions](#functions)
- [`IoError`](#ioerror) (enum)
- [`Reader`](#reader) (trait)
- [`Writer`](#writer) (trait)
- [`ByteSink`](#bytesink) (struct)
- [`ByteSource`](#bytesource) (struct)
- [`BufReader`](#bufreader) (struct)
- [`BufWriter`](#bufwriter) (struct)

## Functions

### `other_error`

```quazi
pub fn other_error(text: str) IoError
```

`IoError.Other(text)`, for modules that construct errors through `stream`.

### `native_error`

```quazi
pub fn native_error(code: i32) IoError
```

`IoError.Native(code)`.

### `closed_error`

```quazi
pub fn closed_error() IoError
```

`IoError.Closed`.

### `timed_out_error`

```quazi
pub fn timed_out_error() IoError
```

`IoError.TimedOut`.

### `would_block_error`

```quazi
pub fn would_block_error() IoError
```

`IoError.WouldBlock`.

### `packed_bytes`

```quazi
pub fn packed_bytes(data: &Array[u8]) *u8
```

`data` packed into a contiguous malloc'd byte buffer (Array elements are
word slots), or 0 when allocation fails; the caller frees it with
`core.free`.

### `copy`

```quazi
pub fn copy[R: Reader, W: Writer](reader: &R!, writer: &W!) Result[u64, IoError]
```

Copy everything `reader` produces into `writer`, then flush it; the number
of bytes copied.

## `IoError`

```quazi
pub enum IoError {
    // The other end is gone (a closed file or socket).
    Closed,
    WouldBlock,
    TimedOut,
    Interrupted,
    // A platform error code.
    Native(i32),
    Other(String),
}
```

Why a streaming read or write failed.

### `IoError.message`

```quazi
pub fn message(self: IoError) str
```

A short English description of the error, for display (a static
text, like every std error's `message()`; `detail()` adds the native
code or the `Other` text).

### `IoError.detail`

```quazi
pub fn detail(self: IoError) String
```

The full description: `message()` plus the native code, or the text
of `Other`.

## `Reader`

```quazi
pub trait Reader {
    fn read_bytes(self: &Self!, max: usize) Result[Array[u8], IoError];
}
```

A source of bytes. `read_bytes` returns up to `max` bytes; an empty array
means the end of the input.

## `Writer`

```quazi
pub trait Writer {
    fn write_bytes(self: &Self!, data: &Array[u8]) Result[usize, IoError];
    fn flush(self: &Self!) Result[bool, IoError];
}
```

A sink of bytes. `write_bytes` writes all of `data` (repeating partial
writes) or fails; `flush` pushes buffered bytes to their destination.

## `ByteSink`

```quazi
pub struct ByteSink { /* internal fields */ }
```

Collects bytes in memory: a Writer for tests and for building payloads.

### `ByteSink.new`

```quazi
pub fn new() ByteSink
```

An empty sink.

### `ByteSink.contents`

```quazi
pub fn contents(self: &ByteSink) &Array[u8]
```

The bytes written so far.

## `ByteSource`

```quazi
pub struct ByteSource { /* internal fields */ }
```

Reads bytes from an in-memory array (a Reader for tests and parsers).

### `ByteSource.new`

```quazi
pub fn new(data: Array[u8]) ByteSource
```

A source over `data`.

## `BufReader`

```quazi
pub struct BufReader[R: Reader] { /* internal fields */ }
```

Reads from `inner` in large chunks and serves small reads from memory.

### `BufReader.new`

```quazi
pub fn new(inner: R) BufReader[R]
```

A reader that fetches 8 KiB from `inner` at a time.

### `BufReader.with_capacity`

```quazi
pub fn with_capacity(inner: R, capacity: usize) BufReader[R]
```

A reader that fetches `capacity` bytes (at least 1) at a time.

### `BufReader.get_ref`

```quazi
pub fn get_ref(self: &BufReader[R]) &R
```

The wrapped reader.

### `BufReader.into_inner`

```quazi
pub fn into_inner(self: BufReader[R]) R
```

The wrapped reader; bytes still buffered are dropped.

### `BufReader.read_until`

```quazi
pub fn read_until(self: &BufReader[R]!, delimiter: u8) Result[Array[u8], IoError]
```

The bytes up to and including the next `delimiter`, or the rest of the
input when it has none; empty at the end of the input.

## `BufWriter`

```quazi
pub struct BufWriter[W: Writer] { /* internal fields */ }
```

Collects small writes in memory and passes them to `inner` in large
chunks. Buffered bytes reach `inner` on `flush`, when the buffer fills, or
when the writer is dropped (errors are then ignored: call `flush` to see
them).

### `BufWriter.new`

```quazi
pub fn new(inner: W) BufWriter[W]
```

A writer that passes 8 KiB to `inner` at a time.

### `BufWriter.with_capacity`

```quazi
pub fn with_capacity(inner: W, capacity: usize) BufWriter[W]
```

A writer that passes `capacity` bytes (at least 1) at a time.

### `BufWriter.get_ref`

```quazi
pub fn get_ref(self: &BufWriter[W]) &W
```

The wrapped writer (without the bytes still buffered).

### `BufWriter.into_inner`

```quazi
pub fn into_inner(self: BufWriter[W]) Result[W, IoError]
```

The wrapped writer, after passing it the buffered bytes (not flushed).
On error the writer is dropped without passing the bytes again.

### `BufWriter.free`

```quazi
pub fn free(self: BufWriter[W]) void
```

Dropping the writer passes the buffered bytes to `inner` and flushes
it, ignoring errors; `inner` is dropped after that.

### `BufWriter.buffered`

```quazi
pub fn buffered(self: &BufWriter[W]) usize
```

The number of bytes waiting for `flush`.
