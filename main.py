#!/usr/bin/env python3
"""Entrypoint for the news-image-20261127 entry (Python 3.13, stdlib only).

Copies the front-page image shipped beside this file to the output
directory as entry.png, after checking it is a whole PNG of at most
1 MiB and at most 1024 by 1024 pixels. Run:
    python3 main.py            # writes /output/entry.png
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024


def check_png(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    length, ctype = struct.unpack(">I4s", head[8:16])
    if ctype != b"IHDR" or length != 13:
        raise SystemExit("entry.png has no IHDR chunk first")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(
            "entry.png is %d by %d pixels, larger than 1024 by 1024"
            % (width, height)
        )
    if os.path.getsize(path) > MAX_BYTES:
        raise SystemExit("entry.png is larger than 1 MiB")
    with open(path, "rb") as fh:
        fh.seek(-12, os.SEEK_END)
        tail = fh.read(12)
    if len(tail) < 12 or tail[4:8] != b"IEND":
        raise SystemExit("entry.png has no IEND chunk at its end")


def main():
    check_png(SRC)
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    size = os.path.getsize(DST)
    if size != os.path.getsize(SRC):
        raise SystemExit("entry.png did not copy whole")
    print("wrote", DST, size, "bytes")


if __name__ == "__main__":
    main()
