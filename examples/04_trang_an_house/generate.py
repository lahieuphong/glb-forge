from __future__ import annotations

import sys
from pathlib import Path

# Cho phép chạy file này trực tiếp mà không cần cài package.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glb_forge import create_trang_an_house, write_scene_glb


OUTPUT_PATH = PROJECT_ROOT / "output" / "trang_an_heritage_house.glb"


def main() -> None:
    scene = create_trang_an_house(seed=42)
    path = write_scene_glb(scene, OUTPUT_PATH)

    print(f"Đã tạo: {path}")
    print(f"Vertices: {len(scene.positions):,}")
    print(f"Materials: {len(scene.materials):,}")


if __name__ == "__main__":
    main()
