#!/usr/bin/env python3
"""Check the 26 November 2026 news-image entry and hand it to the grader.

The picture itself, ``entry.png``, is already finished and lives beside
this script. Nothing here draws, crops, or re-encodes it. All this
program does is confirm the picture obeys the bounty limits and then
drop a byte-for-byte copy into the output folder the grader reads from.

Limits checked before any copying happens:

* the file begins with the eight-byte PNG signature;
* the width and height recorded in its IHDR chunk are each greater
  than zero and at most 1024 pixels;
* the file is no larger than 1 MiB (1,048,576 bytes).

After copying, the digest of the copy is compared with the digest of
the original, so a short or corrupted write is caught instead of
being handed on quietly.

Usage::

    python3 main.py [--output-dir DIR] [--verify-only]

The output folder defaults to ``out``; setting ``MAKEFUN_OUTPUT_DIR``
overrides that default, and ``--output-dir`` overrides both. With
``--verify-only`` the picture is checked and a short summary printed,
but nothing is copied. An output folder that does not exist yet is
created, including any missing parent folders.
"""

import argparse
import hashlib
import os
import struct
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_SIDE = 1024
MAX_BYTES = 1_048_576
SOURCE_NAME = "entry.png"


class EntryProblem(Exception):
    """Raised when the picture or the destination fails a check."""


def digest_file(path):
    """Return the SHA-256 hex digest of the file at *path*."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def inspect_png(path):
    """Validate *path* as a PNG inside the bounty limits.

    Returns a dict holding the picture's width, height, byte size and
    SHA-256 digest. Raises EntryProblem with a plain-language reason
    whenever anything is off.
    """
    if not path.is_file():
        raise EntryProblem(f"no entry picture found at {path}")
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise EntryProblem(
            f"{path} is {size} bytes, over the 1 MiB limit of {MAX_BYTES} bytes"
        )
    with path.open("rb") as handle:
        head = handle.read(24)
    if len(head) < 24 or head[:8] != PNG_SIGNATURE:
        raise EntryProblem(f"{path} does not start with a PNG signature")
    chunk_length, chunk_tag = struct.unpack(">I4s", head[8:16])
    if chunk_tag != b"IHDR" or chunk_length != 13:
        raise EntryProblem(
            f"{path} has no proper IHDR chunk up front"
            f" (found tag {chunk_tag!r}, length {chunk_length})"
        )
    width, height = struct.unpack(">II", head[16:24])
    if width == 0 or height == 0:
        raise EntryProblem(f"{path} reports a zero width or height")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise EntryProblem(
            f"{path} is {width}x{height}, larger than the "
            f"{MAX_SIDE}x{MAX_SIDE} limit"
        )
    return {
        "width": width,
        "height": height,
        "size": size,
        "sha256": digest_file(path),
    }


def hand_over(source, info, output_dir):
    """Copy *source* into *output_dir* and prove the copy is identical.

    Returns the path of the copy. Raises EntryProblem if the output
    folder cannot be created or the copy's digest differs from the
    original.
    """
    # Make the destination folder when it is missing, so the grader
    # does not have to create it by hand first.
    output_dir.mkdir(parents=True, exist_ok=True)
    if not output_dir.is_dir():
        raise EntryProblem(f"could not create output folder {output_dir}")
    destination = output_dir / SOURCE_NAME
    with source.open("rb") as src, destination.open("wb") as dst:
        while True:
            block = src.read(65536)
            if not block:
                break
            dst.write(block)
    copied_digest = digest_file(destination)
    if copied_digest != info["sha256"]:
        raise EntryProblem(
            f"copy at {destination} has digest {copied_digest},"
            f" expected {info['sha256']}"
        )
    return destination


def build_parser():
    """Build the command-line parser for this program."""
    parser = argparse.ArgumentParser(
        description="Validate entry.png and copy it to the grader output folder."
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="folder to copy entry.png into "
        "(default: $MAKEFUN_OUTPUT_DIR or 'out')",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="only check entry.png; do not copy anything",
    )
    return parser


def main(argv=None):
    """Run the check-and-copy flow; return 0 on success, 1 on failure."""
    args = build_parser().parse_args(argv)
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    try:
        info = inspect_png(source)
    except EntryProblem as problem:
        print(f"entry rejected: {problem}", file=sys.stderr)
        return 1
    print(
        f"entry.png OK: {info['width']}x{info['height']},"
        f" {info['size']} bytes, sha256 {info['sha256']}"
    )
    if args.verify_only:
        return 0
    output_dir = Path(
        args.output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    )
    try:
        destination = hand_over(source, info, output_dir)
    except EntryProblem as problem:
        print(f"could not hand over entry: {problem}", file=sys.stderr)
        return 1
    print(f"copied to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
