# `std.net`

std.net — structured IPv4 TCP, UDP, and HTTP/1.1 client/server APIs.
HTTPS goes through std.tls, which adds TLS on top of these TCP streams.

## Contents

- [Functions](#functions)
- [`NetError`](#neterror) (enum)
- [`SocketAddress`](#socketaddress) (struct)
- [`Shutdown`](#shutdown) (enum)
- [`TcpStream`](#tcpstream) (struct)
- [`TcpListener`](#tcplistener) (struct)
- [`UdpDatagram`](#udpdatagram) (struct)
- [`UdpSocket`](#udpsocket) (struct)
- [`Header`](#header) (struct)
- [`Headers`](#headers) (struct)
- [`HttpMethod`](#httpmethod) (enum)
- [`Url`](#url) (struct)
- [`HttpRequest`](#httprequest) (struct)
- [`HttpResponse`](#httpresponse) (struct)
- [`HttpConnection`](#httpconnection) (struct)
- [`HttpServer`](#httpserver) (struct)

## Functions

### `http_request`

```quazi
pub fn http_request(host: str, port: i32, method: str, path: str, body: str) Result[String, NetError]
```

Compatibility helpers. New code should construct HttpRequest and inspect HttpResponse.

### `http_get`

```quazi
pub fn http_get(host: str, port: i32, path: str) Result[String, NetError]
```

Sends an HTTP/1.1 GET for `path` to `host:port` (plain TCP, no TLS) and
returns the response body.

### `http_post`

```quazi
pub fn http_post(host: str, port: i32, path: str, body: str) Result[String, NetError]
```

Sends an HTTP/1.1 POST of `body` and returns the response body.

## `NetError`

```quazi
pub enum NetError {
    InvalidAddress,
    InvalidPort,
    InvalidUrl,
    InvalidHttp,
    NameResolutionFailed,
    ConnectionRefused,
    AddressInUse,
    AddressNotAvailable,
    TimedOut,
    ConnectionReset,
    NotConnected,
    WouldBlock,
    NetworkUnreachable,
    HostUnreachable,
    PermissionDenied,
    BrokenPipe,
    MessageTooLarge,
    LimitExceeded,
    AllocationFailed,
    InvalidUtf8,
    TlsUnavailable,
    Unsupported,
    InvalidTimeout,
    Native(i32),
}
```

Why a network operation failed.

### `NetError.message`

```quazi
pub fn message(self: NetError) str
```

A short English description of the error, for display.

## `SocketAddress`

```quazi
pub struct SocketAddress { /* internal fields */ }
```

A host name or IPv4 address with a port.

### `SocketAddress.new`

```quazi
pub fn new(host: str, port: i32) Result[SocketAddress, NetError]
```

An address for `host` and `port` (checked, not yet resolved).

### `SocketAddress.host`

```quazi
pub fn host(self: &SocketAddress) str
```

The host text.

### `SocketAddress.port`

```quazi
pub fn port(self: &SocketAddress) i32
```

The port.

### `SocketAddress.resolve`

```quazi
pub fn resolve(self: &SocketAddress) Result[SocketAddress, NetError]
```

The address with the host resolved to an IPv4 address (DNS).

## `Shutdown`

```quazi
pub enum Shutdown { Read, Write, Both }
```

Which direction of a TCP connection `shutdown` closes.

## `TcpStream`

```quazi
pub struct TcpStream { /* internal fields */ }
```

A TCP connection; closed automatically at the end of scope.

### `TcpStream.connect`

```quazi
pub fn connect(host: str, port: i32) Result[TcpStream, NetError]
```

Connects to `host:port` (the host is resolved first).

### `TcpStream.send`

```quazi
pub fn send(self: &TcpStream!, text: str) Result[usize, NetError]
```

Sends `text`; returns the number of bytes sent.

### `TcpStream.send_bytes`

```quazi
pub fn send_bytes(self: &TcpStream!, data: bytes) Result[usize, NetError]
```

Sends `data`; returns the number of bytes sent.

### `TcpStream.send_raw`

```quazi
pub fn send_raw(self: &TcpStream!, data: *u8, length: usize) Result[usize, NetError]
```

Unsafe-style raw send of `length` bytes at `data`.

### `TcpStream.recv`

```quazi
pub fn recv(self: &TcpStream!, data: *u8, length: usize) isize
```

Raw receive into `data`; returns the byte count, 0 at end, negative on
error.

### `TcpStream.receive`

```quazi
pub fn receive(self: &TcpStream!, limit: usize) Result[String, NetError]
```

Receives what is available, at most `limit` bytes, as UTF-8 text.

### `TcpStream.receive_all`

```quazi
pub fn receive_all(self: &TcpStream!, limit: usize) Result[String, NetError]
```

Receives until the peer closes the connection, at most `limit` bytes.

### `TcpStream.set_read_timeout`

```quazi
pub fn set_read_timeout(self: &TcpStream!, timeout: Option[Duration]) Result[bool, NetError]
```

Fail blocking receives with TimedOut after `timeout`; None waits forever.

### `TcpStream.set_write_timeout`

```quazi
pub fn set_write_timeout(self: &TcpStream!, timeout: Option[Duration]) Result[bool, NetError]
```

Fail blocking sends with TimedOut after `timeout`; None waits forever.

### `TcpStream.shutdown`

```quazi
pub fn shutdown(self: &TcpStream!, how: Shutdown) Result[bool, NetError]
```

Closes reading, writing or both directions.

### `TcpStream.close`

```quazi
pub fn close(self: &TcpStream!) void
```

Closes the connection now.

### `TcpStream.free`

```quazi
pub fn free(self: TcpStream) void
```

Closes the connection; called automatically at the end of scope.

### `TcpStream.handle`

```quazi
pub fn handle(self: &TcpStream) isize
```

The native socket handle.

## `TcpListener`

```quazi
pub struct TcpListener { /* internal fields */ }
```

A TCP server socket listening on a port.

### `TcpListener.bind`

```quazi
pub fn bind(port: i32) Result[TcpListener, NetError]
```

Listens on `port` on all IPv4 interfaces.

### `TcpListener.bind_with_backlog`

```quazi
pub fn bind_with_backlog(port: i32, backlog: i32) Result[TcpListener, NetError]
```

Like `bind`, with a pending-connection queue of `backlog`.

### `TcpListener.accept`

```quazi
pub fn accept(self: &TcpListener!) Result[TcpStream, NetError]
```

Waits for the next connection.

### `TcpListener.close`

```quazi
pub fn close(self: &TcpListener!) void
```

Stops listening now.

### `TcpListener.free`

```quazi
pub fn free(self: TcpListener) void
```

Stops listening; called automatically at the end of scope.

### `TcpListener.handle`

```quazi
pub fn handle(self: &TcpListener) isize
```

The native socket handle.

## `UdpDatagram`

```quazi
pub struct UdpDatagram { /* internal fields */ }
```

A received datagram with its sender.

### `UdpDatagram.text`

```quazi
pub fn text(self: &UdpDatagram) str
```

The datagram contents as text.

### `UdpDatagram.address`

```quazi
pub fn address(self: &UdpDatagram) SocketAddress
```

Return a copy of the sender address; the datagram stays usable.

## `UdpSocket`

```quazi
pub struct UdpSocket { /* internal fields */ }
```

A UDP socket.

### `UdpSocket.bind`

```quazi
pub fn bind(port: i32) Result[UdpSocket, NetError]
```

A socket receiving on `port`.

### `UdpSocket.connect`

```quazi
pub fn connect(host: str, port: i32) Result[UdpSocket, NetError]
```

A socket whose `send` and `receive` use `host:port`.

### `UdpSocket.send`

```quazi
pub fn send(self: &UdpSocket!, text: str) Result[usize, NetError]
```

Sends `text` to the connected address.

### `UdpSocket.send_to`

```quazi
pub fn send_to(self: &UdpSocket!, text: str, address: SocketAddress) Result[usize, NetError]
```

Sends `text` to `address`.

### `UdpSocket.set_read_timeout`

```quazi
pub fn set_read_timeout(self: &UdpSocket!, timeout: Option[Duration]) Result[bool, NetError]
```

Limits how long `receive` waits (`None`: forever).

### `UdpSocket.set_write_timeout`

```quazi
pub fn set_write_timeout(self: &UdpSocket!, timeout: Option[Duration]) Result[bool, NetError]
```

Limits how long sending waits (`None`: forever).

### `UdpSocket.receive`

```quazi
pub fn receive(self: &UdpSocket!, limit: usize) Result[String, NetError]
```

Receives one datagram, at most `limit` bytes, as text.

### `UdpSocket.receive_from`

```quazi
pub fn receive_from(self: &UdpSocket!, limit: usize) Result[UdpDatagram, NetError]
```

Receives one datagram together with its sender.

### `UdpSocket.close`

```quazi
pub fn close(self: &UdpSocket!) void
```

Closes the socket now.

### `UdpSocket.free`

```quazi
pub fn free(self: UdpSocket) void
```

Closes the socket; called automatically at the end of scope.

### `UdpSocket.handle`

```quazi
pub fn handle(self: &UdpSocket) isize
```

The native socket handle.

## `Header`

```quazi
pub struct Header { /* internal fields */ }
```

One HTTP header line (name and value).

### `Header.new`

```quazi
pub fn new(name: str, value: str) Header
```

A header `name: value`.

### `Header.name`

```quazi
pub fn name(self: &Header) str
```

The header name.

### `Header.value`

```quazi
pub fn value(self: &Header) str
```

The header value.

## `Headers`

```quazi
pub struct Headers { /* internal fields */ }
```

Headers keep their HTTP wire encoding (`Name: value\r\n` per field) in one
owned buffer. Accessors return owned copies, so no caller can retain a view
into storage that a later `set` or `append` replaces.

### `Headers.new`

```quazi
pub fn new() Headers
```

An empty header list.

### `Headers.append`

```quazi
pub fn append(self: &Headers!, name: str, value: str) void
```

Adds a header (repeated names are kept).

### `Headers.set`

```quazi
pub fn set(self: &Headers!, name: str, value: str) void
```

Replace the first field named `name` (ASCII case-insensitive), or append it.

### `Headers.get`

```quazi
pub fn get(self: &Headers, name: str) Option[String]
```

Return a copy of the first value named `name` (ASCII case-insensitive).

### `Headers.contains`

```quazi
pub fn contains(self: &Headers, name: str) bool
```

Whether a header `name` exists (case-insensitive).

### `Headers.len`

```quazi
pub fn len(self: &Headers) usize
```

The number of headers.

### `Headers.get_at`

```quazi
pub fn get_at(self: &Headers, index: usize) Header
```

Return a copy of the field at `index`; panics when `index >= len()`.

### `Headers.copy`

```quazi
pub fn copy(self: &Headers) Headers
```

An owned copy of the list.

### `Headers.encode`

```quazi
pub fn encode(self: &Headers) String
```

The headers as HTTP text lines.

## `HttpMethod`

```quazi
pub enum HttpMethod { Get, Head, Post, Put, Patch, Delete, Options, Connect, Trace }
```

An HTTP request method.

### `HttpMethod.name`

```quazi
pub fn name(self: HttpMethod) str
```

The method token, such as `GET`.

## `Url`

```quazi
pub struct Url { /* internal fields */ }
```

A parsed `http://host:port/path` (or `https`) URL.

### `Url.parse`

```quazi
pub fn parse(text: str) Result[Url, NetError]
```

Parses an `http://` or `https://` URL (send `https` requests with
`std.tls.send_url`).

### `Url.scheme`

```quazi
pub fn scheme(self: &Url) str
```

The scheme (`http` or `https`).

### `Url.host`

```quazi
pub fn host(self: &Url) str
```

The host.

### `Url.port`

```quazi
pub fn port(self: &Url) i32
```

The port (80, or 443 for `https`, when not written).

### `Url.path`

```quazi
pub fn path(self: &Url) str
```

The path with query (`/` when empty).

## `HttpRequest`

```quazi
pub struct HttpRequest { /* internal fields */ }
```

An HTTP/1.1 request, built with chained setters and sent with `send`.

### `HttpRequest.new`

```quazi
pub fn new(method: str, target: str, host: str) HttpRequest
```

A request with method text `method`, target path and `Host`.

### `HttpRequest.with_method`

```quazi
pub fn with_method(method: HttpMethod, target: str, host: str) HttpRequest
```

A request with an `HttpMethod`.

### `HttpRequest.from_url`

```quazi
pub fn from_url(method: HttpMethod, url: Url) HttpRequest
```

A request for `url`'s host and path.

### `HttpRequest.header`

```quazi
pub fn header(self: HttpRequest, name: str, value: str) HttpRequest
```

Adds a header.

### `HttpRequest.body`

```quazi
pub fn body(self: HttpRequest, body: str) HttpRequest
```

Sets the body (and `Content-Length`).

### `HttpRequest.max_response_bytes`

```quazi
pub fn max_response_bytes(self: HttpRequest, limit: usize) HttpRequest
```

Limits the response size `send` accepts.

### `HttpRequest.response_limit`

```quazi
pub fn response_limit(self: &HttpRequest) usize
```

The largest response `send` reads, in bytes.

### `HttpRequest.route`

```quazi
pub fn route(self: HttpRequest, target: str, host: str) HttpRequest
```

Sends to `host` with request target `target`, keeping the method,
headers, body and response limit.

### `HttpRequest.method`

```quazi
pub fn method(self: &HttpRequest) str
```

The method token.

### `HttpRequest.target`

```quazi
pub fn target(self: &HttpRequest) str
```

The request target (path).

### `HttpRequest.host`

```quazi
pub fn host(self: &HttpRequest) str
```

The host.

### `HttpRequest.headers`

```quazi
pub fn headers(self: &HttpRequest) Headers
```

A copy of the headers.

### `HttpRequest.body_text`

```quazi
pub fn body_text(self: &HttpRequest) str
```

The body.

### `HttpRequest.encode`

```quazi
pub fn encode(self: &HttpRequest) String
```

The request as HTTP text.

### `HttpRequest.send`

```quazi
pub fn send(self: HttpRequest, port: i32) Result[HttpResponse, NetError]
```

Sends the request to the host on `port` and reads the response (plain
TCP, no TLS).

### `HttpRequest.send_url`

```quazi
pub fn send_url(self: HttpRequest, url: Url) Result[HttpResponse, NetError]
```

Sends the request to `url`'s host and port.

### `HttpRequest.parse`

```quazi
pub fn parse(raw: String) Result[HttpRequest, NetError]
```

Parses raw HTTP request text (server side).

## `HttpResponse`

```quazi
pub struct HttpResponse { /* internal fields */ }
```

An HTTP/1.1 response.

### `HttpResponse.new`

```quazi
pub fn new(status: i32, reason: str, body: str) HttpResponse
```

A response with `status`, reason phrase and body.

### `HttpResponse.text`

```quazi
pub fn text(status: i32, body: str) HttpResponse
```

A `text/plain` response with the standard reason phrase.

### `HttpResponse.header`

```quazi
pub fn header(self: HttpResponse, name: str, value: str) HttpResponse
```

Adds a header.

### `HttpResponse.status`

```quazi
pub fn status(self: &HttpResponse) i32
```

The status code.

### `HttpResponse.reason`

```quazi
pub fn reason(self: &HttpResponse) str
```

The reason phrase.

### `HttpResponse.headers`

```quazi
pub fn headers(self: &HttpResponse) Headers
```

A copy of the headers.

### `HttpResponse.body`

```quazi
pub fn body(self: &HttpResponse) str
```

The body.

### `HttpResponse.encode`

```quazi
pub fn encode(self: &HttpResponse) String
```

The response as HTTP text.

### `HttpResponse.parse`

```quazi
pub fn parse(raw: String) Result[HttpResponse, NetError]
```

Parses raw HTTP response text.

## `HttpConnection`

```quazi
pub struct HttpConnection { /* internal fields */ }
```

A client connection accepted by `HttpServer`.

### `HttpConnection.read`

```quazi
pub fn read(self: &HttpConnection!, limit: usize) Result[HttpRequest, NetError]
```

Reads and parses one request of at most `limit` bytes.

### `HttpConnection.read_request`

```quazi
pub fn read_request(self: &HttpConnection!, limit: usize) Result[String, NetError]
```

Reads one raw request of at most `limit` bytes.

### `HttpConnection.respond`

```quazi
pub fn respond(self: &HttpConnection!, response: HttpResponse) Result[usize, NetError]
```

Sends `response`.

### `HttpConnection.close`

```quazi
pub fn close(self: &HttpConnection!) void
```

Closes the connection.

## `HttpServer`

```quazi
pub struct HttpServer { /* internal fields */ }
```

A minimal HTTP/1.1 server (one connection at a time, no TLS).

### `HttpServer.bind`

```quazi
pub fn bind(port: i32) Result[HttpServer, NetError]
```

Listens on `port`.

### `HttpServer.accept`

```quazi
pub fn accept(self: &HttpServer!) Result[HttpConnection, NetError]
```

Waits for the next client.

### `HttpServer.close`

```quazi
pub fn close(self: &HttpServer!) void
```

Stops listening now.

### `HttpServer.free`

```quazi
pub fn free(self: HttpServer) void
```

Stops listening; called automatically at the end of scope.

### `HttpServer.serve_once`

```quazi
pub fn serve_once(self: HttpServer, response: HttpResponse, limit: usize) Result[String, NetError]
```

Accepts one client, reads its request (at most `limit` bytes), answers
with `response` and returns the raw request.
