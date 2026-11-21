#!/usr/bin/env python3
"""news-image-20261121 entry point (Python 3.13, standard library only).

Copies the pre-rendered front page (news.png, next to this script) to
<MAKEFUN_OUTPUT_DIR>/entry.png (default /output). Fully deterministic:
no network, no clock, no randomness. The output is a byte-for-byte copy
of the bundled image, so repeated runs produce identical bytes.
"""
import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "news.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    with open(source, "rb") as f:
        data = f.read()

    if not data.startswith(PNG_SIGNATURE):
        print("error: source image is not a valid PNG", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)

    print(f"wrote {dest} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
