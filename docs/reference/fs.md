# `std.fs`

std.fs — cross-platform file-system operations for Linux and Windows.

File owns its operating-system handle. Whole-program destruction analysis
finds File.free and inserts it on every lexical exit, including early return.
Application code normally never calls close/free explicitly.

## Contents

- [Constants](#constants)
- [Functions](#functions)
- [`FsError`](#fserror) (enum)
- [`File`](#file) (struct)
- [`FileType`](#filetype) (enum)
- [`Metadata`](#metadata) (struct)
- [`LineReader`](#linereader) (struct)
- [`BufferedWriter`](#bufferedwriter) (struct)
- [`DirEntry`](#direntry) (struct)
- [`Path`](#path) (methods)

## Constants

### `SEEK_SET`

```quazi
pub const SEEK_SET: i32 = 0;
```

`whence` for `File.seek`: the offset counts from the start of the file.

### `SEEK_CUR`

```quazi
pub const SEEK_CUR: i32 = 1;
```

`whence` for `File.seek`: the offset counts from the current position.

### `SEEK_END`

```quazi
pub const SEEK_END: i32 = 2;
```

`whence` for `File.seek`: the offset counts from the end of the file.

## Functions

### `current_dir`

```quazi
pub fn current_dir() Result[String, FsError]
```

The process's current working directory as an owned path.

### `set_current_dir`

```quazi
pub fn set_current_dir(path: str) Result[bool, FsError]
```

Change the process's current working directory. This affects every thread.

### `read_to_string`

```quazi
pub fn read_to_string(path: str) Result[String, FsError]
```

Read a UTF-8 text file into an owned String. File closure is automatic on
success and every error path; only the private raw staging allocation needs
explicit release before it has been promoted into String ownership.

### `read_to_string_with_limit`

```quazi
pub fn read_to_string_with_limit(path: str, max_bytes: usize) Result[String, FsError]
```

Read a whole UTF-8 file of at most `max_bytes` bytes. A larger file fails
with TooLarge after reading at most `max_bytes + 1` bytes, so untrusted
paths cannot force unbounded allocation.

### `read_bytes_with_limit`

```quazi
pub fn read_bytes_with_limit(path: str, max_bytes: usize) Result[Array[u8], FsError]
```

Read a whole file of at most `max_bytes` bytes as raw bytes. A larger file
fails with TooLarge after reading at most `max_bytes + 1` bytes.

### `exists`

```quazi
pub fn exists(path: str) bool
```

Whether something (file, directory, link target) exists at `path`.

### `readable`

```quazi
pub fn readable(path: str) bool
```

Whether the file at `path` exists and can be opened for reading.

### `metadata`

```quazi
pub fn metadata(path: str) Result[Metadata, FsError]
```

Metadata of the entry `path` names, following symbolic links.

### `symlink_metadata`

```quazi
pub fn symlink_metadata(path: str) Result[Metadata, FsError]
```

Metadata of `path` itself: a symbolic link reports FileType.Symlink.

### `walk`

```quazi
pub fn walk(root_path: str) Result[Array[String], FsError]
```

Every entry below `root` as a path relative to it (`a`, `a/b.txt`, ...),
depth first. Directories are listed before their contents; symbolic links
are reported but not followed, so cycles cannot recur. `/` separates the
components on every platform (Windows accepts it too). An empty root is the
current directory. The root must be readable; a subdirectory that cannot be
listed (for example without permission) is reported but not entered.

### `read_dir`

```quazi
pub fn read_dir(path: str) Result[Array[DirEntry], FsError]
```

The immediate entries of a directory (without `.` and `..`) in
operating-system order. `fs.read_dir(path)?.len()` counts them; iterate
with `for entry : fs.read_dir(path)? { ... }`.

### `is_dir`

```quazi
pub fn is_dir(path: str) bool
```

Whether `path` is a directory (links followed). `false` when it does not
exist or cannot be examined.

### `is_file`

```quazi
pub fn is_file(path: str) bool
```

Whether `path` is a regular file (links followed). `false` when it does
not exist or cannot be examined.

### `is_symlink`

```quazi
pub fn is_symlink(path: str) bool
```

Whether `path` itself is a symbolic link. `false` when it does not exist
or cannot be examined.

### `create_dir_all`

```quazi
pub fn create_dir_all(path: str) Result[bool, FsError]
```

Creates `path` and every missing parent; an existing directory is fine.

### `canonicalize`

```quazi
pub fn canonicalize(path: str) Result[Path, FsError]
```

The absolute path with symbolic links, `.` and `..` resolved; the path
must exist.

### `write`

```quazi
pub fn write(path: str, contents: str) Result[usize, FsError]
```

Creates or truncates `path` and writes `contents`.

### `writable`

```quazi
pub fn writable(path: str) bool
```

Whether the current process may write `path` (an existing file or
directory).

### `remove`

```quazi
pub fn remove(path: str) Result[bool, FsError]
```

Deletes the file at `path` (not a directory; see `rmdir`).

### `mkdir`

```quazi
pub fn mkdir(path: str) Result[bool, FsError]
```

Creates the directory `path`; its parent must exist (see `create_dir_all`).
Errors with `AlreadyExists` when something already has that name.

### `mkdir_mode`

```quazi
pub fn mkdir_mode(path: str, mode: u32) Result[bool, FsError]
```

Like `mkdir`, with Unix permission bits `mode` (before the process
`umask`); Windows ignores `mode`.

### `rmdir`

```quazi
pub fn rmdir(path: str) Result[bool, FsError]
```

Deletes the empty directory `path` (`DirectoryNotEmpty` otherwise).

### `rename`

```quazi
pub fn rename(from: str, to: str) Result[bool, FsError]
```

Moves or renames `from` to `to`, replacing an existing file `to` where
the platform allows it. Both paths must be on the same file system.

### `link`

```quazi
pub fn link(existing: str, new_path: str) Result[bool, FsError]
```

Creates a hard link `new_path` to the existing file `existing`. Windows
returns `Unsupported`.

### `symlink`

```quazi
pub fn symlink(target: str, link_path: str) Result[bool, FsError]
```

Creates a symbolic link `link_path` that points to `target`. Windows
returns `Unsupported`.

### `chmod`

```quazi
pub fn chmod(path: str, mode: u32) Result[bool, FsError]
```

Sets the Unix permission bits of `path` to `mode` (for example `0o644`).
Windows returns `Unsupported`.

## `FsError`

```quazi
pub enum FsError {
    NotFound,
    PermissionDenied,
    AlreadyExists,
    InvalidPath,
    IsDirectory,
    NotDirectory,
    DirectoryNotEmpty,
    ReadOnly,
    NoSpace,
    TooManyOpenFiles,
    AllocationFailed,
    InvalidData,
    Unsupported,
    TooLarge,
    Native(i32),
}
```

Why a file-system operation failed. Match the variants to react to a
specific failure; use `message()` to display it.

### `FsError.message`

```quazi
pub fn message(self: FsError) str
```

A short English description of the error, for display.

## `File`

```quazi
pub struct File { /* internal fields */ }
```

An open file. It owns the operating-system handle and closes it
automatically when it goes out of scope; `close()` closes it earlier.

### `File.open`

```quazi
pub fn open(path: str) Result[File, FsError]
```

Open an existing file for reading.

### `File.create`

```quazi
pub fn create(path: str) Result[File, FsError]
```

Create or truncate a file for writing.

### `File.open_rw`

```quazi
pub fn open_rw(path: str) Result[File, FsError]
```

Open for reading and writing, creating the file when needed.

### `File.open_append`

```quazi
pub fn open_append(path: str) Result[File, FsError]
```

Open for append, creating the file when needed.

### `File.read`

```quazi
pub fn read(self: &File!, buf: *u8, n: usize) isize
```

Raw buffer read. The caller guarantees `buf` is writable for `n` bytes.

### `File.write`

```quazi
pub fn write(self: &File!, buf: bytes) Result[usize, FsError]
```

Writes `buf` and returns the number of bytes written, which can be fewer
than `buf.len()`.

### `File.write_raw`

```quazi
pub fn write_raw(self: &File!, buf: *u8, n: usize) isize
```

Raw buffer write. The caller guarantees `buf` is readable for `n` bytes.

### `File.write_str`

```quazi
pub fn write_str(self: &File!, text: str) Result[usize, FsError]
```

Writes all of `text`, repeating partial writes, and returns its length in
bytes.

### `File.close`

```quazi
pub fn close(self: &File!) Result[bool, FsError]
```

Explicit close is available for scarce-resource handoff. It invalidates
this File, so the later automatic destructor is a harmless no-op.

### `File.free`

```quazi
pub fn free(self: File) void
```

Destructor discovered by whole-program analysis.

### `File.seek`

```quazi
pub fn seek(self: &File!, offset: i64, whence: i32) Result[i64, FsError]
```

Moves the read/write position by `offset` from `whence` (`SEEK_SET`,
`SEEK_CUR` or `SEEK_END`) and returns the new position from the start.

### `File.fd`

```quazi
pub fn fd(self: &File) i32
```

Linux descriptor, or a truncated Windows HANDLE for compatibility.

### `File.raw_handle`

```quazi
pub fn raw_handle(self: &File) usize
```

The native handle (file descriptor or Windows `HANDLE`) as a number. Only
the exact `-1` bit pattern is invalid; do not test it with a sign check.

### `File.sync`

```quazi
pub fn sync(self: &File!) Result[bool, FsError]
```

Flushes the file's data and metadata to the storage device (`fsync`,
`FlushFileBuffers`).

### `File.truncate`

```quazi
pub fn truncate(self: &File!, len: i64) Result[bool, FsError]
```

File truncation is currently implemented by the Linux backend.

## `FileType`

```quazi
pub enum FileType {
    File,
    Directory,
    Symlink,
    Other,
}
```

What a path names, as reported by the operating system.

## `Metadata`

```quazi
pub struct Metadata { /* internal fields */ }
```

Size, kind, write protection and modification time of a file-system entry.

### `Metadata.len`

```quazi
pub fn len(self: &Metadata) u64
```

The file size in bytes.

### `Metadata.file_type`

```quazi
pub fn file_type(self: &Metadata) FileType
```

Whether the path is a file, a directory, a symbolic link or something else.

### `Metadata.is_file`

```quazi
pub fn is_file(self: &Metadata) bool
```

Whether the path is a regular file.

### `Metadata.is_dir`

```quazi
pub fn is_dir(self: &Metadata) bool
```

Whether the path is a directory.

### `Metadata.is_symlink`

```quazi
pub fn is_symlink(self: &Metadata) bool
```

Whether the path is a symbolic link (only from `symlink_metadata`).

### `Metadata.readonly`

```quazi
pub fn readonly(self: &Metadata) bool
```

No write permission bit for anyone (Linux) or the read-only attribute
(Windows).

### `Metadata.modified_unix_nanos`

```quazi
pub fn modified_unix_nanos(self: &Metadata) i64
```

Last modification as nanoseconds since 1970-01-01 UTC.

## `LineReader`

```quazi
pub struct LineReader { /* internal fields */ }
```

Reads a file line by line through one 64 KiB buffer. Lines end at `\n`
(a preceding `\r` is dropped too); the last line needs no terminator.
Every line must be valid UTF-8.

### `LineReader.open`

```quazi
pub fn open(path: str) Result[LineReader, FsError]
```

Opens `path` for reading line by line with `read_line`.

### `LineReader.read_line`

```quazi
pub fn read_line(self: &LineReader!) Result[Option[String], FsError]
```

The next line without its terminator, or None at the end of the file.

### `LineReader.close`

```quazi
pub fn close(self: &LineReader!) Result[bool, FsError]
```

Closes the file now (dropping the reader does it otherwise); later
reads report the end of the file.

### `LineReader.free`

```quazi
pub fn free(self: LineReader) void
```

Closes the file; called automatically at the end of scope.

## `BufferedWriter`

```quazi
pub struct BufferedWriter { /* internal fields */ }
```

Collects writes in a 64 KiB buffer and hands them to the file in large
pieces. `flush` reports write errors; dropping the writer flushes what is
left (ignoring errors, like closing a file) and closes the file.

### `BufferedWriter.create`

```quazi
pub fn create(path: str) Result[BufferedWriter, FsError]
```

Creates or truncates `path` for buffered writing.

### `BufferedWriter.write_str`

```quazi
pub fn write_str(self: &BufferedWriter!, text: str) Result[usize, FsError]
```

Appends `text`; writes the buffer to the file when it is full. Returns
the number of bytes accepted.

### `BufferedWriter.flush`

```quazi
pub fn flush(self: &BufferedWriter!) Result[bool, FsError]
```

Hands the buffered bytes to the operating system. After an error the
bytes not yet written stay buffered for a later flush.

### `BufferedWriter.close`

```quazi
pub fn close(self: &BufferedWriter!) Result[bool, FsError]
```

Flushes and closes the file, reporting either failure.

### `BufferedWriter.free`

```quazi
pub fn free(self: BufferedWriter) void
```

Flushes what it can and closes the file; called automatically at the end
of scope. Call `flush` or `close` first to see write errors.

## `DirEntry`

```quazi
pub struct DirEntry { /* internal fields */ }
```

One entry of a directory listing: its name, its path (the listed
directory joined with the name) and its type as the listing reported it.

### `DirEntry.name`

```quazi
pub fn name(self: &DirEntry) str
```

The file name of the entry, without its directory.

### `DirEntry.path`

```quazi
pub fn path(self: &DirEntry) Path
```

The listed directory joined with the entry name.

### `DirEntry.path_str`

```quazi
pub fn path_str(self: &DirEntry) str
```

The listed directory joined with the entry name, as text.

### `DirEntry.file_type`

```quazi
pub fn file_type(self: &DirEntry) FileType
```

The entry type as reported by the listing (links are not followed).

### `DirEntry.is_file`

```quazi
pub fn is_file(self: &DirEntry) bool
```

Whether the entry is a regular file (links are not followed).

### `DirEntry.is_dir`

```quazi
pub fn is_dir(self: &DirEntry) bool
```

Whether the entry is a directory (links are not followed).

### `DirEntry.is_symlink`

```quazi
pub fn is_symlink(self: &DirEntry) bool
```

Whether the entry is a symbolic link.

### `DirEntry.metadata`

```quazi
pub fn metadata(self: &DirEntry) Result[Metadata, FsError]
```

Metadata of the entry itself (a link is not followed).

## `Path`

### `Path.exists`

```quazi
pub fn exists(self: &Path) bool
```

Whether something exists at this path (see `fs.exists`).

### `Path.is_dir`

```quazi
pub fn is_dir(self: &Path) bool
```

Whether this path is a directory (see `fs.is_dir`).

### `Path.is_file`

```quazi
pub fn is_file(self: &Path) bool
```

Whether this path is a regular file (see `fs.is_file`).

### `Path.is_symlink`

```quazi
pub fn is_symlink(self: &Path) bool
```

Whether this path is a symbolic link (see `fs.is_symlink`).

### `Path.metadata`

```quazi
pub fn metadata(self: &Path) Result[Metadata, FsError]
```

Metadata of this path, links followed (see `fs.metadata`).

### `Path.read_dir`

```quazi
pub fn read_dir(self: &Path) Result[Array[DirEntry], FsError]
```

The entries of this directory (see `fs.read_dir`).

### `Path.read_to_string`

```quazi
pub fn read_to_string(self: &Path) Result[String, FsError]
```

The contents of this file as text (see `fs.read_to_string`).

### `Path.canonicalize`

```quazi
pub fn canonicalize(self: &Path) Result[Path, FsError]
```

The absolute form of this path (see `fs.canonicalize`).

### `Path.open`

```quazi
pub fn open(self: &Path) Result[File, FsError]
```

Opens the file at this path for reading (`File.open`).

### `Path.create`

```quazi
pub fn create(self: &Path) Result[File, FsError]
```

Creates or truncates the file at this path for writing (`File.create`).

### `Path.write`

```quazi
pub fn write(self: &Path, contents: str) Result[usize, FsError]
```

Replaces the file's contents with `contents` (`fs.write`).

### `Path.create_dir_all`

```quazi
pub fn create_dir_all(self: &Path) Result[bool, FsError]
```

Creates this directory and its missing parents (`fs.create_dir_all`).

### `Path.remove`

```quazi
pub fn remove(self: &Path) Result[bool, FsError]
```

Removes the file at this path (`fs.remove`).
