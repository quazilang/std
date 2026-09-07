# Networking

`std.net` is Quazi's cross-platform IPv4 TCP, UDP, and HTTP/1.1 module. Linux
uses socket syscalls; Windows uses Winsock. `SocketAddress` resolves DNS names;
`TcpStream`/`TcpListener` cover streams and servers; `UdpSocket` supports
connected datagrams plus `send_to`/`receive_from`.

Fully valid dotted-decimal IPv4 addresses are used directly without DNS lookup;
host names retain platform DNS resolution.

HTTP uses `Url`, `HttpMethod`, `Header`, `Headers`, `HttpRequest`, and
`HttpResponse`. Requests support arbitrary methods, headers, bodies, ports,
response limits, DNS hosts, encoding, sending, and server-side parsing.
Responses expose status/reason/headers/body and parse Content-Length or chunked
transfer encoding. Compatibility `http_get`/`http_post` helpers remain.

`HttpRequest.send_url(url)` routes the existing request to `url.host()` and
`url.port()` and replaces its request target with `url.path()`. It preserves
the chosen method, body, headers, and response limit. An explicitly supplied
`Host` header remains a deliberate virtual-host override; otherwise encoding
adds the URL authority, including a non-default HTTP port, as `Host`. `https`
URLs return `TlsUnavailable` rather than downgrading the connection.

Safe operations return `Result[T, NetError]`, not platform integers. Portable
variants include `ConnectionRefused`, `AddressInUse`, `TimedOut`,
`ConnectionReset`, and reachability/permission failures. `message()` returns
readable text. `Native(code)` preserves unexpected OS-specific failures.

HTTPS returns `TlsUnavailable`; HTTP over TLS needs a dedicated TLS transport.
Redirects, cookies, proxies, compression, and HTTP/2 are separate policy or
protocol layers. Handles close at scope exit and may be closed early. The
walkthrough is `examples/26-http-client-server` in the compiler repository.
