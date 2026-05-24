from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glb_forge import create_trang_an_house, write_scene_glb


def main() -> None:
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    scene = create_trang_an_house(seed=42)
    path = write_scene_glb(scene, output_dir / "trang_an_heritage_house.glb")

    print(f"Generated file: {path}")
    print(f"Scene 04 vertices: {len(scene.positions):,}")
    print(f"Scene 04 materials: {len(scene.materials):,}")


if __name__ == "__main__":
    main()
