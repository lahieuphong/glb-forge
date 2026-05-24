from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glb_forge import HERITAGE_SITES, write_scene_glb


def main() -> None:
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    for site in HERITAGE_SITES:
        scene = site.create_scene()
        path = write_scene_glb(scene, site.output_path(output_dir))

        print(f"Generated file: {path}")
        print(f"{site.name} vertices: {len(scene.positions):,}")
        print(f"{site.name} materials: {len(scene.materials):,}")


if __name__ == "__main__":
    main()
