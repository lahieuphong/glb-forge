from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .scene import SceneMesh
from .scenes import create_trang_an_house


SceneFactory = Callable[[], SceneMesh]


@dataclass(frozen=True)
class HeritageSite:
    name: str
    province_dir: str
    file_name: str
    create_scene: SceneFactory

    def output_path(self, output_root: str | Path) -> Path:
        return Path(output_root) / self.province_dir / self.file_name


TRANG_AN_HERITAGE_HOUSE = HeritageSite(
    name="Nhà cổ Tràng An",
    province_dir="35-Ninh-Binh",
    file_name="Nha-co-Trang-An.glb",
    create_scene=lambda: create_trang_an_house(seed=42),
)


HERITAGE_SITES = [
    TRANG_AN_HERITAGE_HOUSE,
]


__all__ = [
    "HERITAGE_SITES",
    "TRANG_AN_HERITAGE_HOUSE",
    "HeritageSite",
]
