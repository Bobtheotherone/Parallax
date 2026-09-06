"""Linear RGB materials and explicit air/solid dielectric interface optics."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import TypeAlias

from .math3d import BLACK, WHITE, Vec3, reflect


def _color(value: Vec3, *, bounded: bool = True) -> None:
    if not value.finite() or min(value.xyz()) < 0 or (bounded and max(value.xyz()) > 1):
        raise ValueError("color must be finite, nonnegative, and at most 1 for reflectance")


@dataclass(frozen=True, slots=True)
class Checker:
    a: Vec3
    b: Vec3
    size: float = 1.0

    def __post_init__(self) -> None:
        _color(self.a)
        _color(self.b)
        if not math.isfinite(self.size) or self.size <= 0:
            raise ValueError("checker size must be finite and positive")

    def at(self, point: Vec3) -> Vec3:
        cell = math.floor(point.x / self.size) + math.floor(point.z / self.size)
        return self.a if cell % 2 == 0 else self.b


@dataclass(frozen=True, slots=True)
class Diffuse:
    albedo: Vec3 | Checker

    def __post_init__(self) -> None:
        if isinstance(self.albedo, Vec3):
            _color(self.albedo)
        elif not isinstance(self.albedo, Checker):
            raise ValueError("diffuse albedo must be a color or Checker")

    def at(self, point: Vec3) -> Vec3:
        return self.albedo.at(point) if isinstance(self.albedo, Checker) else self.albedo


@dataclass(frozen=True, slots=True)
class Mirror:
    tint: Vec3 = WHITE

    def __post_init__(self) -> None:
        _color(self.tint)


@dataclass(frozen=True, slots=True)
class Dielectric:
    ior: float = 1.5
    absorption: Vec3 = BLACK  # Beer-Lambert extinction coefficients per scene unit.

    def __post_init__(self) -> None:
        if not math.isfinite(self.ior) or self.ior <= 0:
            raise ValueError("index of refraction must be finite and positive")
        _color(self.absorption, bounded=False)

    def attenuation(self, distance: float) -> Vec3:
        return Vec3(math.exp(-self.absorption.x * distance),
                    math.exp(-self.absorption.y * distance),
                    math.exp(-self.absorption.z * distance))


@dataclass(frozen=True, slots=True)
class Emissive:
    radiance: Vec3

    def __post_init__(self) -> None:
        _color(self.radiance, bounded=False)


Material: TypeAlias = Diffuse | Mirror | Dielectric | Emissive


def interface(direction: Vec3, normal: Vec3, eta_i: float,
              eta_t: float) -> tuple[Vec3, Vec3 | None, float]:
    """Reflection, refraction, Fresnel weight. Normal faces against incident ray.

    Snell's law uses the incident/transmitted indices, NOT a fixed air/glass ratio.
    Schlick uses the lower-index-side cosine, approaching one at the critical angle.
    A missing refracted direction means total internal reflection.
    """
    reflected = reflect(direction, normal)
    if eta_i == eta_t:
        return reflected, direction, 0.0
    cosine_i = max(0.0, min(1.0, -direction.dot(normal)))
    ratio = eta_i / eta_t
    sine_t_squared = ratio * ratio * max(0.0, 1.0 - cosine_i * cosine_i)
    if sine_t_squared >= 1.0:
        return reflected, None, 1.0
    cosine_t = math.sqrt(max(0.0, 1.0 - sine_t_squared))
    refracted = direction * ratio + normal * (ratio * cosine_i - cosine_t)
    r0 = ((eta_i - eta_t) / (eta_i + eta_t)) ** 2
    cosine = cosine_t if eta_i > eta_t else cosine_i
    fresnel = r0 + (1.0 - r0) * (1.0 - cosine) ** 5
    return reflected, refracted, fresnel
