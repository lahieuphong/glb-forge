from __future__ import annotations

import sys
from pathlib import Path

# Cho phép chạy trực tiếp: python examples/01_cube/generate.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glb_forge import write_glb
from glb_forge.shapes import create_cube


OUTPUT_PATH = PROJECT_ROOT / "output" / "cube.glb"


if __name__ == "__main__":
    mesh = create_cube(size=2.0, color=(0.1, 0.35, 1.0, 1.0))
    path = write_glb(mesh, OUTPUT_PATH)
    print(f"Đã tạo: {path}")
