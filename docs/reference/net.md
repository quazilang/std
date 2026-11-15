# `std.net`

std.net — structured IPv4 TCP, UDP, and HTTP/1.1 client/server APIs.
HTTPS intentionally stays separate: transport security requires a TLS module.

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

_Undocumented._

### `http_post`

```quazi
pub fn http_post(host: str, port: i32, path: str, body: str) Result[String, NetError]
```

_Undocumented._

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

_Undocumented._

### `NetError.message`

```quazi
pub fn message(self: NetError) str
```

_Undocumented._

## `SocketAddress`

```quazi
pub struct SocketAddress { /* internal fields */ }
```

_Undocumented._

### `SocketAddress.new`

```quazi
pub fn new(host: str, port: i32) Result[SocketAddress, NetError]
```

_Undocumented._

### `SocketAddress.host`

```quazi
pub fn host(self: &SocketAddress) str
```

_Undocumented._

### `SocketAddress.port`

```quazi
pub fn port(self: &SocketAddress) i32
```

_Undocumented._

### `SocketAddress.resolve`

```quazi
pub fn resolve(self: &SocketAddress) Result[SocketAddress, NetError]
```

_Undocumented._

## `Shutdown`

```quazi
pub enum Shutdown { Read, Write, Both }
```

_Undocumented._

## `TcpStream`

```quazi
pub struct TcpStream { /* internal fields */ }
```

_Undocumented._

### `TcpStream.connect`

```quazi
pub fn connect(host: str, port: i32) Result[TcpStream, NetError]
```

_Undocumented._

### `TcpStream.send`

```quazi
pub fn send(self: &TcpStream!, text: str) Result[usize, NetError]
```

_Undocumented._

### `TcpStream.send_bytes`

```quazi
pub fn send_bytes(self: &TcpStream!, data: bytes) Result[usize, NetError]
```

_Undocumented._

### `TcpStream.send_raw`

```quazi
pub fn send_raw(self: &TcpStream!, data: *u8, length: usize) Result[usize, NetError]
```

_Undocumented._

### `TcpStream.recv`

```quazi
pub fn recv(self: &TcpStream!, data: *u8, length: usize) isize
```

_Undocumented._

### `TcpStream.receive`

```quazi
pub fn receive(self: &TcpStream!, limit: usize) Result[String, NetError]
```

_Undocumented._

### `TcpStream.receive_all`

```quazi
pub fn receive_all(self: &TcpStream!, limit: usize) Result[String, NetError]
```

_Undocumented._

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

_Undocumented._

### `TcpStream.close`

```quazi
pub fn close(self: &TcpStream!) void
```

_Undocumented._

### `TcpStream.free`

```quazi
pub fn free(self: TcpStream) void
```

_Undocumented._

### `TcpStream.handle`

```quazi
pub fn handle(self: &TcpStream) isize
```

_Undocumented._

## `TcpListener`

```quazi
pub struct TcpListener { /* internal fields */ }
```

_Undocumented._

### `TcpListener.bind`

```quazi
pub fn bind(port: i32) Result[TcpListener, NetError]
```

_Undocumented._

### `TcpListener.bind_with_backlog`

```quazi
pub fn bind_with_backlog(port: i32, backlog: i32) Result[TcpListener, NetError]
```

_Undocumented._

### `TcpListener.accept`

```quazi
pub fn accept(self: &TcpListener!) Result[TcpStream, NetError]
```

_Undocumented._

### `TcpListener.close`

```quazi
pub fn close(self: &TcpListener!) void
```

_Undocumented._

### `TcpListener.free`

```quazi
pub fn free(self: TcpListener) void
```

_Undocumented._

### `TcpListener.handle`

```quazi
pub fn handle(self: &TcpListener) isize
```

_Undocumented._

## `UdpDatagram`

```quazi
pub struct UdpDatagram { /* internal fields */ }
```

_Undocumented._

### `UdpDatagram.text`

```quazi
pub fn text(self: &UdpDatagram) str
```

_Undocumented._

### `UdpDatagram.address`

```quazi
pub fn address(self: &UdpDatagram) SocketAddress
```

Return a copy of the sender address; the datagram stays usable.

## `UdpSocket`

```quazi
pub struct UdpSocket { /* internal fields */ }
```

_Undocumented._

### `UdpSocket.bind`

```quazi
pub fn bind(port: i32) Result[UdpSocket, NetError]
```

_Undocumented._

### `UdpSocket.connect`

```quazi
pub fn connect(host: str, port: i32) Result[UdpSocket, NetError]
```

_Undocumented._

### `UdpSocket.send`

```quazi
pub fn send(self: &UdpSocket!, text: str) Result[usize, NetError]
```

_Undocumented._

### `UdpSocket.send_to`

```quazi
pub fn send_to(self: &UdpSocket!, text: str, address: SocketAddress) Result[usize, NetError]
```

_Undocumented._

### `UdpSocket.set_read_timeout`

```quazi
pub fn set_read_timeout(self: &UdpSocket!, timeout: Option[Duration]) Result[bool, NetError]
```

_Undocumented._

### `UdpSocket.set_write_timeout`

```quazi
pub fn set_write_timeout(self: &UdpSocket!, timeout: Option[Duration]) Result[bool, NetError]
```

_Undocumented._

### `UdpSocket.receive`

```quazi
pub fn receive(self: &UdpSocket!, limit: usize) Result[String, NetError]
```

_Undocumented._

### `UdpSocket.receive_from`

```quazi
pub fn receive_from(self: &UdpSocket!, limit: usize) Result[UdpDatagram, NetError]
```

_Undocumented._

### `UdpSocket.close`

```quazi
pub fn close(self: &UdpSocket!) void
```

_Undocumented._

### `UdpSocket.free`

```quazi
pub fn free(self: UdpSocket) void
```

_Undocumented._

### `UdpSocket.handle`

```quazi
pub fn handle(self: &UdpSocket) isize
```

_Undocumented._

## `Header`

```quazi
pub struct Header { /* internal fields */ }
```

_Undocumented._

### `Header.new`

```quazi
pub fn new(name: str, value: str) Header
```

_Undocumented._

### `Header.name`

```quazi
pub fn name(self: &Header) str
```

_Undocumented._

### `Header.value`

```quazi
pub fn value(self: &Header) str
```

_Undocumented._

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

_Undocumented._

### `Headers.append`

```quazi
pub fn append(self: &Headers!, name: str, value: str) void
```

_Undocumented._

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

_Undocumented._

### `Headers.len`

```quazi
pub fn len(self: &Headers) usize
```

_Undocumented._

### `Headers.get_at`

```quazi
pub fn get_at(self: &Headers, index: usize) Header
```

Return a copy of the field at `index`; panics when `index >= len()`.

### `Headers.copy`

```quazi
pub fn copy(self: &Headers) Headers
```

_Undocumented._

### `Headers.encode`

```quazi
pub fn encode(self: &Headers) String
```

_Undocumented._

## `HttpMethod`

```quazi
pub enum HttpMethod { Get, Head, Post, Put, Patch, Delete, Options, Connect, Trace }
```

_Undocumented._

### `HttpMethod.name`

```quazi
pub fn name(self: HttpMethod) str
```

_Undocumented._

## `Url`

```quazi
pub struct Url { /* internal fields */ }
```

_Undocumented._

### `Url.parse`

```quazi
pub fn parse(text: str) Result[Url, NetError]
```

_Undocumented._

### `Url.scheme`

```quazi
pub fn scheme(self: &Url) str
```

_Undocumented._

### `Url.host`

```quazi
pub fn host(self: &Url) str
```

_Undocumented._

### `Url.port`

```quazi
pub fn port(self: &Url) i32
```

_Undocumented._

### `Url.path`

```quazi
pub fn path(self: &Url) str
```

_Undocumented._

## `HttpRequest`

```quazi
pub struct HttpRequest { /* internal fields */ }
```

_Undocumented._

### `HttpRequest.new`

```quazi
pub fn new(method: str, target: str, host: str) HttpRequest
```

_Undocumented._

### `HttpRequest.with_method`

```quazi
pub fn with_method(method: HttpMethod, target: str, host: str) HttpRequest
```

_Undocumented._

### `HttpRequest.from_url`

```quazi
pub fn from_url(method: HttpMethod, url: Url) HttpRequest
```

_Undocumented._

### `HttpRequest.header`

```quazi
pub fn header(self: HttpRequest, name: str, value: str) HttpRequest
```

_Undocumented._

### `HttpRequest.body`

```quazi
pub fn body(self: HttpRequest, body: str) HttpRequest
```

_Undocumented._

### `HttpRequest.max_response_bytes`

```quazi
pub fn max_response_bytes(self: HttpRequest, limit: usize) HttpRequest
```

_Undocumented._

### `HttpRequest.method`

```quazi
pub fn method(self: &HttpRequest) str
```

_Undocumented._

### `HttpRequest.target`

```quazi
pub fn target(self: &HttpRequest) str
```

_Undocumented._

### `HttpRequest.host`

```quazi
pub fn host(self: &HttpRequest) str
```

_Undocumented._

### `HttpRequest.headers`

```quazi
pub fn headers(self: &HttpRequest) Headers
```

_Undocumented._

### `HttpRequest.body_text`

```quazi
pub fn body_text(self: &HttpRequest) str
```

_Undocumented._

### `HttpRequest.encode`

```quazi
pub fn encode(self: &HttpRequest) String
```

_Undocumented._

### `HttpRequest.send`

```quazi
pub fn send(self: HttpRequest, port: i32) Result[HttpResponse, NetError]
```

_Undocumented._

### `HttpRequest.send_url`

```quazi
pub fn send_url(self: HttpRequest, url: Url) Result[HttpResponse, NetError]
```

_Undocumented._

### `HttpRequest.parse`

```quazi
pub fn parse(raw: String) Result[HttpRequest, NetError]
```

_Undocumented._

## `HttpResponse`

```quazi
pub struct HttpResponse { /* internal fields */ }
```

_Undocumented._

### `HttpResponse.new`

```quazi
pub fn new(status: i32, reason: str, body: str) HttpResponse
```

_Undocumented._

### `HttpResponse.text`

```quazi
pub fn text(status: i32, body: str) HttpResponse
```

_Undocumented._

### `HttpResponse.header`

```quazi
pub fn header(self: HttpResponse, name: str, value: str) HttpResponse
```

_Undocumented._

### `HttpResponse.status`

```quazi
pub fn status(self: &HttpResponse) i32
```

_Undocumented._

### `HttpResponse.reason`

```quazi
pub fn reason(self: &HttpResponse) str
```

_Undocumented._

### `HttpResponse.headers`

```quazi
pub fn headers(self: &HttpResponse) Headers
```

_Undocumented._

### `HttpResponse.body`

```quazi
pub fn body(self: &HttpResponse) str
```

_Undocumented._

### `HttpResponse.encode`

```quazi
pub fn encode(self: &HttpResponse) String
```

_Undocumented._

### `HttpResponse.parse`

```quazi
pub fn parse(raw: String) Result[HttpResponse, NetError]
```

_Undocumented._

## `HttpConnection`

```quazi
pub struct HttpConnection { /* internal fields */ }
```

_Undocumented._

### `HttpConnection.read`

```quazi
pub fn read(self: &HttpConnection!, limit: usize) Result[HttpRequest, NetError]
```

_Undocumented._

### `HttpConnection.read_request`

```quazi
pub fn read_request(self: &HttpConnection!, limit: usize) Result[String, NetError]
```

_Undocumented._

### `HttpConnection.respond`

```quazi
pub fn respond(self: &HttpConnection!, response: HttpResponse) Result[usize, NetError]
```

_Undocumented._

### `HttpConnection.close`

```quazi
pub fn close(self: &HttpConnection!) void
```

_Undocumented._

## `HttpServer`

```quazi
pub struct HttpServer { /* internal fields */ }
```

_Undocumented._

### `HttpServer.bind`

```quazi
pub fn bind(port: i32) Result[HttpServer, NetError]
```

_Undocumented._

### `HttpServer.accept`

```quazi
pub fn accept(self: &HttpServer!) Result[HttpConnection, NetError]
```

_Undocumented._

### `HttpServer.close`

```quazi
pub fn close(self: &HttpServer!) void
```

_Undocumented._

### `HttpServer.free`

```quazi
pub fn free(self: HttpServer) void
```

_Undocumented._

### `HttpServer.serve_once`

```quazi
pub fn serve_once(self: HttpServer, response: HttpResponse, limit: usize) Result[String, NetError]
```

_Undocumented._
