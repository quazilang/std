#!/usr/bin/env python3
"""Check that docs/reference matches `qz doc` for src/ and report public
declarations without a doc comment. Modules in COMPLETE must have none.

Regenerate with:  qz doc -o docs/reference
"""

import argparse
import filecmp
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPLETE = {"fs.md", "path.md", "process.md", "io.md", "time.md", "random.md", "os.md",
            "json.md", "codec.md", "ini.md", "math.md", "thread.md", "core.md", "dylib.md",
            "ffi.md", "net.md", "collections/map.md", "collections/set.md"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qz", type=Path, help="matching compiler executable")
    qz = parser.parse_args().qz.resolve()
    committed = ROOT / "docs/reference"
    with tempfile.TemporaryDirectory(prefix="quazi-std-reference-") as directory:
        generated = Path(directory)
        subprocess.run([str(qz), "doc", "-o", str(generated)], cwd=ROOT, check=True,
                       capture_output=True)
        stale = [str(page.relative_to(generated)) for page in sorted(generated.rglob("*.md"))
                 if not (committed / page.relative_to(generated)).exists()
                 or not filecmp.cmp(page, committed / page.relative_to(generated), shallow=False)]
        stale += [str(page.relative_to(committed)) for page in committed.rglob("*.md")
                  if not (generated / page.relative_to(committed)).exists()]
        gaps = {str(page.relative_to(generated)): page.read_text().count("_Undocumented._")
                for page in sorted(generated.rglob("*.md"))}
    if stale:
        sys.exit(f"docs/reference is out of date: {stale}; run `qz doc -o docs/reference`")
    incomplete = [name for name in COMPLETE if gaps.get(name)]
    if incomplete:
        sys.exit(f"undocumented public declarations in {incomplete}")
    pending = {name: count for name, count in gaps.items() if count}
    print(f"PASS reference: docs/reference is current; {len(COMPLETE)} modules fully documented, "
          f"undocumented elsewhere: {sum(pending.values())} in {len(pending)} modules")


if __name__ == "__main__":
    main()
