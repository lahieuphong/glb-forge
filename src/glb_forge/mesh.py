from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

Vec3 = tuple[float, float, float]
ColorRGBA = tuple[float, float, float, float]


@dataclass(frozen=True)
class MeshData:
    """Dữ liệu mesh tối thiểu để ghi ra file GLB.

    positions: danh sách điểm 3D, mỗi điểm là (x, y, z)
    normals: danh sách normal ứng với từng position
    indices: danh sách index tạo tam giác, cứ 3 số là 1 tam giác
    color: màu vật liệu dạng RGBA, giá trị từ 0.0 đến 1.0
    """

    name: str
    positions: Sequence[Vec3]
    normals: Sequence[Vec3]
    indices: Sequence[int]
    color: ColorRGBA = (0.1, 0.35, 1.0, 1.0)

    def validate(self) -> None:
        if not self.positions:
            raise ValueError("Mesh phải có ít nhất 1 position.")

        if len(self.positions) != len(self.normals):
            raise ValueError("Số lượng positions và normals phải bằng nhau.")

        if len(self.indices) % 3 != 0:
            raise ValueError("Số lượng indices phải chia hết cho 3 vì mỗi tam giác có 3 index.")

        max_index = len(self.positions) - 1
        for index in self.indices:
            if index < 0 or index > max_index:
                raise ValueError(f"Index {index} nằm ngoài range 0..{max_index}.")

        if len(self.color) != 4:
            raise ValueError("color phải là tuple RGBA có 4 giá trị.")
