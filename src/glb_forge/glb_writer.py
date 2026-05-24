from __future__ import annotations

import json
import struct
from pathlib import Path

from .mesh import MeshData

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
    """Pad dữ liệu để độ dài chia hết cho 4 byte."""
    padding = (4 - len(data) % 4) % 4
    return data + pad_byte * padding


def _bounds(positions: list[tuple[float, float, float]]) -> tuple[list[float], list[float]]:
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    zs = [p[2] for p in positions]
    return [min(xs), min(ys), min(zs)], [max(xs), max(ys), max(zs)]


def write_glb(mesh: MeshData, output_path: str | Path) -> Path:
    """Ghi 1 mesh đơn giản ra file .glb.

    Hàm này hỗ trợ:
    - POSITION
    - NORMAL
    - indices
    - 1 material PBR đơn giản
    """
    mesh.validate()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    positions = list(mesh.positions)
    normals = list(mesh.normals)
    indices = list(mesh.indices)

    position_bytes = b"".join(struct.pack("<3f", *position) for position in positions)
    normal_bytes = b"".join(struct.pack("<3f", *normal) for normal in normals)

    if max(indices) <= 65535:
        index_component_type = UNSIGNED_SHORT
        index_bytes = b"".join(struct.pack("<H", index) for index in indices)
    else:
        index_component_type = UNSIGNED_INT
        index_bytes = b"".join(struct.pack("<I", index) for index in indices)

    offset_positions = 0
    offset_normals = offset_positions + len(position_bytes)
    offset_indices = offset_normals + len(normal_bytes)

    bin_blob = position_bytes + normal_bytes + index_bytes
    bin_chunk = _pad4(bin_blob, b"\x00")

    position_min, position_max = _bounds(positions)

    gltf_json = {
        "asset": {
            "version": "2.0",
            "generator": "glb-forge pure-python writer",
        },
        "scene": 0,
        "scenes": [
            {"nodes": [0]}
        ],
        "nodes": [
            {"mesh": 0, "name": mesh.name}
        ],
        "meshes": [
            {
                "name": mesh.name,
                "primitives": [
                    {
                        "attributes": {
                            "POSITION": 0,
                            "NORMAL": 1,
                        },
                        "indices": 2,
                        "material": 0,
                        "mode": TRIANGLES,
                    }
                ],
            }
        ],
        "materials": [
            {
                "name": f"{mesh.name} Material",
                "pbrMetallicRoughness": {
                    "baseColorFactor": list(mesh.color),
                    "metallicFactor": 0.0,
                    "roughnessFactor": 0.6,
                },
            }
        ],
        "buffers": [
            {
                "byteLength": len(bin_blob),
            }
        ],
        "bufferViews": [
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
            {
                "buffer": 0,
                "byteOffset": offset_indices,
                "byteLength": len(index_bytes),
                "target": ELEMENT_ARRAY_BUFFER,
            },
        ],
        "accessors": [
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
            {
                "bufferView": 2,
                "byteOffset": 0,
                "componentType": index_component_type,
                "count": len(indices),
                "type": "SCALAR",
            },
        ],
    }

    json_bytes = json.dumps(gltf_json, separators=(",", ":")).encode("utf-8")
    json_chunk = _pad4(json_bytes, b" ")

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
