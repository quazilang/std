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

_Undocumented._

### `Set.new`

```quazi
pub fn new() Result[Set, SetError]
```

_Undocumented._

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

_Undocumented._

### `Set.remove`

```quazi
pub fn remove(self: &Set!, key: usize) bool
```

_Undocumented._

### `Set.len`

```quazi
pub fn len(self: &Set) usize
```

_Undocumented._

### `Set.clear`

```quazi
pub fn clear(self: &Set!) void
```

_Undocumented._

### `Set.free`

```quazi
pub fn free(self: Set) void
```

_Undocumented._
