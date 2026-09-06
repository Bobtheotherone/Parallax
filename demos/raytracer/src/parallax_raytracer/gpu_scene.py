"""Serialize the existing CPU scene/BVH into simple std430 GPU buffers.

The live renderer deliberately reuses the exact Scene and BVH construction path.
Only the traversal/intersection implementation changes from Python to GLSL.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct

from .geometry import Sphere, Triangle
from .materials import Checker, Dielectric, Diffuse, Emissive, Material, Mirror
from .scene import Scene


PRIMITIVE_SPHERE = 0
PRIMITIVE_TRIANGLE = 1
MATERIAL_DIFFUSE = 0
MATERIAL_CHECKER = 1
MATERIAL_MIRROR = 2
MATERIAL_DIELECTRIC = 3
MATERIAL_EMISSIVE = 4


@dataclass(frozen=True, slots=True)
class PackedScene:
    primitives: bytes
    materials: bytes
    lights: bytes
    node_bounds: bytes
    node_meta: bytes
    leaf_indices: bytes
    primitive_count: int
    material_count: int
    light_count: int
    node_count: int
    leaf_index_count: int


def _pack_material(material: Material) -> bytes:
    """Three vec4 values (48 bytes), matching the GLSL Material struct."""
    p0 = [0.0, 0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0, 0.0]
    p2 = [0.0, 0.0, 0.0, 0.0]
    if isinstance(material, Diffuse):
        if isinstance(material.albedo, Checker):
            p0[:3] = material.albedo.a.xyz()
            p0[3] = float(MATERIAL_CHECKER)
            p1[:3] = material.albedo.b.xyz()
            p1[3] = material.albedo.size
        else:
            p0[:3] = material.albedo.xyz()
            p0[3] = float(MATERIAL_DIFFUSE)
    elif isinstance(material, Mirror):
        p0[:3] = material.tint.xyz()
        p0[3] = float(MATERIAL_MIRROR)
    elif isinstance(material, Dielectric):
        p0[:3] = material.absorption.xyz()
        p0[3] = float(MATERIAL_DIELECTRIC)
        p2[0] = material.ior
    elif isinstance(material, Emissive):
        p0[:3] = material.radiance.xyz()
        p0[3] = float(MATERIAL_EMISSIVE)
    else:  # pragma: no cover - Material is a closed union in the public module.
        raise TypeError(f"unsupported GPU material: {type(material).__name__}")
    return struct.pack("<12f", *p0, *p1, *p2)


def pack_scene(scene: Scene) -> PackedScene:
    """Create immutable little-endian buffers for the OpenGL 4.3 compute path."""
    material_ids: dict[Material, int] = {}
    material_chunks: list[bytes] = []

    def material_id(material: Material) -> int:
        existing = material_ids.get(material)
        if existing is not None:
            return existing
        index = len(material_chunks)
        material_ids[material] = index
        material_chunks.append(_pack_material(material))
        return index

    primitive_chunks: list[bytes] = []
    for primitive in scene.objects:
        mid = material_id(primitive.material)
        if isinstance(primitive, Sphere):
            values = (*primitive.center.xyz(), primitive.radius,
                      0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0)
            primitive_chunks.append(struct.pack("<12f4i", *values,
                                                PRIMITIVE_SPHERE, mid, 0, 0))
        elif isinstance(primitive, Triangle):
            values = (*primitive.a.xyz(), 0.0,
                      *primitive.b.xyz(), 0.0,
                      *primitive.c.xyz(), 0.0)
            primitive_chunks.append(struct.pack("<12f4i", *values,
                                                PRIMITIVE_TRIANGLE, mid, 0, 0))
        else:  # pragma: no cover - Primitive is a closed union in geometry.py.
            raise TypeError(f"unsupported GPU primitive: {type(primitive).__name__}")

    light_chunks = [struct.pack("<16f",
                                *light.center.xyz(), 0.0,
                                *light.u.xyz(), 0.0,
                                *light.v.xyz(), 0.0,
                                *light.radiance.xyz(), 0.0)
                    for light in scene.lights]

    leaf_indices: list[int] = []
    bounds_chunks: list[bytes] = []
    meta_chunks: list[bytes] = []
    for node in scene.bvh.nodes:
        bounds_chunks.append(struct.pack("<8f", *node.bounds.lo, 0.0, *node.bounds.hi, 0.0))
        if node.indices:
            start = len(leaf_indices)
            leaf_indices.extend(node.indices)
            meta_chunks.append(struct.pack("<4i", -1, -1, start, len(node.indices)))
        else:
            meta_chunks.append(struct.pack("<4i", node.left, node.right, -1, 0))

    return PackedScene(
        primitives=b"".join(primitive_chunks),
        materials=b"".join(material_chunks),
        lights=b"".join(light_chunks),
        node_bounds=b"".join(bounds_chunks),
        node_meta=b"".join(meta_chunks),
        leaf_indices=struct.pack(f"<{len(leaf_indices)}i", *leaf_indices) if leaf_indices else b"",
        primitive_count=len(primitive_chunks),
        material_count=len(material_chunks),
        light_count=len(light_chunks),
        node_count=len(bounds_chunks),
        leaf_index_count=len(leaf_indices),
    )
