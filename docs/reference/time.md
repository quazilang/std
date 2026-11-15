# `std.time`

std.time — monotonic durations and instants, UTC wall-clock time.

`Instant` is suitable for elapsed-time measurements and deadlines; its epoch
is opaque and values from separate system boots are incomparable.
`SystemTime` is POSIX wall-clock time (Unix seconds, leap seconds not
counted) limited to years 0001-9999; `DateTime` is its proleptic-Gregorian
UTC calendar form. Named time zones are not supported; RFC 3339 parsing
accepts numeric UTC offsets and normalizes to UTC.

## Contents

- [Functions](#functions)
- [`TimeError`](#timeerror) (enum)
- [`Duration`](#duration) (struct)
- [`Instant`](#instant) (struct)
- [`Interval`](#interval) (struct)
- [`Deadline`](#deadline) (struct)
- [`SystemTime`](#systemtime) (struct)
- [`UtcOffset`](#utcoffset) (struct)
- [`DateTime`](#datetime) (struct)

## Functions

### `sleep`

```quazi
pub fn sleep(duration: Duration) void
```

Block the calling thread for at least `duration`, rounded up to whole
milliseconds (the platform sleep granularity); saturates at u64::MAX ms.

## `TimeError`

```quazi
pub enum TimeError { ClockUnavailable, ClockWentBackwards, InvalidFormat, OutOfRange, }
```

_Undocumented._

### `TimeError.message`

```quazi
pub fn message(self: TimeError) str
```

_Undocumented._

## `Duration`

```quazi
pub struct Duration { /* internal fields */ }
```

_Undocumented._

### `Duration.zero`

```quazi
pub fn zero() Duration
```

_Undocumented._

### `Duration.from_nanoseconds`

```quazi
pub fn from_nanoseconds(nanoseconds: u64) Duration
```

_Undocumented._

### `Duration.from_microseconds`

```quazi
pub fn from_microseconds(microseconds: u64) Duration
```

_Undocumented._

### `Duration.from_milliseconds`

```quazi
pub fn from_milliseconds(milliseconds: u64) Duration
```

_Undocumented._

### `Duration.from_seconds`

```quazi
pub fn from_seconds(seconds: u64) Duration
```

_Undocumented._

### `Duration.from_minutes`

```quazi
pub fn from_minutes(minutes: u64) Option[Duration]
```

Minutes and hours are fixed 60/3600-second units; None on u64 overflow.
Days and longer calendar units are deliberately absent.

### `Duration.from_hours`

```quazi
pub fn from_hours(hours: u64) Option[Duration]
```

_Undocumented._

### `Duration.compare`

```quazi
pub fn compare(self: &Duration, other: &Duration) i32
```

-1, 0 or 1 as `self` is shorter than, equal to or longer than `other`.

### `Duration.seconds`

```quazi
pub fn seconds(self: &Duration) u64
```

_Undocumented._

### `Duration.subsec_nanoseconds`

```quazi
pub fn subsec_nanoseconds(self: &Duration) u32
```

_Undocumented._

### `Duration.checked_add`

```quazi
pub fn checked_add(self: &Duration, other: Duration) Option[Duration]
```

_Undocumented._

### `Duration.checked_sub`

```quazi
pub fn checked_sub(self: &Duration, other: Duration) Option[Duration]
```

_Undocumented._

## `Instant`

```quazi
pub struct Instant { /* internal fields */ }
```

_Undocumented._

### `Instant.now`

```quazi
pub fn now() Result[Instant, TimeError]
```

_Undocumented._

### `Instant.now`

```quazi
pub fn now() Result[Instant, TimeError]
```

_Undocumented._

### `Instant.now`

```quazi
pub fn now() Result[Instant, TimeError]
```

_Undocumented._

### `Instant.duration_since`

```quazi
pub fn duration_since(self: Instant, earlier: Instant) Result[Duration, TimeError]
```

_Undocumented._

### `Instant.checked_add`

```quazi
pub fn checked_add(self: &Instant, duration: Duration) Option[Instant]
```

None if the result does not fit the instant representation.

### `Instant.compare`

```quazi
pub fn compare(self: &Instant, other: &Instant) i32
```

-1, 0 or 1 as `self` is earlier than, equal to or later than `other`.

### `Instant.elapsed`

```quazi
pub fn elapsed(self: Instant) Result[Duration, TimeError]
```

_Undocumented._

## `Interval`

```quazi
pub struct Interval { /* internal fields */ }
```

A periodic timer on the monotonic clock. Ticks are scheduled at
start + k * period, so repeated waits do not drift; ticks missed while the
caller was busy are skipped and reported by the next `wait`.

### `Interval.new`

```quazi
pub fn new(period: Duration) Result[Interval, TimeError]
```

The first tick is one `period` from now; a zero period is OutOfRange.

### `Interval.starting_at`

```quazi
pub fn starting_at(start: &Instant, period: Duration) Result[Interval, TimeError]
```

An interval whose first tick is one `period` after `start`.

### `Interval.wait`

```quazi
pub fn wait(self: &Interval!) Result[u64, TimeError]
```

Blocks until the next tick and returns how many ticks have passed
(1, or more when the caller fell behind).

### `Interval.until`

```quazi
pub fn until(self: &Interval, now: &Instant) Duration
```

Time from `now` until the next tick, zero if it is due.

### `Interval.advance_at`

```quazi
pub fn advance_at(self: &Interval!, now: &Instant) u64
```

Ticks due at `now` (0 before the next tick), moving the schedule past
`now`; deterministic for tests.

## `Deadline`

```quazi
pub struct Deadline { /* internal fields */ }
```

A point on the monotonic clock by which an operation should finish.

### `Deadline.at`

```quazi
pub fn at(instant: Instant) Deadline
```

_Undocumented._

### `Deadline.after`

```quazi
pub fn after(duration: Duration) Result[Deadline, TimeError]
```

The deadline `duration` from now; OutOfRange if it cannot be represented.

### `Deadline.remaining`

```quazi
pub fn remaining(self: &Deadline) Result[Duration, TimeError]
```

Time left before the deadline, or zero once it has passed.

### `Deadline.has_expired`

```quazi
pub fn has_expired(self: &Deadline) Result[bool, TimeError]
```

_Undocumented._

### `Deadline.remaining_at`

```quazi
pub fn remaining_at(self: &Deadline, now: &Instant) Duration
```

`remaining` measured from an explicit instant (deterministic for tests).

## `SystemTime`

```quazi
pub struct SystemTime { /* internal fields */ }
```

Wall-clock time as Unix seconds plus nanoseconds, UTC, without leap seconds.

### `SystemTime.from_unix`

```quazi
pub fn from_unix(seconds: i64, nanoseconds: u32) Option[SystemTime]
```

None unless `nanoseconds < 1_000_000_000` and the time is in years 0001-9999.

### `SystemTime.unix_epoch`

```quazi
pub fn unix_epoch() SystemTime
```

_Undocumented._

### `SystemTime.now`

```quazi
pub fn now() Result[SystemTime, TimeError]
```

_Undocumented._

### `SystemTime.now`

```quazi
pub fn now() Result[SystemTime, TimeError]
```

_Undocumented._

### `SystemTime.now`

```quazi
pub fn now() Result[SystemTime, TimeError]
```

_Undocumented._

### `SystemTime.unix_seconds`

```quazi
pub fn unix_seconds(self: &SystemTime) i64
```

_Undocumented._

### `SystemTime.subsec_nanoseconds`

```quazi
pub fn subsec_nanoseconds(self: &SystemTime) u32
```

_Undocumented._

### `SystemTime.compare`

```quazi
pub fn compare(self: &SystemTime, other: &SystemTime) i32
```

-1, 0 or 1 as `self` is earlier than, equal to or later than `other`.

### `SystemTime.duration_since`

```quazi
pub fn duration_since(self: &SystemTime, earlier: &SystemTime) Result[Duration, TimeError]
```

The elapsed time from `earlier` to `self`; ClockWentBackwards if negative.

### `SystemTime.checked_add`

```quazi
pub fn checked_add(self: &SystemTime, duration: Duration) Option[SystemTime]
```

None when the result leaves years 0001-9999.

### `SystemTime.checked_sub`

```quazi
pub fn checked_sub(self: &SystemTime, duration: Duration) Option[SystemTime]
```

_Undocumented._

### `SystemTime.to_utc`

```quazi
pub fn to_utc(self: &SystemTime) DateTime
```

Proleptic-Gregorian UTC calendar fields.

### `SystemTime.to_offset`

```quazi
pub fn to_offset(self: &SystemTime, offset: &UtcOffset) Option[DateTime]
```

Wall-clock fields at a fixed offset; None if they leave years 0001-9999.

### `SystemTime.format_rfc3339_at`

```quazi
pub fn format_rfc3339_at(self: &SystemTime, offset: &UtcOffset) Option[String]
```

RFC 3339 text at a fixed offset, e.g. `2000-02-29T14:34:56+02:00`
(`Z` for UTC); None if the local fields leave years 0001-9999.

### `SystemTime.format_rfc3339`

```quazi
pub fn format_rfc3339(self: &SystemTime) String
```

RFC 3339 UTC text, e.g. `2026-11-08T09:05:00Z`; nonzero fractions use
nine digits (`...:00.000000123Z`).

### `SystemTime.parse_rfc3339`

```quazi
pub fn parse_rfc3339(text: str) Result[SystemTime, TimeError]
```

Parse `YYYY-MM-DDTHH:MM:SS[.fraction](Z|+hh:mm|-hh:mm)`. `T`/`Z` may be
lowercase; at most nine fraction digits; second 60 is rejected because
leap seconds are not representable. The offset is applied to give UTC.

## `UtcOffset`

```quazi
pub struct UtcOffset { /* internal fields */ }
```

A fixed offset from UTC in whole minutes, -23:59 through +23:59. It is not
a time zone: it carries no daylight-saving rules.

### `UtcOffset.utc`

```quazi
pub fn utc() UtcOffset
```

_Undocumented._

### `UtcOffset.from_hours_minutes`

```quazi
pub fn from_hours_minutes(hours: i32, minutes: i32) Option[UtcOffset]
```

`hours` carries the sign; `minutes` is 0-59 (e.g. (-5, 30) is -05:30).

### `UtcOffset.seconds`

```quazi
pub fn seconds(self: &UtcOffset) i32
```

Seconds east of UTC.

## `DateTime`

```quazi
pub struct DateTime { /* internal fields */ }
```

A proleptic-Gregorian UTC date and time of day.

### `DateTime.new`

```quazi
pub fn new(year: i32, month: u32, day: u32, hour: u32, minute: u32, second: u32, nanosecond: u32) Option[DateTime]
```

None unless every field is in range for years 0001-9999 (seconds 0-59).

### `DateTime.year`

```quazi
pub fn year(self: &DateTime) i32
```

_Undocumented._

### `DateTime.month`

```quazi
pub fn month(self: &DateTime) u32
```

_Undocumented._

### `DateTime.day`

```quazi
pub fn day(self: &DateTime) u32
```

_Undocumented._

### `DateTime.hour`

```quazi
pub fn hour(self: &DateTime) u32
```

_Undocumented._

### `DateTime.minute`

```quazi
pub fn minute(self: &DateTime) u32
```

_Undocumented._

### `DateTime.second`

```quazi
pub fn second(self: &DateTime) u32
```

_Undocumented._

### `DateTime.nanosecond`

```quazi
pub fn nanosecond(self: &DateTime) u32
```

_Undocumented._

### `DateTime.weekday`

```quazi
pub fn weekday(self: &DateTime) u32
```

ISO weekday: 1 = Monday ... 7 = Sunday.

### `DateTime.to_system_time`

```quazi
pub fn to_system_time(self: &DateTime) SystemTime
```

_Undocumented._

### `DateTime.format_rfc3339`

```quazi
pub fn format_rfc3339(self: &DateTime) String
```

_Undocumented._
