# `std.tls`

std.tls — TLS client streams over std.net TCP, backed by the system TLS
library (D-008).

Linux uses the system OpenSSL 3 (`libssl`/`libcrypto`) and its trust store.
Programs that call into this module must link those libraries and libc:

    [target.x86_64-linux.link]
    libc = true
    libraries = ["ssl", "crypto"]

Certificate and host-name verification are always on; TLS 1.2 is the
minimum protocol version. Other targets return `TlsError.Unsupported`.

## Contents

- [Functions](#functions)
- [`TlsError`](#tlserror) (enum)
- [`TlsConfig`](#tlsconfig) (struct)
- [`TlsStream`](#tlsstream) (struct)

## Functions

### `send_url_with`

```quazi
pub fn send_url_with(request: HttpRequest, url: Url, config: &TlsConfig) Result[HttpResponse, TlsError]
```

Sends `request` to an `https` `url` and reads the response, verifying the
server with `config`. The request target and host come from `url`, as in
`HttpRequest.send_url`.

### `send_url`

```quazi
pub fn send_url(request: HttpRequest, url: Url) Result[HttpResponse, TlsError]
```

Sends `request` to an `https` `url`, trusting the system certificate store.

## `TlsError`

```quazi
pub enum TlsError {
    // The underlying TCP connection failed.
    Net(NetError),
    // TLS is not implemented for this target.
    Unsupported,
    // The host name or CA path contains a NUL byte at this position.
    InvalidName(usize),
    AllocationFailed,
    // The TLS library could not create its context or session.
    LibraryFailure,
    // The configured trust store could not be loaded.
    TrustStoreUnavailable,
    // The peer certificate chain is not trusted (verification code).
    UntrustedCertificate(i64),
    // The certificate does not name the requested host.
    HostnameMismatch,
    // The TLS handshake failed for another reason (SSL_get_error code).
    HandshakeFailed(i32),
    // A record could not be read or written (SSL_get_error code), including a
    // connection closed without a TLS close_notify alert.
    ProtocolError(i32),
    // The stream was already closed.
    Closed,
    LimitExceeded,
    InvalidUtf8,
    // The configuration is unusable (an empty CA file path).
    InvalidConfig,
}
```

Why a TLS operation failed.

### `TlsError.message`

```quazi
pub fn message(self: TlsError) str
```

A short English description of the error, for display.

## `TlsConfig`

```quazi
pub struct TlsConfig { /* internal fields */ }
```

Which certificates a client trusts.

### `TlsConfig.system`

```quazi
pub fn system() TlsConfig
```

Trust the operating system's certificate store.

### `TlsConfig.with_ca_file`

```quazi
pub fn with_ca_file(path: str) Result[TlsConfig, TlsError]
```

Trust only the PEM certificates in `path` instead of the system store
(for private certificate authorities). An empty path is InvalidConfig;
use `system()` for the system store.

### `TlsConfig.ca_file`

```quazi
pub fn ca_file(self: &TlsConfig) str
```

The CA file, or "" for the system store.

## `TlsStream`

```quazi
pub struct TlsStream { /* internal fields */ }
```

A verified TLS client connection. Closed (with a close_notify alert) at the
end of scope.

### `TlsStream.connect`

```quazi
pub fn connect(host: str, port: i32) Result[TlsStream, TlsError]
```

Connects to `host:port` and verifies the server against the system
trust store and `host`.

### `TlsStream.connect_with`

```quazi
pub fn connect_with(host: str, port: i32, config: &TlsConfig) Result[TlsStream, TlsError]
```

Connects to `host:port`, verifying the server with `config`.

### `TlsStream.send`

```quazi
pub fn send(self: &TlsStream!, text: str) Result[usize, TlsError]
```

Sends `text`; returns the number of bytes sent.

### `TlsStream.send_bytes`

```quazi
pub fn send_bytes(self: &TlsStream!, data: bytes) Result[usize, TlsError]
```

Sends `data`; returns the number of bytes sent.

### `TlsStream.receive`

```quazi
pub fn receive(self: &TlsStream!, limit: usize) Result[String, TlsError]
```

Receives what is available, at most `limit` bytes, as UTF-8 text.
Returns "" after the peer closed the stream.

### `TlsStream.receive_all`

```quazi
pub fn receive_all(self: &TlsStream!, limit: usize) Result[String, TlsError]
```

Receives until the peer closes the stream with close_notify, at most
`limit` bytes. A connection cut without close_notify is an error, so a
truncated response is never mistaken for a complete one.

### `TlsStream.close`

```quazi
pub fn close(self: &TlsStream!) void
```

Sends close_notify and closes the connection now.

### `TlsStream.free`

```quazi
pub fn free(self: TlsStream) void
```

Closes the stream; called automatically at the end of scope.

### `TlsStream.handle`

```quazi
pub fn handle(self: &TlsStream) isize
```

The native socket handle of the underlying TCP connection.
