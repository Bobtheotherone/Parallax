"""Deterministic BVH differential/work-count check and PNG file validation.

Run from the repository root after installation. Only the standard library is
used; these checks do not supply geometry, acceleration, or expected rendered pixels.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from random import Random
import struct
from time import perf_counter
import zlib

from parallax_raytracer.bvh import BVH, TraversalStats, brute_force
from parallax_raytracer.geometry import Ray, Sphere, Triangle
from parallax_raytracer.materials import Diffuse
from parallax_raytracer.math3d import WHITE, Vec3

if not __debug__:
    raise SystemExit("checks.py requires assertions: do not use -O or PYTHONOPTIMIZE")


def differential() -> dict:
    rng = Random(193817)
    material = Diffuse(WHITE)
    objects = []
    for x in range(-4, 5):
        for y in range(-2, 3):
            for z in range(-3, 4):
                center = Vec3(x*2.4, y*2.4, z*2.4)
                if (x+y+z) % 3:
                    objects.append(Sphere(center, rng.uniform(0.25, 0.8), material))
                else:
                    objects.append(Triangle(center + Vec3(-0.8, -0.6, 0.2),
                                            center + Vec3(0.7, -0.4, -0.1),
                                            center + Vec3(0.1, 0.8, 0.3), material))
    # Coincident geometry exercises identity ties across alternative traversal order.
    objects.extend((objects[0], objects[1]))
    objects = tuple(objects)
    tree = BVH(objects)
    accelerated, reference = TraversalStats(), TraversalStats()
    hit_count = 0
    start = perf_counter()
    for i in range(4000):
        origin = Vec3(*(rng.uniform(-16, 16) for _ in range(3)))
        if i % 4 == 0:
            # Aim at primitive interiors rather than letting most random rays miss.
            target = objects[rng.randrange(len(objects))]
            origin = target.center if isinstance(target, Sphere) else origin
            direction = Vec3(*(rng.uniform(-1, 1) for _ in range(3)))
        elif i % 4 == 1:
            target = objects[rng.randrange(len(objects))].bounds
            direction = Vec3(*(target.centroid(a) for a in range(3))) - origin
        elif i % 4 == 2:
            components = [0.0, -0.0, 0.0]
            components[i % 3] = 1.0 if i % 2 else -1.0
            direction = Vec3(*components)
        else:
            direction = Vec3(*(rng.uniform(-1, 1) for _ in range(3)))
        ray = Ray(origin, direction)
        t_min = 0.0 if i % 5 else 0.2
        t_max = math.inf if i % 3 else rng.uniform(0.3, 40)
        a = tree.nearest(ray, t_min, t_max, accelerated)
        b = brute_force(objects, ray, t_min, t_max, reference)
        assert (a is None) == (b is None), (i, a, b)
        if a is not None:
            hit_count += 1
            assert (a.t, a.primitive_id, a.front_face, a.normal) == (b.t, b.primitive_id, b.front_face, b.normal), (i, a, b)
    ratio = accelerated.primitive_tests / reference.primitive_tests
    assert hit_count > 1500, hit_count
    assert ratio < 0.20, f"BVH did not meaningfully reduce intersection work: {ratio}"
    return {"status": "PASS", "rays": 4000, "primitives": len(objects), "hits": hit_count,
            "bvh_primitive_tests": accelerated.primitive_tests,
            "brute_force_primitive_tests": reference.primitive_tests,
            "bvh_box_tests": accelerated.box_tests, "primitive_test_ratio": ratio,
            "elapsed_seconds": round(perf_counter()-start, 4),
            "scope": "shared primitives, distinct traversal; analytic geometry tests run separately"}


def validate_png(path: Path, width: int, height: int) -> dict:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "bad PNG signature"
    offset, compressed, dimensions, ended = 8, bytearray(), None, False
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset+4])[0]
        tag = data[offset+4:offset+8]
        payload = data[offset+8:offset+8+length]
        crc = struct.unpack(">I", data[offset+8+length:offset+12+length])[0]
        assert zlib.crc32(tag + payload) & 0xffffffff == crc, f"bad {tag!r} CRC"
        offset += length + 12
        if tag == b"IHDR":
            w, h, bits, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", payload)
            dimensions = w, h
            assert dimensions == (width, height), dimensions
            assert (bits, color, compression, filtering, interlace) == (8, 2, 0, 0, 0)
        elif tag == b"IDAT":
            compressed.extend(payload)
        elif tag == b"IEND":
            assert length == 0
            ended = True
            break
    assert ended and dimensions and offset == len(data), "incomplete PNG or trailing data"
    decoded = zlib.decompress(compressed)
    stride = width * 3 + 1
    assert len(decoded) == height * stride, "wrong decompressed image size"
    assert all(decoded[row*stride] in range(5) for row in range(height)), "invalid PNG filter"
    assert len(set(decoded)) > 16, "image stream is empty or suspiciously uniform"
    return {"status": "PASS", "path": str(path), "dimensions": list(dimensions),
            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "scope": "PNG signature, chunks/CRCs, RGB format, dimensions, decompression and scanlines"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path)
    parser.add_argument("--width", type=int, default=360)
    parser.add_argument("--height", type=int, default=225)
    args = parser.parse_args()
    report = {"bvh": differential()}
    if args.image:
        report["image"] = validate_png(args.image, args.width, args.height)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
