from __future__ import annotations

from glb_forge.scenes import create_trang_an_house
from glb_forge.sites.models import HeritageSite, Province


NINH_BINH = Province(
    code="35",
    slug="ninh-binh",
    name="Ninh Bình",
    output_name="Ninh-Binh",
)


TRANG_AN_HERITAGE_HOUSE = HeritageSite(
    site_id="nha-co-trang-an",
    name="Nhà cổ Tràng An",
    province=NINH_BINH,
    output_name="Nha-co-Trang-An",
    create_scene=lambda: create_trang_an_house(seed=42),
)


NINH_BINH_SITES = [
    TRANG_AN_HERITAGE_HOUSE,
]


__all__ = [
    "NINH_BINH",
    "NINH_BINH_SITES",
    "TRANG_AN_HERITAGE_HOUSE",
]
