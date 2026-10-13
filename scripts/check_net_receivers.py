#!/usr/bin/env python3
"""Check production receiver declarations in isolation from unfinished codecs.

The fixture keeps real owner fields, constructors and transport implementation.
It excludes Headers operations and HTTP codecs. Passing this check does not
establish that the full std.net module builds.
"""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile


def declarations(source, name, methods):
    # This bounded extractor follows net.qz's column-zero declaration endings.
    struct = re.search(
        rf"^pub struct {name} \{{[^\n]*\}}|^pub struct {name} \{{.*?^\}}",
        source, re.M | re.S,
    )
    impl = re.search(rf"^impl {name} \{{\n(.*?)^\}}", source, re.M | re.S)
    if not struct or not impl:
        raise ValueError(f"missing production declaration: {name}")
    body = impl.group(1)
    starts = list(re.finditer(r"^    pub fn (\w+)\(", body, re.M))
    selected = []
    for method in methods:
        hits = [i for i, match in enumerate(starts) if match.group(1) == method]
        if len(hits) != 1:
            raise ValueError(f"expected one production method: {name}.{method}")
        index = hits[0]
        end = starts[index + 1].start() if index + 1 < len(starts) else len(body)
        selected.append(body[starts[index].start():end])
    return struct.group(0) + "\n\nimpl " + name + " {\n" + "".join(selected) + "}\n"


def invoke(qz, work, arguments):
    return subprocess.run(
        [str(qz), *arguments, "--no-color", "--no-unicode"],
        cwd=work, text=True, capture_output=True, timeout=120,
    )


def require_success(qz, work, arguments):
    result = invoke(qz, work, arguments)
    if result.returncode != 0:
        raise AssertionError(f"{arguments}: failed\n{result.stdout}\n{result.stderr}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qz", type=Path, help="matching compiler executable")
    parser.add_argument(
        "--source", type=Path,
        help="alternate net.qz for before/after regression checks",
    )
    args = parser.parse_args()
    qz = args.qz.resolve()
    root = Path(__file__).resolve().parents[1]
    source = (args.source or root / "src/net.qz").read_text()
    transport, marker, _ = source.partition("pub struct Header {")
    if not marker:
        raise ValueError("missing transport/HTTP boundary")
    selected = [
        ("Header", ["new", "name", "value"]),
        ("Headers", ["new"]),
        ("HttpRequest", ["new", "method", "target", "host", "body_text"]),
        ("HttpResponse", ["new", "status", "reason", "body"]),
        ("HttpConnection", ["read_request", "close"]),
        ("HttpServer", ["bind", "accept", "close", "free"]),
    ]
    fixture = transport + "\n".join(
        declarations(source, name, methods) for name, methods in selected
    )
    tests = re.sub(
        r"^import std\.(?:net\..*|core);\n", "",
        (root / "tests/net_receivers.qz").read_text(), flags=re.M,
    )
    with tempfile.TemporaryDirectory(prefix="quazi-net-receivers-") as directory:
        work = Path(directory)
        (work / "src").mkdir()
        (work / "quazi.toml").write_text(
            '[package]\nname = "net_receivers"\nversion = "0.1.0"\n'
            '[lib]\npath = "src/net.qz"\n'
        )
        (work / "src/net.qz").write_text(fixture + "\n" + tests)
        output = require_success(qz, work, ["test"])
        print("\n".join(line for line in output.splitlines() if line.startswith(
            ("running ", "test ")
        )), flush=True)
        cases = {
            "request_view_move": ("cannot move `owner` while it is shared-borrowed", '''
                fn take(value: HttpRequest) void {}
                fn main() i32 {
                    var owner = HttpRequest.new("GET", "/", "host");
                    const view: str = owner.method();
                    take(owner);
                    ret view.len() as i32;
                }
            '''),
            "response_view_write": ("cannot mutate `owner` while it is shared-borrowed", '''
                fn main() i32 {
                    var owner = HttpResponse.new(200, "OK", "body");
                    const view: str = owner.body();
                    owner.body = String.from("changed");
                    ret view.len() as i32;
                }
            '''),
            "temporary_datagram_view": ("cannot store a string view borrowed from a temporary owner", '''
                fn main() i32 {
                    const view: str = UdpDatagram {
                        data: String.from("payload"),
                        address: SocketAddress {
                            host: String.from("127.0.0.1"), port: 80,
                        },
                    }.text();
                    ret view.len() as i32;
                }
            '''),
        }
        for name, (expected, body) in cases.items():
            probe = work / "src" / (name + ".qz")
            probe.write_text(fixture + "\n" + body)
            result = invoke(qz, work, [
                "build", str(probe), "-i", "--no-incremental",
                "-o", str(work / (name + ".qzi")),
            ])
            diagnostic = result.stdout + result.stderr
            if (
                result.returncode == 0
                or "error[S10]" not in diagnostic
                or expected not in diagnostic
            ):
                raise AssertionError(f"{name}: expected {expected}\n{diagnostic}")
            print(f"negative lifetime probe {name}: rejected with S10", flush=True)
        # Artifact execution runs the seven new tests; qz test also runs the
        # three existing transport regressions copied with the implementation.
        calls = re.findall(r"^fn (\w+)\(\) void", tests, re.M)
        entry_calls = []
        for name in calls:
            call = name + "();"
            if name.startswith("linux_"):
                call = '@cfg(target_os = "linux") { ' + call + " }"
            entry_calls.append(call)
        native = work / "src/roundtrip.qz"
        native.write_text(
            fixture + "\n" + tests + "\nfn main() i32 { "
            + " ".join(entry_calls) + " ret 0; }\n"
        )
        artifact = work / "receivers.qzi"
        commands = [
            ["build", str(native), "-i", "--no-incremental", "-o", str(artifact)],
            ["build", str(artifact), "-o", str(work / "receivers"), "-r"],
            ["build", str(native), "-c", "--target", "x86_64-windows",
             "--no-incremental", "-o", str(work / "receivers.obj")],
        ]
        for command in commands:
            require_success(qz, work, command)
        print("QZI native round trip and Windows COFF emission: passed", flush=True)


if __name__ == "__main__":
    main()
