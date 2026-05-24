from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glb_forge import MeshData, write_glb


OUTPUT_PATH = PROJECT_ROOT / "output" / "custom_triangle.glb"


if __name__ == "__main__":
    # Ví dụ mesh tự viết: 1 tam giác đơn giản nằm trên mặt phẳng XZ.
    mesh = MeshData(
        name="Custom Triangle",
        positions=[
            (-1.0, 0.0, -1.0),
            (1.0, 0.0, -1.0),
            (0.0, 0.0, 1.0),
        ],
        normals=[
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
        ],
        indices=[0, 1, 2],
        color=(0.2, 0.9, 0.4, 1.0),
    )

    path = write_glb(mesh, OUTPUT_PATH)
    print(f"Đã tạo: {path}")
