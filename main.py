#!/usr/bin/env python3
"""Entry for make.fun's 'Make the cutest picture' competition.

Repository layout (repo: ~/workspace/ai-worker/makefun-art/mf-cute-pic):
  entry.png  - the picture (baby panda hugging a glowing star, pastel meadow)
  main.py    - this program: copies entry.png to /output/entry.png

RULES.txt for this competition states the simplest entry is "a repository
holding the image and a one-line program that copies it there".
Standard library only, no network, no randomness.
"""

import hashlib
import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    data = source.read_bytes()

    # The gate only accepts a whole PNG: check the magic bytes before
    # writing, so a corrupted entry.png fails loudly instead of
    # producing an invalid submission.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print(f"error: {source} is not a PNG file", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)

    # Self-check: the written file must be byte-identical to the source.
    written = target.read_bytes()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        print(f"error: {target} does not match {source}", file=sys.stderr)
        return 1

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
