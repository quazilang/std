# `std.collections.map`

std.collections.map — open-addressing hash map (linear probing, tombstone delete)
Keys and values are usize. Generic owned storage requires trait bounds and
drop-aware slots, which the language does not expose yet.
Resize at 75% load; initial capacity 16.

## Contents

- [`MapError`](#maperror) (enum)
- [`Map`](#map) (struct)

## `MapError`

```quazi
pub enum MapError {
    AllocationFailed,
    CapacityOverflow,
}
```

flags slot values: 0 = empty, 1 = used, 2 = tombstone

## `Map`

```quazi
pub struct Map { /* internal fields */ }
```

A hash map from `usize` keys to `usize` values (open addressing).

### `Map.new`

```quazi
pub fn new() Result[Map, MapError]
```

An empty map; `AllocationFailed` when memory is exhausted.

### `Map.insert`

```quazi
pub fn insert(self: &Map!, key: usize, val: usize) Result[bool, MapError]
```

Mutating methods require an exclusive loan; returning a second Map
would duplicate this allocation owner.

### `Map.get`

```quazi
pub fn get(self: &Map, key: usize) Option[usize]
```

The value stored for `key`, or `None`.

### `Map.contains`

```quazi
pub fn contains(self: &Map, key: usize) bool
```

Whether `key` has a value.

### `Map.remove`

```quazi
pub fn remove(self: &Map!, key: usize) bool
```

Removes `key`; returns whether it was present.

### `Map.len`

```quazi
pub fn len(self: &Map) usize
```

The number of entries.

### `Map.clear`

```quazi
pub fn clear(self: &Map!) void
```

Removes every entry.

### `Map.free`

```quazi
pub fn free(self: Map) void
```

Frees the storage; called automatically at the end of scope.
