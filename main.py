#!/usr/bin/env python3
"""Entry point for news-image-20261123.

Copies the entry image (entry.png, in this repository) to /output/entry.png.
Standard library only, no network; the output is byte-identical on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT_DIR, "entry.png")
shutil.copyfile(src, dst)
# Fail loudly rather than submit a truncated copy.
assert os.path.getsize(dst) == os.path.getsize(src), "entry.png copy mismatch"
