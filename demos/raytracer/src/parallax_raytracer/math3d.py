"""Double-precision vector arithmetic; directions are normalized at ray creation."""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, value: float) -> Vec3:
        return Vec3(self.x * value, self.y * value, self.z * value)

    __rmul__ = __mul__

    def __truediv__(self, value: float) -> Vec3:
        return Vec3(self.x / value, self.y / value, self.z / value)

    def hadamard(self, other: Vec3) -> Vec3:
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def dot(self, other: Vec3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def length(self) -> float:
        return math.hypot(self.x, self.y, self.z)

    def unit(self) -> Vec3:
        length = self.length()
        if not math.isfinite(length) or length == 0:
            raise ValueError("direction must be finite and nonzero")
        return self / length

    def xyz(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    def finite(self) -> bool:
        return math.isfinite(self.x) and math.isfinite(self.y) and math.isfinite(self.z)


BLACK = Vec3(0.0, 0.0, 0.0)
WHITE = Vec3(1.0, 1.0, 1.0)


def reflect(direction: Vec3, normal: Vec3) -> Vec3:
    """Both inputs are unit vectors; normal orientation does not change reflection."""
    return direction - normal * (2.0 * direction.dot(normal))
