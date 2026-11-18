#!/usr/bin/env python3
"""Place the 17 November 2026 world-news image in the grading output directory."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

SOURCE = os.path.join(HERE, "entry.png")
if not os.path.isfile(SOURCE):
    raise SystemExit("entry.png is missing from the repository")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SOURCE, os.path.join(OUT, "entry.png"))
