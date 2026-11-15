# `std.os_memory`

Internal Linux /proc/meminfo parsing. Return scalar bytes, never text views.

## Contents

- [Functions](#functions)

## Functions

### `available_bytes`

```quazi
pub fn available_bytes(text: str) Option[u64]
```

MemAvailable includes memory reclaimable without swapping. Zero is valid.
Missing, malformed or inconsistent snapshots use the caller's native fallback.
