from __future__ import annotations

from glb_forge.mesh import ColorRGBA, MeshData


def create_cube(
    size: float = 2.0,
    color: ColorRGBA = (0.1, 0.35, 1.0, 1.0),
) -> MeshData:
    """Tạo cube flat-shaded.

    Mỗi mặt có 4 vertex riêng để normal của mặt đó rõ ràng.
    """
    half = size / 2

    faces = [
        ((0, 0, 1), [(-half, -half, half), (half, -half, half), (half, half, half), (-half, half, half)]),
        ((0, 0, -1), [(half, -half, -half), (-half, -half, -half), (-half, half, -half), (half, half, -half)]),
        ((1, 0, 0), [(half, -half, half), (half, -half, -half), (half, half, -half), (half, half, half)]),
        ((-1, 0, 0), [(-half, -half, -half), (-half, -half, half), (-half, half, half), (-half, half, -half)]),
        ((0, 1, 0), [(-half, half, half), (half, half, half), (half, half, -half), (-half, half, -half)]),
        ((0, -1, 0), [(-half, -half, -half), (half, -half, -half), (half, -half, half), (-half, -half, half)]),
    ]

    positions = []
    normals = []
    indices = []

    for normal, corners in faces:
        base_index = len(positions)
        positions.extend(corners)
        normals.extend([normal] * 4)
        indices.extend(
            [
                base_index,
                base_index + 1,
                base_index + 2,
                base_index,
                base_index + 2,
                base_index + 3,
            ]
        )

    return MeshData(
        name="Cube",
        positions=positions,
        normals=normals,
        indices=indices,
        color=color,
    )
