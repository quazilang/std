# `std.collections`

The current collections are open-addressed tables with linear probing and
tombstones. They are re-exported from `std.collections`, so users can write:

```quazi
import std.collections.Map;
import std.collections.Set;
```

## Map

`Map` stores `usize -> usize`. `Map.new()` and `insert()` return
`Result[Map, MapError]`; `get()` returns `Option[usize]`. `contains`, `remove`,
`len`, and `free` are non-panicking. Reassign the returned value after an insert:

```quazi
var counts: Map = Map.new()?;
counts = counts.insert(7, 42)?;
var answer: usize = counts.get(7).unwrap();
```

## Set

`Set` stores `usize`. `Set.new()` and `insert()` return
`Result[Set, SetError]`; `contains`, `remove`, `len`, and `free` are
non-panicking.

## Invariants

- Flags are `0 = empty`, `1 = occupied`, and `2 = tombstone`.
- Capacity starts at 16 and doubles at 75% occupancy.
- Every allocation path frees earlier allocations before returning an error.
- Growth checks both capacity doubling and the conversion from slots to bytes.
- Generic owned storage is deferred until the language can express Hash/Eq and
  drop behavior for raw slots. Do not reintroduce fake unconstrained generics.
