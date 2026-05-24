from __future__ import annotations

import math

from glb_forge.mesh import ColorRGBA, MeshData, Vec3


def _subtract(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _normalize(v: Vec3) -> Vec3:
    length = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if length == 0:
        return (0.0, 1.0, 0.0)
    return (v[0] / length, v[1] / length, v[2] / length)


def _face_normal(points: list[Vec3]) -> Vec3:
    a = _subtract(points[1], points[0])
    b = _subtract(points[2], points[0])
    return _normalize(_cross(a, b))


def create_pyramid(
    size: float = 2.0,
    height: float = 2.4,
    color: ColorRGBA = (1.0, 0.6, 0.15, 1.0),
) -> MeshData:
    """Tạo pyramid đáy vuông."""
    half = size / 2

    bottom_a = (-half, 0.0, -half)
    bottom_b = (half, 0.0, -half)
    bottom_c = (half, 0.0, half)
    bottom_d = (-half, 0.0, half)
    top = (0.0, height, 0.0)

    # Thứ tự điểm được chọn để mặt hướng ra ngoài.
    faces = [
        [bottom_d, bottom_c, bottom_b, bottom_a],  # đáy
        [bottom_a, bottom_b, top],                 # mặt sau
        [bottom_b, bottom_c, top],                 # mặt phải
        [bottom_c, bottom_d, top],                 # mặt trước
        [bottom_d, bottom_a, top],                 # mặt trái
    ]

    positions = []
    normals = []
    indices = []

    for face_points in faces:
        base_index = len(positions)
        normal = _face_normal(face_points)

        positions.extend(face_points)
        normals.extend([normal] * len(face_points))

        # Triangulate dạng fan: 0-1-2, 0-2-3, ...
        for i in range(1, len(face_points) - 1):
            indices.extend([base_index, base_index + i, base_index + i + 1])

    return MeshData(
        name="Pyramid",
        positions=positions,
        normals=normals,
        indices=indices,
        color=color,
    )
