#!/usr/bin/env python3
"""End-to-end check of std.tls against a local TLS server (D-008 matrix).

Builds a small HTTPS client with the given compiler, then runs it against a
Python `ssl` server whose certificate is issued by a throwaway CA:

- trusted CA file and matching host name: the response arrives;
- system trust store: the private CA is untrusted;
- address that the certificate does not name: host-name mismatch;
- connection cut without close_notify: reported, never a short response;
- peer closed while the client keeps writing: an error, not a SIGPIPE death.

Usage (from the workspace root):

    python3 std/scripts/check_tls.py --qz quazistrap/target/release/qz \
        [--openssl /path/to/openssl] [--ssl-lib /dir/with/libssl.so]

Linux only. The client links the system `libssl`/`libcrypto`.
"""

import argparse
import os
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

STD_ROOT = Path(__file__).resolve().parent.parent

CLIENT = """\
import std.io;
import std.net.{HttpMethod, HttpRequest, Url};
import std.tls;
import std.tls.{TlsConfig, TlsError, TlsStream};

// Writes until the peer's reset fails a write (SIGPIPE must not kill us).
fn flood(port: i32, config: &TlsConfig) i32 {
    const connected = TlsStream.connect_with("localhost", port, config);
    if (connected.is_err()) {
        const error: TlsError = connected.unwrap_err();
        io.println("connect error: {}", error.message());
        ret 1;
    }
    var stream: TlsStream = connected.unwrap();
    var block: String = String.new();
    for i : 0..4096 { block.push_str("0123456789abcdef"); }
    for round : 0..4096 {
        const sent = stream.send(block.as_str());
        if (sent.is_err()) {
            const error: TlsError = sent.unwrap_err();
            io.println("error: {}", error.message());
            ret 1;
        }
    }
    io.println("no error");
    ret 0;
}

// Usage: client <url> [ca-file [flood-port]]
fn main(args: Array[str]) i32 {
    if (args.len() < 2) { ret 2; }
    const target: str = args[1];
    var config: TlsConfig = TlsConfig.system();
    if (args.len() > 2) {
        const ca_file: str = args[2];
        config = TlsConfig.with_ca_file(ca_file).unwrap();
    }
    if (args.len() > 3) {
        const port_text: str = args[3];
        ret flood(port_text.parse_i32().unwrap(), &config);
    }
    const url = Url.parse(target);
    if (url.is_err()) { ret 2; }
    const request = HttpRequest.from_url(HttpMethod.Get, Url.parse(target).unwrap());
    const response = tls.send_url_with(request, url.unwrap(), &config);
    if (response.is_err()) {
        const error: TlsError = response.unwrap_err();
        io.println("error: {}", error.message());
        ret 1;
    }
    const ok = response.unwrap();
    io.println("status {} body {}", ok.status(), ok.body());
    ret 0;
}
"""

BODY = "hello over tls ✓"


def find_openssl(explicit):
    if explicit:
        return explicit
    found = shutil.which("openssl")
    if found:
        return found
    for candidate in sorted(Path("/nix/store").glob("*-openssl-3*-bin/bin/openssl")):
        return str(candidate)
    sys.exit("FAIL tls: no openssl executable (pass --openssl)")


def is_x86_64_elf(path):
    with open(path, "rb") as handle:
        header = handle.read(20)
    return header[:4] == b"\x7fELF" and header[4] == 2 and header[18] == 0x3E


def find_ssl_lib(explicit):
    if explicit:
        return explicit
    for directory in ["/usr/lib/x86_64-linux-gnu", "/usr/lib64", "/usr/lib", "/lib64"]:
        if Path(directory, "libssl.so").exists():
            return directory
    for candidate in sorted(Path("/nix/store").glob("*-openssl-3*/lib/libssl.so")):
        if is_x86_64_elf(candidate.resolve()):
            return str(candidate.parent)
    sys.exit("FAIL tls: no x86-64 libssl.so (pass --ssl-lib)")


def make_certificates(openssl, directory):
    def run(*args):
        subprocess.run([openssl, *args], cwd=directory, check=True, capture_output=True)

    run("req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "2",
        "-subj", "/CN=Quazi Test CA", "-keyout", "ca.key", "-out", "ca.pem")
    run("req", "-newkey", "rsa:2048", "-nodes", "-subj", "/CN=localhost",
        "-keyout", "server.key", "-out", "server.csr")
    Path(directory, "san.ext").write_text("subjectAltName=DNS:localhost\n")
    run("x509", "-req", "-in", "server.csr", "-CA", "ca.pem", "-CAkey", "ca.key",
        "-CAcreateserial", "-days", "2", "-extfile", "san.ext", "-out", "server.pem")


def serve(directory, close_notify, reset=False):
    """Start a one-thread HTTPS server; returns (port, stop)."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(Path(directory, "server.pem"), Path(directory, "server.key"))
    listener = socket.create_server(("127.0.0.1", 0))
    listener.settimeout(0.2)
    port = listener.getsockname()[1]
    stopping = threading.Event()
    body = BODY.encode()
    response = (b"HTTP/1.1 200 OK\r\nContent-Length: " + str(len(body)).encode()
                + b"\r\nConnection: close\r\n\r\n" + body)

    def loop():
        while not stopping.is_set():
            try:
                raw, _ = listener.accept()
            except socket.timeout:
                continue
            raw.settimeout(5)
            try:
                connection = context.wrap_socket(raw, server_side=True)
            except (ssl.SSLError, OSError):
                raw.close()
                continue
            if reset:
                # Close (FIN) right after the handshake: the client's next
                # writes draw an RST, and writing after it raises EPIPE.
                connection.close()
                continue
            try:
                data = b""
                while b"\r\n\r\n" not in data:
                    chunk = connection.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                if close_notify:
                    connection.sendall(response)
                    connection.unwrap().close()
                else:
                    connection.sendall(response[: len(response) // 2])
                    # Drop the TCP connection without a TLS close_notify.
                    connection.shutdown(socket.SHUT_RDWR)
                    connection.close()
            except (ssl.SSLError, OSError):
                connection.close()
        listener.close()

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

    def stop():
        stopping.set()
        thread.join()

    return port, stop


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qz", type=Path, default=Path("quazistrap/target/debug/qz"))
    parser.add_argument("--openssl")
    parser.add_argument("--ssl-lib")
    args = parser.parse_args()
    qz = args.qz.resolve()
    openssl = find_openssl(args.openssl)
    ssl_lib = find_ssl_lib(args.ssl_lib)

    with tempfile.TemporaryDirectory(prefix="quazi-tls-") as temp:
        root = Path(temp)
        make_certificates(openssl, root)
        project = root / "client"
        (project / "src").mkdir(parents=True)
        (project / "src" / "main.qz").write_text(CLIENT)
        (project / "quazi.toml").write_text(
            '[package]\nname = "tls-client"\nversion = "0.1.0"\nout_dir = "build"\n\n'
            '[[bin]]\nname = "tls-client"\npath = "src/main.qz"\n\n'
            '[target.x86_64-linux.link]\nlibc = true\nlibraries = ["ssl", "crypto"]\n'
            f'library-paths = ["{ssl_lib}"]\n'
        )
        environment = dict(os.environ, QUAZI_STD_ROOT=str(STD_ROOT))
        built = subprocess.run([qz, "build"], cwd=project, env=environment,
                               capture_output=True, text=True)
        if built.returncode != 0:
            sys.exit(f"FAIL tls: client build failed\n{built.stdout}\n{built.stderr}")
        client = project / "build" / "tls-client"
        run_environment = dict(os.environ, LD_LIBRARY_PATH=ssl_lib)
        # The system store must not happen to trust the throwaway CA.
        run_environment.pop("SSL_CERT_FILE", None)
        run_environment.pop("SSL_CERT_DIR", None)
        ca = str(root / "ca.pem")

        def run(url, *extra):
            result = subprocess.run([client, url, *extra], env=run_environment,
                                    capture_output=True, text=True, timeout=30)
            return result.returncode, result.stdout.strip()

        failures = []

        def expect(name, outcome, code, text):
            if outcome != (code, text):
                failures.append(f"{name}: expected {(code, text)!r}, got {outcome!r}")

        port, stop = serve(root, close_notify=True)
        try:
            expect("trusted CA", run(f"https://localhost:{port}/", ca),
                   0, f"status 200 body {BODY}")
            expect("system store", run(f"https://localhost:{port}/"),
                   1, "error: the server certificate is not trusted")
            expect("wrong host", run(f"https://127.0.0.1:{port}/", ca),
                   1, "error: the server certificate does not match the host name")
            expect("missing CA file", run(f"https://localhost:{port}/", str(root / "absent.pem")),
                   1, "error: the TLS trust store could not be loaded")
        finally:
            stop()
        port, stop = serve(root, close_notify=False)
        try:
            expect("truncated", run(f"https://localhost:{port}/", ca),
                   1, "error: TLS record error or truncated connection")
        finally:
            stop()
        port, stop = serve(root, close_notify=True, reset=True)
        try:
            # Exit status -13 would mean SIGPIPE killed the client.
            expect("peer closed while writing", run(f"https://localhost:{port}/", ca, str(port)),
                   1, "error: TLS record error or truncated connection")
        finally:
            stop()
        closed = socket.create_server(("127.0.0.1", 0))
        refused_port = closed.getsockname()[1]
        closed.close()
        expect("refused", run(f"https://localhost:{refused_port}/", ca),
               1, "error: connection refused")

        if failures:
            sys.exit("FAIL tls:\n  " + "\n  ".join(failures))
    print("PASS tls: trusted CA, untrusted system store, host-name mismatch, "
          "missing trust store, truncation, peer closed while writing and refused connection")


if __name__ == "__main__":
    main()
