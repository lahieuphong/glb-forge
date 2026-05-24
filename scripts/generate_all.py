from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glb_forge import MeshData, create_cube, create_pyramid, create_trang_an_house, write_glb, write_scene_glb


def main() -> None:
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    files = []

    files.append(write_glb(create_cube(size=2.0, color=(0.1, 0.35, 1.0, 1.0)), output_dir / "cube.glb"))
    files.append(write_glb(create_pyramid(size=2.0, height=2.4, color=(1.0, 0.6, 0.15, 1.0)), output_dir / "pyramid.glb"))

    triangle = MeshData(
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
    files.append(write_glb(triangle, output_dir / "custom_triangle.glb"))

    scene = create_trang_an_house(seed=42)
    files.append(write_scene_glb(scene, output_dir / "trang_an_heritage_house.glb"))

    print("Generated files:")
    for path in files:
        print(f"- {path}")
    print(f"Scene 04 vertices: {len(scene.positions):,}")
    print(f"Scene 04 materials: {len(scene.materials):,}")


if __name__ == "__main__":
    main()
