# `std.collections.hash_set`

std.collections.hash_set — a generic set of `Hash + Eq` values.

## Contents

- [`HashSet`](#hashset) (struct)

## `HashSet`

```quazi
pub struct HashSet[K: Hash + Eq] { /* internal fields */ }
```

A set that owns its values (a `HashMap` without payloads).

### `HashSet.new`

```quazi
pub fn new() HashSet[K]
```

An empty set.

### `HashSet.len`

```quazi
pub fn len(self: &HashSet[K]) usize
```

The number of values.

### `HashSet.is_empty`

```quazi
pub fn is_empty(self: &HashSet[K]) bool
```

Whether the set has no values.

### `HashSet.insert`

```quazi
pub fn insert(self: &HashSet[K]!, value: K) Result[bool, ArrayReserveError]
```

Add `value`: true when it was not in the set (otherwise it is dropped).
If capacity or allocation fails, existing values are preserved.

### `HashSet.contains`

```quazi
pub fn contains(self: &HashSet[K], value: &K) bool
```

Whether the set has `value`.

### `HashSet.remove`

```quazi
pub fn remove(self: &HashSet[K]!, value: &K) bool
```

Remove and drop `value`; false when it was not in the set.

### `HashSet.value_at`

```quazi
pub fn value_at(self: &HashSet[K], index: usize) &K
```

Value number `index` (0 to `len() - 1`); panics when out of range.

### `HashSet.clear`

```quazi
pub fn clear(self: &HashSet[K]!) void
```

Remove and drop every value.
