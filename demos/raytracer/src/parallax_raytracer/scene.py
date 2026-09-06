"""Immutable scene snapshot, rectangular area lights, and the default studio."""
from __future__ import annotations

from dataclasses import dataclass, field
from random import Random

from .bvh import BVH
from .camera import Camera
from .geometry import Primitive, Sphere, Triangle
from .materials import Checker, Dielectric, Diffuse, Emissive, Material, Mirror
from .math3d import Vec3


def quad(a: Vec3, b: Vec3, c: Vec3, d: Vec3, material: Material) -> tuple[Triangle, Triangle]:
    return Triangle(a, b, c, material), Triangle(a, c, d, material)


def box(lo: Vec3, hi: Vec3, material: Material) -> tuple[Triangle, ...]:
    if any(a >= b for a, b in zip(lo.xyz(), hi.xyz())):
        raise ValueError("box minimum must be strictly below maximum on every axis")
    a, b, c, d = (Vec3(lo.x, lo.y, lo.z), Vec3(hi.x, lo.y, lo.z),
                  Vec3(hi.x, hi.y, lo.z), Vec3(lo.x, hi.y, lo.z))
    e, f, g, h = (Vec3(lo.x, lo.y, hi.z), Vec3(hi.x, lo.y, hi.z),
                  Vec3(hi.x, hi.y, hi.z), Vec3(lo.x, hi.y, hi.z))
    return (quad(a, d, c, b, material) + quad(e, f, g, h, material)
            + quad(a, e, h, d, material) + quad(b, c, g, f, material)
            + quad(d, h, g, c, material) + quad(a, b, f, e, material))


@dataclass(frozen=True, slots=True)
class AreaLight:
    center: Vec3
    u: Vec3  # Half-edge, not necessarily unit length.
    v: Vec3
    radiance: Vec3
    normal: Vec3 = field(init=False)
    area: float = field(init=False)
    geometry: tuple[Triangle, Triangle] = field(init=False)

    def __post_init__(self) -> None:
        cross = self.u.cross(self.v)
        object.__setattr__(self, "normal", cross.unit())
        object.__setattr__(self, "area", 4.0 * cross.length())
        material = Emissive(self.radiance)
        c, u, v = self.center, self.u, self.v
        object.__setattr__(self, "geometry", quad(c-u-v, c+u-v, c+u+v, c-u+v, material))

    def sample(self, rng: Random) -> Vec3:
        return self.center + self.u * (2.0 * rng.random() - 1.0) + self.v * (2.0 * rng.random() - 1.0)


@dataclass(frozen=True, slots=True)
class Scene:
    objects: tuple[Primitive, ...]
    lights: tuple[AreaLight, ...] = ()
    ambient: Vec3 = Vec3(0.10, 0.13, 0.18)
    bvh: BVH = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        # Own a fixed snapshot, even if a caller supplies mutable input lists.
        objects = tuple(self.objects) + tuple(p for light in self.lights for p in light.geometry)
        object.__setattr__(self, "objects", objects)
        object.__setattr__(self, "lights", tuple(self.lights))
        object.__setattr__(self, "bvh", BVH(objects))

    @staticmethod
    def background(direction: Vec3) -> Vec3:
        t = max(0.0, min(1.0, direction.y * 0.5 + 0.5))
        return Vec3(0.10, 0.14, 0.21) * (1.0-t) + Vec3(0.48, 0.62, 0.82) * t


def showcase() -> tuple[Scene, Camera]:
    """The Prism Studio: chrome, clear glass, warm ceramic, faceted teal sculpture."""
    floor = Diffuse(Checker(Vec3(0.46, 0.52, 0.60), Vec3(0.105, 0.16, 0.23), 0.85))
    wall = Diffuse(Vec3(0.052, 0.078, 0.12))
    teal = Diffuse(Vec3(0.045, 0.50, 0.41))
    objects: list[Primitive] = list(quad(Vec3(-14, 0, -12), Vec3(-14, 0, 14),
                                          Vec3(14, 0, 14), Vec3(14, 0, -12), floor))
    objects.extend(quad(Vec3(-14, 0, -5), Vec3(14, 0, -5),
                        Vec3(14, 7, -5), Vec3(-14, 7, -5), wall))
    objects.extend([
        Sphere(Vec3(-1.65, 1.02, 0.35), 1.02, Mirror(Vec3(0.96, 0.98, 1.0))),
        Sphere(Vec3(0.9, 1.0, 1.05), 1.0, Dielectric(1.5, Vec3(0.055, 0.014, 0.007))),
        Sphere(Vec3(-0.15, 0.72, -1.85), 0.72, Diffuse(Vec3(0.80, 0.16, 0.07))),
        Sphere(Vec3(-3.25, 0.36, -1.7), 0.36, Diffuse(Vec3(0.90, 0.57, 0.12))),
    ])
    objects.extend(box(Vec3(1.1, 0, -2.4), Vec3(2.95, 0.22, -0.55),
                       Diffuse(Vec3(0.16, 0.21, 0.29))))
    ring = [Vec3(2.02 + x, 1.18, -1.48 + z)
            for x, z in ((-0.88, 0), (0, 0.88), (0.88, 0), (0, -0.88))]
    top, bottom = Vec3(2.02, 2.72, -1.48), Vec3(2.02, 0.22, -1.48)
    for index, vertex in enumerate(ring):
        next_vertex = ring[(index+1) % 4]
        objects.extend((Triangle(top, vertex, next_vertex, teal),
                        Triangle(bottom, next_vertex, vertex, teal)))
    # An architectural inlay, visible in reflections as well as directly.
    objects.extend(quad(Vec3(-5.5, 2.85, -4.99), Vec3(5.5, 2.85, -4.99),
                        Vec3(5.5, 2.89, -4.99), Vec3(-5.5, 2.89, -4.99),
                        Emissive(Vec3(1.0, 1.8, 2.8))))
    lights = (
        AreaLight(Vec3(-3.5, 6, 3.0), Vec3(2, 0, 0), Vec3(0, 0, 1.3), Vec3(18, 16, 13)),
        AreaLight(Vec3(3.5, 4.5, -2.7), Vec3(1.4, 0, 0), Vec3(0, 0.65, 1.2), Vec3(10, 15, 22)),
    )
    return Scene(tuple(objects), lights), Camera(Vec3(4.8, 3.3, 9.0), Vec3(0.05, 1.0, -0.3), 29)
