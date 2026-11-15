# `std.collections.set`

std.collections.set — open-addressing hash set (linear probing, tombstone delete)
Elements are usize values.
Resize at 75% load; initial capacity 16.

## Contents

- [`SetError`](#seterror) (enum)
- [`Set`](#set) (struct)

## `SetError`

```quazi
pub enum SetError {
    AllocationFailed,
    CapacityOverflow,
}
```

flags slot values: 0 = empty, 1 = used, 2 = tombstone

## `Set`

```quazi
pub struct Set { /* internal fields */ }
```

A hash set of `usize` values.

### `Set.new`

```quazi
pub fn new() Result[Set, SetError]
```

An empty set; `AllocationFailed` when memory is exhausted.

### `Set.insert`

```quazi
pub fn insert(self: &Set!, key: usize) Result[bool, SetError]
```

Mutating methods require an exclusive loan; returning a second Set
would duplicate this allocation owner.

### `Set.contains`

```quazi
pub fn contains(self: &Set, key: usize) bool
```

Whether `key` is in the set.

### `Set.remove`

```quazi
pub fn remove(self: &Set!, key: usize) bool
```

Removes `key`; returns whether it was present.

### `Set.len`

```quazi
pub fn len(self: &Set) usize
```

The number of values.

### `Set.clear`

```quazi
pub fn clear(self: &Set!) void
```

Removes every value.

### `Set.free`

```quazi
pub fn free(self: Set) void
```

Frees the storage; called automatically at the end of scope.
