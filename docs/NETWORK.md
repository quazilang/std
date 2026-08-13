# Networking

`std.net` is Quazi's cross-platform TCP and HTTP/1.1 module. Linux uses socket
syscalls; Windows uses Winsock. Public operations cover client connections,
local bind/listen/accept, complete sends, bounded receives, HTTP requests, and
one-request local-server responses.

Safe operations return `Result[T, NetError]`, not platform integers. Portable
variants include `ConnectionRefused`, `AddressInUse`, `TimedOut`,
`ConnectionReset`, and reachability/permission failures. `message()` returns
readable text. `Native(code)` preserves unexpected OS-specific failures.

HTTPS is not supported without a TLS implementation. Callers must keep receive
limits explicit and close sockets on success and error paths. The executable
client/server walkthrough is in the compiler repository's `examples/26-http-client-server`.
