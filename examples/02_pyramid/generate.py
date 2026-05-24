from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glb_forge import write_glb
from glb_forge.shapes import create_pyramid


OUTPUT_PATH = PROJECT_ROOT / "output" / "pyramid.glb"


if __name__ == "__main__":
    mesh = create_pyramid(size=2.0, height=2.4, color=(1.0, 0.6, 0.15, 1.0))
    path = write_glb(mesh, OUTPUT_PATH)
    print(f"Đã tạo: {path}")
