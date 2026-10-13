# Standard-library plan checklist — 2026-10-13

Audited base commit: `cb1cf48` plus the existing local working tree.

**Complete: 47.7%. Remaining: 52.3%.**

Scope: the filesystem, os, process, net, math, panic, concurrency, time,
and rest-of-library requirements from the workspace production-readiness
plan (`goal.md`), plus the accepted D-012 serialization contract.
The previous eight-area estimate omitted os and the remaining library
audit. This checklist includes both. Untracked user CLI development is
preserved and receives no implementation credit from this audit.

Percentages are calculated from the explicit requirements below, not assigned
from labels such as "partial". A checked requirement has a concrete implementation
or a documented regression fixture. Unimplemented, incomplete, unproven final
validation, and currently failing requirements remain unchecked. Checked source
features do not claim that every runtime/platform combination passes.

Each plan item has equal weight. Within an item, each listed requirement has equal
weight. Item completion is `checked requirements / listed requirements`; overall
completion is the arithmetic mean of item completion fractions, using unrounded
fractions. Remaining is `100% - completion`. Display rounds to one decimal place.
The checklist breakdown is explicit review judgment; the arithmetic is exact for
this checklist. It measures implementation coverage, not remaining effort or a
release-readiness probability. New requirements change the denominator.

## Summary

| Plan item | Implemented requirements | Complete | Remaining |
| --- | --- | --- | --- |
| Filesystem / I/O | 9/16 | 56.2% | 43.8% |
| Operating-system APIs | 5/10 | 50.0% | 50.0% |
| Processes | 7/16 | 43.8% | 56.2% |
| Networking / TLS | 8/17 | 47.1% | 52.9% |
| Mathematics | 7/11 | 63.6% | 36.4% |
| Panic handling | 5/10 | 50.0% | 50.0% |
| Concurrency | 4/12 | 33.3% | 66.7% |
| Time | 5/19 | 26.3% | 73.7% |
| Serialization | 6/15 | 40.0% | 60.0% |
| Library-wide safety / other modules | 6/9 | 66.7% | 33.3% |

## Requirements

### Filesystem / I/O

Evidence: [src/fs.qz](../src/fs.qz).

- [x] File open/create/read-write/append modes.
- [x] Raw reads and writes.
- [x] Safe length-derived binary writes.
- [x] Owned validated UTF-8 whole-file reads.
- [x] Documented EOF and partial-I/O semantics.
- [x] Owning handles with lexical close and repeat-safe explicit close.
- [x] Seeking and syncing.
- [x] Basic directory enumeration and file/directory mutation.
- [x] Structured portable FsError surface.
- [ ] Buffered reader/writer abstractions.
- [ ] Common streaming reader/writer interfaces.
- [ ] Structured path abstraction.
- [ ] Structured metadata API.
- [ ] Directory iterator/traversal API.
- [ ] Bounded large-file reads.
- [ ] Complete target-native large-file/partial-I/O matrix.

### Operating-system APIs

Evidence: [src/os.qz](../src/os.qz).

- [x] Owned environment reads.
- [x] Platform-name query.
- [x] Host/CPU/memory/display metadata queries.
- [x] Process/parent identifiers.
- [x] Sleep and scheduler-yield helpers.
- [ ] Portable environment mutation.
- [ ] Portable owned cwd query and cwd changes.
- [ ] Portable standard-library argument access.
- [ ] Move Unix-specific responsibilities out of portable os surface.
- [ ] Complete target-native OS query/error matrix.

### Processes

Evidence: [src/process.qz](../src/process.qz).

- [x] Shell-free exact-path spawn.
- [x] Argument-vector marshalling.
- [x] Inherited Linux executable environment.
- [x] Inherited standard streams.
- [x] Structured errors and exit/signal status.
- [x] wait and try_wait.
- [x] Explicit termination and close/reap lifecycle.
- [ ] Per-child environment overrides.
- [ ] Per-child working directory.
- [ ] Piped standard streams.
- [ ] Owned binary output capture.
- [ ] Timeout/cancellation API.
- [ ] Windows CreateProcessW runtime.
- [ ] Large-output and simultaneous stdout/stderr regressions.
- [ ] Automatic Child scope cleanup.
- [ ] Complete target-native argv/status/termination/cleanup matrix.

### Networking / TLS

Evidence: [src/net.qz](../src/net.qz).

- [x] IPv4 addresses and DNS resolution.
- [x] TCP streams/listeners.
- [x] UDP datagrams.
- [x] Partial-send handling.
- [x] Bounded receive operations.
- [x] Exclusive socket shutdown/close lifecycle.
- [x] Structured NetError surface.
- [x] Deterministic transport/receiver regression fixtures.
- [ ] Timeout/deadline API.
- [ ] Common streaming-I/O integration.
- [ ] Maintained TLS transport backend.
- [ ] Certificate-chain verification.
- [ ] Hostname verification.
- [ ] Trust-store/protocol/update policy.
- [ ] Ownership-safe fully compiling HTTP Headers/request/response path.
- [ ] Defined concurrent socket-sharing policy.
- [ ] Target-native TCP/UDP/HTTP/TLS integration matrix.

### Mathematics

Evidence: [src/math.qz](../src/math.qz).

- [x] Integer GCD/LCM and combinatorics.
- [x] Basic scalar arithmetic helpers.
- [x] Rounding operations.
- [x] Angular conversions.
- [x] Roots and scaled hypot.
- [x] Trigonometric functions.
- [x] Exponential/logarithmic/power functions.
- [ ] Checked overflow policy across integer operations.
- [ ] Complete NaN/infinity/domain behavior audit.
- [ ] Quantified precision/error bounds.
- [ ] Comprehensive numeric edge-case regression suite.

### Panic handling

Evidence: companion compiler `quazistrap/prelude/src/panic.qz` and its panic-handler semantic tests.

- [x] Current termination-only behavior.
- [x] PanicInfo source/message payload.
- [x] Validated custom panic-handler signature.
- [x] Default source-location diagnostics.
- [x] Default exit status 101.
- [ ] Final custom-handler lifecycle/safety contract.
- [ ] Nested/recursive panic behavior.
- [ ] Thread/task panic interaction.
- [ ] Target-native custom-handler lifecycle regressions.
- [ ] Resolve the remaining D-006 panic policy.

### Concurrency

Evidence: [src/thread.qz](../src/thread.qz).

- [x] Linux/Windows native thread creation paths.
- [x] Explicit consuming join.
- [x] Result[Thread, ThreadError] creation failure.
- [x] Target-specific exported C callback ABI.
- [ ] Cancellation policy/API.
- [ ] Synchronization primitives.
- [ ] Defined communication surface.
- [ ] Typed thread result propagation.
- [ ] Panic propagation.
- [ ] Structured automatic joining/cleanup.
- [ ] Target-native lifetime/failure/synchronization matrix.
- [ ] Finalize D-007 model and terminology.

### Time

Evidence: [src/time.qz](../src/time.qz).

- [x] Normalized ns/us/ms/s Duration constructors.
- [x] Checked duration addition/subtraction.
- [x] Linux/Windows monotonic Instant backends.
- [x] Elapsed/duration_since with backwards-clock errors.
- [x] Deterministic duration/instant arithmetic regressions.
- [ ] Unit-safe minute/hour constructors.
- [ ] Wall-clock instants.
- [ ] Civil dates and times.
- [ ] Time zones.
- [ ] UTC offsets.
- [ ] Unix timestamps.
- [ ] Parsing.
- [ ] Formatting.
- [ ] General temporal comparison surface.
- [ ] Duration-based sleeping.
- [ ] Timers.
- [ ] Deadline abstraction.
- [ ] Leap-second/range/calendar policy.
- [ ] Time serialization.

### Serialization

Evidence: [src/codec.qz](../src/codec.qz).

- [x] Scalar Serialize trait implementations.
- [x] Compiler-generated Serialize metadata and initial field matrix.
- [x] Bounded JSON syntax validation.
- [x] Escaped Unicode JSON-string encoding/decoding.
- [x] Bounded bool/i64/String scalar decoding.
- [x] Bounded top-level object-field extraction.
- [ ] Ownership-safe JSON object composition under the current compiler.
- [ ] Derived Deserialize.
- [ ] Option field support.
- [ ] Collection field support.
- [ ] Nested struct support.
- [ ] Enum support.
- [ ] Wider numeric field matrix.
- [ ] Finalize missing/unknown/duplicate/default decode policy.
- [ ] Complete source/QZI/target-native codec regression matrix.

### Library-wide safety / other modules

Evidence: [AGENTS.md](../AGENTS.md).

- [x] Fallible concrete usize Map/Set.
- [x] Owning checked CString and explicit unsafe CStr.
- [x] Explicit unsafe raw pointer/count operations.
- [x] OS-backed secure random primitives.
- [x] Owned dynamic-library handles with unsafe symbol casts.
- [x] Owned text and local view migration.
- [ ] Sound generic hash/equality/drop-aware collections.
- [ ] Passing full standard-library suite including HTTP/JSON.
- [ ] Final public API/documentation/target consistency audit.

## Verification boundary

The source checklist is backed by current module declarations, tracked tests,
`AGENTS.md`, the companion compiler API reference, D-006/D-007/D-008/D-009,
D-012, and the 2026-10-13 compiler checkpoint. Current source has
`Result[Thread, ThreadError]`; older resume prose describing a zero-handle
high-level return is not used for the count.

Full standard-library compilation remains blocked by HTTP Headers/JSON
owned reads and unrelated user CLI work. JSON object composition and the full
library test gate therefore receive no completion credit. Process cleanup is
explicit: there is no automatic `Child.free` hook. Windows process creation,
portable cwd/environment mutation, buffered I/O, civil time, and TLS are absent.

The bounded receiver fixture excludes Headers/codec operations and does not
establish a full-module build or full HTTP round trip. See `docs/NETWORK.md`.

Current check: `python3 std/scripts/check_net_receivers.py quazistrap/target/debug/qz`
(from the workspace root) passed **10 native tests**, rejected **3 negative
lifetime probes with S10**, and passed QZI native execution plus Windows
COFF emission. The first sandboxed run could not create four local sockets;
the authorized run outside the sandbox passed. No Windows host execution
or full HTTP round trip is claimed.
