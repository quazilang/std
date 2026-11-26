# `std.collections.hash_map`

std.collections.hash_map — a generic hash map over `Hash + Eq` keys.

Entries are stored densely, in insertion order, in `keys` and `values`;
removing an entry moves the last one into its place. `slots` is an
open-addressed index over the entries with linear probing: 0 is an empty
slot, 1 a deleted one and `n + 2` refers to entry `n`. Its length is a power
of two. At most three quarters of its slots are used or deleted.

## Contents

- [`HashMap`](#hashmap) (struct)

## `HashMap`

```quazi
pub struct HashMap[K: Hash + Eq, V] { /* internal fields */ }
```

A hash map from `K` to `V` that owns its keys and values.

### `HashMap.new`

```quazi
pub fn new() HashMap[K, V]
```

An empty map.

### `HashMap.len`

```quazi
pub fn len(self: &HashMap[K, V]) usize
```

The number of entries.

### `HashMap.is_empty`

```quazi
pub fn is_empty(self: &HashMap[K, V]) bool
```

Whether the map has no entries.

### `HashMap.find`

```quazi
pub fn find(self: &HashMap[K, V], key: &K) Option[usize]
```

The position of `key`'s entry (for `key_at`/`value_at`), or `None`.

### `HashMap.get`

```quazi
pub fn get(self: &HashMap[K, V], key: &K) Option[V]
```

A copy of `key`'s value, or `None` (like `Map.get`). For values that
own resources use `find` and `value_at`, which borrow instead.

### `HashMap.contains`

```quazi
pub fn contains(self: &HashMap[K, V], key: &K) bool
```

Whether the map has an entry for `key`.

### `HashMap.insert`

```quazi
pub fn insert(self: &HashMap[K, V]!, key: K, value: V) Result[bool, ArrayReserveError]
```

Store `value` for `key`: true when the key is new, false when an
existing value was replaced (and dropped) and `key` is dropped.
If capacity or allocation fails, existing entries are preserved.

### `HashMap.key_at`

```quazi
pub fn key_at(self: &HashMap[K, V], index: usize) &K
```

The key of entry `index` (0 to `len() - 1`, insertion order until a
removal moves the last entry); panics when out of range.

### `HashMap.value_at`

```quazi
pub fn value_at(self: &HashMap[K, V], index: usize) &V
```

The value of entry `index`; panics when out of range.

### `HashMap.remove`

```quazi
pub fn remove(self: &HashMap[K, V]!, key: &K) bool
```

Remove and drop `key`'s entry; false when there is none.

### `HashMap.clear`

```quazi
pub fn clear(self: &HashMap[K, V]!) void
```

Remove and drop every entry.
