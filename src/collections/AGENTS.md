# `std.collections`

The current collections are open-addressed tables with linear probing and
tombstones. They are re-exported from `std.collections`, so users can write:

```quazi
import std.collections.Map;
import std.collections.Set;
```

## Map

`Map` stores `usize -> usize`. `Map.new()` returns `Result[Map, MapError]`;
`insert()` returns `Result[bool, MapError]`, where `true` means a new key was
inserted and `false` means an existing value was replaced. `get()` returns
`Option[usize]`. `contains`, `remove`, `len`, and `free` are non-panicking.
`insert` mutates its single owning map in place:

```quazi
var counts: Map = Map.new()?;
counts.insert(7, 42)?;
var answer: usize = counts.get(7).unwrap();
```

## Set

`Set` stores `usize`. `Set.new()` returns `Result[Set, SetError]`; `insert()`
returns `Result[bool, SetError]`, where `true` means a new key was added.
`contains`, `remove`, `len`, and `free` are non-panicking.

## Invariants

- Flags are `0 = empty`, `1 = occupied`, and `2 = tombstone`.
- Capacity starts at 16 and doubles at 75% occupancy.
- Every allocation path frees earlier allocations before returning an error.
- Growth checks both capacity doubling and the conversion from slots to bytes.
- Generic owned storage is deferred until the language can express Hash/Eq and
  drop behavior for raw slots. Do not reintroduce fake unconstrained generics.
