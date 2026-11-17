# `std.timezone`

std.timezone — named time zones from IANA TZif data (RFC 8536).

A TimeZone maps an instant to its UTC offset, abbreviation and daylight
flag. Transitions come from the TZif file; instants after the last one use
the file's POSIX TZ footer rule (e.g. `EET-2EEST,M3.5.0/3,M10.5.0/4`).
Leap-second records are ignored: SystemTime counts POSIX seconds.

## Contents

- [`TimeZone`](#timezone) (struct)

## `TimeZone`

```quazi
pub struct TimeZone { /* internal fields */ }
```

A time zone: TZif transitions plus an optional POSIX rule for later times.

### `TimeZone.utc`

```quazi
pub fn utc() TimeZone
```

Coordinated Universal Time.

### `TimeZone.from_tzif`

```quazi
pub fn from_tzif(name: str, data: &Array[u8]) Result[TimeZone, TimeError]
```

Decode TZif data (versions 1-4). `name` is reported by `name()`.

### `TimeZone.from_posix`

```quazi
pub fn from_posix(rule: str) Result[TimeZone, TimeError]
```

A zone from a POSIX TZ rule such as `CET-1CEST,M3.5.0,M10.5.0/3`.

### `TimeZone.load`

```quazi
pub fn load(name: str) Result[TimeZone, TimeError]
```

Load an IANA zone such as `Europe/Kyiv` from the system time zone
database: `$TZDIR`, then /usr/share/zoneinfo, /etc/zoneinfo (NixOS) and
/usr/share/lib/zoneinfo. Windows has no TZif database unless TZDIR
points at one. A name with `..` or a leading `/` is UnknownZone.

### `TimeZone.local`

```quazi
pub fn local() Result[TimeZone, TimeError]
```

The process's local zone: the `TZ` variable (`:Name`, an IANA name or
a POSIX rule), otherwise /etc/localtime, otherwise UTC.

### `TimeZone.name`

```quazi
pub fn name(self: &TimeZone) str
```

The name the zone was loaded under.

### `TimeZone.offset_at`

```quazi
pub fn offset_at(self: &TimeZone, instant: &SystemTime) UtcOffset
```

The UTC offset in effect at `instant`.

### `TimeZone.is_dst_at`

```quazi
pub fn is_dst_at(self: &TimeZone, instant: &SystemTime) bool
```

Whether daylight-saving time is in effect at `instant`.

### `TimeZone.abbreviation_at`

```quazi
pub fn abbreviation_at(self: &TimeZone, instant: &SystemTime) String
```

The abbreviation in effect at `instant`, such as `EEST`.

### `TimeZone.local_time`

```quazi
pub fn local_time(self: &TimeZone, instant: &SystemTime) Option[DateTime]
```

The local wall-clock fields at `instant`; None outside years 0001-9999.

### `TimeZone.format_rfc3339`

```quazi
pub fn format_rfc3339(self: &TimeZone, instant: &SystemTime) Option[String]
```

RFC 3339 text in this zone, e.g. `2024-07-01T15:00:00+03:00`.
