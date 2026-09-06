"""Finite geometry. Intersection intervals are (t_min, t_max]; ties keep scene order.

Triangles use ray-aligned shear coordinates and shared edge functions. No fixed
world-space epsilon is used to expand triangles or discard positive intersections.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import TypeAlias

from .materials import Material
from .math3d import Vec3


@dataclass(frozen=True, slots=True)
class Ray:
    origin: Vec3
    direction: Vec3
    o: tuple[float, float, float] = field(init=False, repr=False)
    d: tuple[float, float, float] = field(init=False, repr=False)
    shear: tuple[int, int, int, float, float] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.origin.finite():
            raise ValueError("ray origin must be finite")
        direction = self.direction.unit()
        object.__setattr__(self, "direction", direction)
        object.__setattr__(self, "o", self.origin.xyz())
        coordinates = direction.xyz()
        object.__setattr__(self, "d", coordinates)
        kz = 0
        if abs(coordinates[1]) > abs(coordinates[kz]):
            kz = 1
        if abs(coordinates[2]) > abs(coordinates[kz]):
            kz = 2
        kx, ky = (kz + 1) % 3, (kz + 2) % 3
        object.__setattr__(self, "shear", (kx, ky, kz, coordinates[kx] / coordinates[kz],
                                          coordinates[ky] / coordinates[kz]))

    def at(self, t: float) -> Vec3:
        return self.origin + self.direction * t


@dataclass(frozen=True, slots=True)
class Bounds:
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]

    @classmethod
    def points(cls, *points: Vec3) -> Bounds:
        coordinates = [p.xyz() for p in points]
        # Outward rounding also gives planar triangles conservative nonzero boxes.
        return cls(tuple(math.nextafter(min(p[a] for p in coordinates), -math.inf)
                         for a in range(3)),
                   tuple(math.nextafter(max(p[a] for p in coordinates), math.inf)
                         for a in range(3)))

    def union(self, other: Bounds) -> Bounds:
        return Bounds(tuple(min(a, b) for a, b in zip(self.lo, other.lo)),
                      tuple(max(a, b) for a, b in zip(self.hi, other.hi)))

    def entry(self, ray: Ray, t_min: float, t_max: float) -> float | None:
        for origin, direction, lo, hi in zip(ray.o, ray.d, self.lo, self.hi):
            if direction == 0.0:  # Includes signed zero; avoids 0 * infinity / NaN.
                if origin < lo or origin > hi:
                    return None
                continue
            a, b = (lo - origin) / direction, (hi - origin) / direction
            if a > b:
                a, b = b, a
            # Conservative slab rounding prevents a grazing primitive being culled.
            a = math.nextafter(a, -math.inf)
            b = math.nextafter(b, math.inf)
            if a > t_min:
                t_min = a
            if b < t_max:
                t_max = b
            if t_max < t_min:
                return None
        return t_min

    def area(self) -> float:
        x, y, z = (b - a for a, b in zip(self.lo, self.hi))
        return 2.0 * (x*y + y*z + z*x)

    def centroid(self, axis: int) -> float:
        return self.lo[axis] * 0.5 + self.hi[axis] * 0.5


@dataclass(frozen=True, slots=True)
class Sphere:
    center: Vec3
    radius: float
    material: Material
    bounds: Bounds = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.center.finite() or not math.isfinite(self.radius) or self.radius <= 0:
            raise ValueError("sphere requires finite center and positive finite radius")
        r = Vec3(self.radius, self.radius, self.radius)
        object.__setattr__(self, "bounds", Bounds.points(self.center - r, self.center + r))

    def intersect(self, ray: Ray, t_min: float, t_max: float) -> float | None:
        x = ray.origin.x - self.center.x
        y = ray.origin.y - self.center.y
        z = ray.origin.z - self.center.z
        dx, dy, dz = ray.d
        a = dx * dx + dy * dy + dz * dz
        b = x * dx + y * dy + z * dz
        # Cross-product distance avoids subtracting two O(distance^2) terms in
        # the discriminant for small spheres far along the viewing direction.
        cx, cy, cz = y * dz - z * dy, z * dx - x * dz, x * dy - y * dx
        disc = self.radius * self.radius * a - (cx * cx + cy * cy + cz * cz)
        if disc < 0.0:
            return None
        q = -b - math.copysign(math.sqrt(disc), b)
        if q == 0.0:
            root = -b / a
            return root if t_min < root <= t_max else None
        length = math.hypot(x, y, z)
        c = (length - self.radius) * (length + self.radius)
        first, second = q / a, c / q
        if first > second:
            first, second = second, first
        if t_min < first <= t_max:
            return first
        return second if t_min < second <= t_max else None

    def surface(self, ray: Ray, t: float) -> tuple[Vec3, Vec3, float]:
        outward = (ray.at(t) - self.center).unit()
        # Reproject the computed point to the sphere, reducing accumulated error.
        return self.center + outward * self.radius, outward, self.radius


@dataclass(frozen=True, slots=True)
class Triangle:
    a: Vec3
    b: Vec3
    c: Vec3
    material: Material
    bounds: Bounds = field(init=False, repr=False)
    normal: Vec3 = field(init=False, repr=False)
    scale: float = field(init=False, repr=False)
    vertices: tuple = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not all(p.finite() for p in (self.a, self.b, self.c)):
            raise ValueError("triangle vertices must be finite")
        ab, ac = self.b - self.a, self.c - self.a
        # Normalize edges before their cross product to avoid unnecessary
        # overflow/underflow in geometry at very large/small uniform scales.
        normal = ab.unit().cross(ac.unit()).unit()
        object.__setattr__(self, "normal", normal)
        object.__setattr__(self, "scale", max(ab.length(), ac.length()))
        object.__setattr__(self, "vertices", (self.a.xyz(), self.b.xyz(), self.c.xyz()))
        object.__setattr__(self, "bounds", Bounds.points(self.a, self.b, self.c))

    def intersect(self, ray: Ray, t_min: float, t_max: float) -> float | None:
        d, o = ray.d, ray.o
        kx, ky, kz, sx, sy = ray.shear
        a, b, c = self.vertices
        az, bz, cz = a[kz] - o[kz], b[kz] - o[kz], c[kz] - o[kz]
        ax, ay = a[kx] - o[kx] - sx * az, a[ky] - o[ky] - sy * az
        bx, by = b[kx] - o[kx] - sx * bz, b[ky] - o[ky] - sy * bz
        cx, cy = c[kx] - o[kx] - sx * cz, c[ky] - o[ky] - sy * cz
        ea, eb, ec = bx * cy - by * cx, cx * ay - cy * ax, ax * by - ay * bx
        if min(ea, eb, ec) < 0.0 < max(ea, eb, ec):
            return None
        det = ea + eb + ec
        if det == 0.0:
            return None
        t = ((ea * az + eb * bz + ec * cz) / det) / d[kz]
        return t if t_min < t <= t_max else None

    def surface(self, ray: Ray, t: float) -> tuple[Vec3, Vec3, float]:
        return ray.at(t), self.normal, self.scale


Primitive: TypeAlias = Sphere | Triangle


@dataclass(frozen=True, slots=True)
class Hit:
    t: float
    point: Vec3
    outward: Vec3
    normal: Vec3  # Oriented against incident direction, even for interior hits.
    front_face: bool
    material: Material
    primitive_id: int
    error: float

    @classmethod
    def make(cls, ray: Ray, t: float, primitive: Primitive, index: int) -> Hit:
        point, outward, scale = primitive.surface(ray, t)
        front = ray.direction.dot(outward) < 0.0
        magnitude = max(abs(t), scale, *(abs(v) for v in ray.o),
                        *(abs(v) for v in point.xyz()))
        # A small arithmetic error budget in ulps, NOT a scene-sized epsilon.
        return cls(t, point, outward, outward if front else -outward,
                   front, primitive.material, index, 32.0 * math.ulp(magnitude))

    def offset(self, direction: Vec3) -> Vec3:
        n = self.outward if direction.dot(self.outward) >= 0.0 else -self.outward
        shifted = self.point + n * self.error
        # Round away from the surface on each nonzero component.
        values = tuple(math.nextafter(p, math.inf if d > 0 else -math.inf) if d else p
                       for p, d in zip(shifted.xyz(), n.xyz()))
        return Vec3(*values)

    def spawn(self, direction: Vec3) -> Ray:
        return Ray(self.offset(direction), direction)
