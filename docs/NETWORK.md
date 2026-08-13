# Networking

`std.net` is Quazi's cross-platform IPv4 TCP, UDP, and HTTP/1.1 module. Linux
uses socket syscalls; Windows uses Winsock. `SocketAddress` resolves DNS names;
`TcpStream`/`TcpListener` cover streams and servers; `UdpSocket` supports
connected datagrams plus `send_to`/`receive_from`.

HTTP uses `Url`, `HttpMethod`, `Header`, `Headers`, `HttpRequest`, and
`HttpResponse`. Requests support arbitrary methods, headers, bodies, ports,
response limits, DNS hosts, encoding, sending, and server-side parsing.
Responses expose status/reason/headers/body and parse Content-Length or chunked
transfer encoding. Compatibility `http_get`/`http_post` helpers remain.

Safe operations return `Result[T, NetError]`, not platform integers. Portable
variants include `ConnectionRefused`, `AddressInUse`, `TimedOut`,
`ConnectionReset`, and reachability/permission failures. `message()` returns
readable text. `Native(code)` preserves unexpected OS-specific failures.

HTTPS returns `TlsUnavailable`; HTTP over TLS needs a dedicated TLS transport.
Redirects, cookies, proxies, compression, and HTTP/2 are separate policy or
protocol layers. Handles close at scope exit and may be closed early. The
walkthrough is `examples/26-http-client-server` in the compiler repository.
