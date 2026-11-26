# Networking

`std.net` is Quazi's cross-platform IPv4 TCP, UDP, and HTTP/1.1 module. Linux
and NetBSD use sockets (Linux name resolution goes through libc: set
`[target.x86_64-linux.link] libc = true`); Windows uses Winsock. `SocketAddress` resolves DNS names;
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
URLs return `TlsUnavailable` rather than downgrading the connection; send them
with `std.tls.send_url`.

Safe operations return `Result[T, NetError]`, not platform integers. Portable
variants include `ConnectionRefused`, `AddressInUse`, `TimedOut`,
`ConnectionReset`, and reachability/permission failures. `message()` returns
readable text. `Native(code)` preserves unexpected OS-specific failures.

Redirects, cookies, proxies, compression, and HTTP/2 are separate policy or
protocol layers. Handles close at scope exit and may be closed early. The
walkthrough is `examples/26-http-client-server` in the compiler repository.

## Sharing sockets between qoroutines and threads

Sockets follow D-014 (companion compiler
`docs/decisions/whole-program-ownership.md`)
ownership: every `TcpStream`, `TcpListener`, `UdpSocket` and `TlsStream` has
one owner, and every I/O operation takes an exclusive receiver, so two pieces
of code never use one socket at the same time. To use a socket concurrently,
move its owner into the qoroutine that does the I/O (`qo serve(stream)`) and
exchange data with other qoroutines through `Channel[T]`; the qoroutine closes
the socket when it ends. A socket borrowed into `qo` (`qo f(&stream!)`) stays
borrowed for the rest of the spawning scope: the spawner can no longer use or
close it. OS threads receive only raw `ThreadCallback` arguments, so a socket
handed to one goes through `handle()` in unsafe code and the caller keeps the
whole lifetime contract. There are no cloned handles or split read/write
halves; full-duplex use from two qoroutines needs a single owner that
multiplexes. `tests/net_receivers.qz` checks the move-into-qoroutine case.

## TLS

`std.tls` implements D-008 (В30А): the system TLS library and trust store.
On Linux it binds OpenSSL 3, so a program that calls it links libc and the
system libraries:

```toml
[target.x86_64-linux.link]
libc = true
libraries = ["ssl", "crypto"]
```

`TlsStream.connect(host, port)` verifies the certificate chain against the
system store and the certificate against `host` (DNS name or IPv4 address;
SNI is sent for names). `TlsStream.connect_with(host, port, &config)` takes a
`TlsConfig`: `TlsConfig.system()` or `TlsConfig.with_ca_file(path)` for a
private CA (that file replaces the system store). There is no way to turn
verification off. TLS 1.2 is the minimum version; protocol and cipher updates
come with the system library. `send`, `send_bytes`, `receive` and
`receive_all` mirror `TcpStream`; `receive_all` succeeds only after the peer's
close_notify, so a cut connection is a `ProtocolError` rather than a short
response. Writes block SIGPIPE for the calling thread, so a closed peer is an
error rather than a killed process; close_notify is skipped after a fatal
error. Streams send close_notify and release the session at scope exit.

`tls.send_url(request, url)` and `send_url_with(request, url, &config)` send
an `HttpRequest` to an `https` URL like `HttpRequest.send_url`, adding the
port to `Host` when it is not 443. Errors are `TlsError`: `Net(NetError)` for
the TCP layer, `UntrustedCertificate(code)`, `HostnameMismatch`,
`TrustStoreUnavailable`, `HandshakeFailed(code)`, `ProtocolError(code)` and
the usual limit/UTF-8 cases.

Windows uses Schannel (TLS 1.2) and verifies the server itself with the
certificate chain API: the chain must end at a root of the system store or,
with a CA file, at one of that file's PEM certificates, and the SSL policy
checks the host name (В32А, 2026-11-26; checked under Wine 11). NetBSD is not
implemented yet and returns `TlsError.Unsupported`. `scripts/check_tls.py` builds a client and runs it
against a local Python TLS server with a throwaway CA: trusted CA, untrusted
system store, wrong host name, missing CA file, truncation, a peer that closes
while the client writes, and a refused connection; `--wine WINE` runs the
same matrix with the Windows client under Wine.

## Receiver migration checkpoint

Datagram text and HTTP value accessors borrow their owners. HTTP connection
read/respond/close and server accept/close operations require mutable locals
and exclusive access; `serve_once` and server `free` remain consuming.

`Headers` keeps fields in one owned wire-format buffer: `append`/`set` take an
exclusive receiver, lookups are shared and return owned copies (`get` returns
`Option[String]`). Request/response `headers()` and `encode()` copy the headers
instead of moving fields, and `UdpDatagram.address()` returns a copy. The whole
module passes ownership analysis. Run the bounded transport/receiver check from
the workspace root with the matching compiler:

```sh
python3 std/scripts/check_net_receivers.py quazistrap/target/debug/qz
```

The check isolates exact production declarations; the full HTTP round trip is
covered by `examples/26-http-client-server` in the compiler repository. Canonical contracts and limitations
are recorded in the companion compiler's `docs/api/net.md` and
`docs/migrations/http-receivers.md`. The canonical repository is
[quazilang/quazistrap](https://github.com/quazilang/quazistrap); the migration
checkpoint remains local until publication is separately authorized.
