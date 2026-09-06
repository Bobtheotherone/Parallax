"""Pinhole perspective camera, vertical field of view in degrees, world Y up."""
from __future__ import annotations

from dataclasses import dataclass, field
import math

from .geometry import Ray
from .math3d import Vec3


@dataclass(frozen=True, slots=True)
class Camera:
    eye: Vec3
    target: Vec3
    vertical_fov: float = 43.0
    up: Vec3 = Vec3(0.0, 1.0, 0.0)
    forward: Vec3 = field(init=False, repr=False)
    right: Vec3 = field(init=False, repr=False)
    vertical: Vec3 = field(init=False, repr=False)
    half_height: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.eye.finite() or not self.target.finite():
            raise ValueError("camera positions must be finite")
        if not math.isfinite(self.vertical_fov) or not 0 < self.vertical_fov < 179:
            raise ValueError("vertical field of view must be between 0 and 179 degrees")
        forward = (self.target - self.eye).unit()
        right = forward.cross(self.up).unit()
        object.__setattr__(self, "forward", forward)
        object.__setattr__(self, "right", right)
        object.__setattr__(self, "vertical", right.cross(forward).unit())
        object.__setattr__(self, "half_height", math.tan(math.radians(self.vertical_fov) / 2))

    def ray(self, u: float, v: float, aspect: float) -> Ray:
        # u and v span the image; v=0 is the TOP, avoiding an output-side flip.
        horizontal = (2.0 * u - 1.0) * aspect * self.half_height
        vertical = (1.0 - 2.0 * v) * self.half_height
        return Ray(self.eye, self.forward + self.right * horizontal + self.vertical * vertical)
