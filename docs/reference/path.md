# `std.path`

Lexical path manipulation. Nothing here touches the file system: `join`,
`parent` and `normalize` work on the text alone, so `normalize` does not
resolve symbolic links. `/` separates components everywhere; Windows builds
also accept `\` and treat `C:\` and `\\server\share` prefixes as absolute.
Indexes count Unicode scalars, like every `str` operation.

## Contents

- [`Path`](#path) (struct)
- [`PathBuf`](#pathbuf) (type alias)

## `Path`

```quazi
pub struct Path { /* internal fields */ }
```

A file-system path held as owned UTF-8 text. Its methods split and join
paths lexically (without touching the disk); `std.fs` adds file-system
queries such as `exists`, `is_dir` and `read_dir`.

### `Path.new`

```quazi
pub fn new(text: str) Path
```

A path holding a copy of `text`.

### `Path.as_str`

```quazi
pub fn as_str(self: &Path) str
```

The path as text.

### `Path.to_string`

```quazi
pub fn to_string(self: &Path) String
```

An owned copy of the text.

### `Path.with_extension`

```quazi
pub fn with_extension(self: &Path, extension: str) Path
```

The path with its extension replaced (or added; empty removes it).

### `Path.starts_with`

```quazi
pub fn starts_with(self: &Path, base: str) bool
```

Whether the path starts with all components of `base`.

### `Path.is_absolute`

```quazi
pub fn is_absolute(self: &Path) bool
```

A rooted path: `/x`, and on Windows also `\x`, `C:\x` and `\\host\x`.

### `Path.join`

```quazi
pub fn join(self: &Path, child: str) Path
```

`child` appended with one separator; an absolute `child` replaces the
path, as an empty base yields `child` unchanged.

### `Path.file_name`

```quazi
pub fn file_name(self: &Path) Option[String]
```

The last component, unless the path ends in a root or `..`.

### `Path.parent`

```quazi
pub fn parent(self: &Path) Option[Path]
```

The path without its last component: `a/b` -> `a`, `a` -> ``, and a
root or empty path has none.

### `Path.extension`

```quazi
pub fn extension(self: &Path) Option[String]
```

The file name after its last `.`; none for `.hidden` or no dot.

### `Path.stem`

```quazi
pub fn stem(self: &Path) Option[String]
```

The file name without its extension.

### `Path.components`

```quazi
pub fn components(self: &Path) Array[String]
```

Components between separators, skipping empty ones and `.`; a root
is reported as the separator (with its drive on Windows).

### `Path.normalize`

```quazi
pub fn normalize(self: &Path) Path
```

`.` components and duplicate separators removed and `x/..` pairs
collapsed lexically; leading `..` of a relative path are kept and a
root swallows `..`. An empty result is `.`.

## `PathBuf`

```quazi
pub type PathBuf = Path;
```

`Path` owns its text, so the owned and borrowed spellings are one type.
