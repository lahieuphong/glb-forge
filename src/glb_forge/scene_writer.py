from __future__ import annotations

import json
import struct
from pathlib import Path

from .scene import SceneMesh, Vec3

GLB_MAGIC = 0x46546C67      # b"glTF"
GLB_VERSION = 2
CHUNK_JSON = 0x4E4F534A     # b"JSON"
CHUNK_BIN = 0x004E4942      # b"BIN\0"

FLOAT = 5126
UNSIGNED_SHORT = 5123
UNSIGNED_INT = 5125
ARRAY_BUFFER = 34962
ELEMENT_ARRAY_BUFFER = 34963
TRIANGLES = 4


def _pad4(data: bytes, pad_byte: bytes) -> bytes:
    padding = (4 - len(data) % 4) % 4
    return data + pad_byte * padding


def _append_aligned(blob: bytearray, data: bytes) -> int:
    while len(blob) % 4 != 0:
        blob.append(0)
    offset = len(blob)
    blob.extend(data)
    return offset


def _pack_vec3(values: list[Vec3]) -> bytes:
    return b"".join(struct.pack("<3f", *v) for v in values)


def _pack_indices(indices: list[int]) -> tuple[bytes, int]:
    if max(indices) <= 65535:
        return b"".join(struct.pack("<H", i) for i in indices), UNSIGNED_SHORT
    return b"".join(struct.pack("<I", i) for i in indices), UNSIGNED_INT


def _bounds(positions: list[Vec3]) -> tuple[list[float], list[float]]:
    return (
        [min(p[i] for p in positions) for i in range(3)],
        [max(p[i] for p in positions) for i in range(3)],
    )


def write_scene_glb(scene: SceneMesh, output_path: str | Path) -> Path:
    """Ghi SceneMesh nhiều material ra file GLB thuần Python."""
    scene.validate()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    positions = list(scene.positions)
    normals = list(scene.normals)

    position_bytes = _pack_vec3(positions)
    normal_bytes = _pack_vec3(normals)

    bin_blob = bytearray()
    offset_positions = _append_aligned(bin_blob, position_bytes)
    offset_normals = _append_aligned(bin_blob, normal_bytes)

    position_min, position_max = _bounds(positions)

    buffer_views: list[dict] = [
        {
            "buffer": 0,
            "byteOffset": offset_positions,
            "byteLength": len(position_bytes),
            "target": ARRAY_BUFFER,
        },
        {
            "buffer": 0,
            "byteOffset": offset_normals,
            "byteLength": len(normal_bytes),
            "target": ARRAY_BUFFER,
        },
    ]

    accessors: list[dict] = [
        {
            "bufferView": 0,
            "byteOffset": 0,
            "componentType": FLOAT,
            "count": len(positions),
            "type": "VEC3",
            "min": position_min,
            "max": position_max,
        },
        {
            "bufferView": 1,
            "byteOffset": 0,
            "componentType": FLOAT,
            "count": len(normals),
            "type": "VEC3",
        },
    ]

    primitives: list[dict] = []

    for material_index, indices in scene.indices_by_material.items():
        if not indices:
            continue

        index_bytes, index_component_type = _pack_indices(indices)
        offset_indices = _append_aligned(bin_blob, index_bytes)

        buffer_view_index = len(buffer_views)
        buffer_views.append(
            {
                "buffer": 0,
                "byteOffset": offset_indices,
                "byteLength": len(index_bytes),
                "target": ELEMENT_ARRAY_BUFFER,
            }
        )

        accessor_index = len(accessors)
        accessors.append(
            {
                "bufferView": buffer_view_index,
                "byteOffset": 0,
                "componentType": index_component_type,
                "count": len(indices),
                "type": "SCALAR",
            }
        )

        primitives.append(
            {
                "attributes": {
                    "POSITION": 0,
                    "NORMAL": 1,
                },
                "indices": accessor_index,
                "material": material_index,
                "mode": TRIANGLES,
            }
        )

    gltf_materials: list[dict] = []
    for material in scene.materials:
        gltf_materials.append(
            {
                "name": material.name,
                "doubleSided": material.double_sided,
                "pbrMetallicRoughness": {
                    "baseColorFactor": list(material.color),
                    "metallicFactor": material.metallic,
                    "roughnessFactor": material.roughness,
                },
            }
        )

    gltf_json = {
        "asset": {
            "version": "2.0",
            "generator": "glb-forge pure-python procedural scene writer",
        },
        "scene": 0,
        "scenes": [
            {
                "name": "Scene",
                "nodes": [0],
            }
        ],
        "nodes": [
            {
                "name": scene.name,
                "mesh": 0,
            }
        ],
        "meshes": [
            {
                "name": scene.name,
                "primitives": primitives,
            }
        ],
        "materials": gltf_materials,
        "buffers": [
            {
                "byteLength": len(bin_blob),
            }
        ],
        "bufferViews": buffer_views,
        "accessors": accessors,
    }

    json_bytes = json.dumps(gltf_json, separators=(",", ":")).encode("utf-8")
    json_chunk = _pad4(json_bytes, b" ")
    bin_chunk = _pad4(bytes(bin_blob), b"\x00")

    total_length = 12 + 8 + len(json_chunk) + 8 + len(bin_chunk)

    glb_data = b"".join(
        [
            struct.pack("<III", GLB_MAGIC, GLB_VERSION, total_length),
            struct.pack("<II", len(json_chunk), CHUNK_JSON),
            json_chunk,
            struct.pack("<II", len(bin_chunk), CHUNK_BIN),
            bin_chunk,
        ]
    )

    output_path.write_bytes(glb_data)
    return output_path
