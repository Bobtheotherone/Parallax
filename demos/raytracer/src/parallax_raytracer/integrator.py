"""Whitted recursion, Lambertian direct lighting, transmissive shadow visibility.

Glass is a closed solid surrounded by air. Nested/overlapping media are not
modeled. Visibility through glass is a straight-ray attenuation approximation;
view rays refract, but this direct-light estimator does not simulate caustics.
"""
from __future__ import annotations

import math
from random import Random

from .geometry import Hit, Ray
from .materials import Dielectric, Diffuse, Emissive, Mirror, interface
from .math3d import BLACK, WHITE, Vec3, reflect
from .scene import Scene


def visibility(scene: Scene, ray: Ray, distance: float) -> Vec3:
    """Finite light segment: opaque occlusion or Fresnel/Beer glass transmission."""
    transmission = WHITE
    remaining = distance - 64.0 * math.ulp(distance)
    # A straight line intersects each sphere at most twice and each triangle
    # once. This is a scene-derived safety bound, not unbounded self-hit retry.
    for _ in range(2 * len(scene.objects) + 1):
        hit = scene.bvh.nearest(ray, t_max=remaining)
        if hit is None:
            return transmission
        material = hit.material
        if not isinstance(material, Dielectric):
            return BLACK
        eta_i, eta_t = (1.0, material.ior) if hit.front_face else (material.ior, 1.0)
        _, refracted, fresnel = interface(ray.direction, hit.normal, eta_i, eta_t)
        if refracted is None:
            return BLACK
        transmission = transmission * (1.0 - fresnel)
        if not hit.front_face:
            transmission = transmission.hadamard(material.attenuation(hit.t))
        advanced = hit.spawn(ray.direction)
        remaining -= hit.t + (advanced.origin - hit.point).dot(ray.direction)
        ray = advanced
        if remaining <= 0:
            return transmission
    raise ArithmeticError("visibility did not advance through finite scene geometry")


def direct(scene: Scene, hit: Hit, material: Diffuse, rng: Random) -> Vec3:
    albedo = material.at(hit.point)
    # An explicit low-cost environment fill, not a claim of global illumination.
    color = albedo.hadamard(scene.ambient) * (0.55 + 0.45 * max(0.0, hit.normal.y))
    for light in scene.lights:
        target = light.sample(rng)
        delta = target - hit.point
        distance = delta.length()
        if distance == 0:
            continue
        direction = delta / distance
        cosine = max(0.0, hit.normal.dot(direction))
        emitter_cosine = max(0.0, -light.normal.dot(direction))
        if cosine == 0.0 or emitter_cosine == 0.0:
            continue
        origin = hit.offset(direction)
        # Recompute the endpoint after moving the origin off the surface.
        delta = target - origin
        distance = delta.length()
        shadow = Ray(origin, delta)
        transmitted = visibility(scene, shadow, distance)
        weight = cosine * emitter_cosine * light.area / (math.pi * distance * distance)
        color = color + albedo.hadamard(light.radiance).hadamard(transmitted) * weight
    return color


def trace(scene: Scene, ray: Ray, depth: int, rng: Random) -> Vec3:
    hit = scene.bvh.nearest(ray)
    if hit is None:
        return scene.background(ray.direction)
    material = hit.material
    if isinstance(material, Emissive):
        return material.radiance if hit.front_face else BLACK
    if isinstance(material, Diffuse):
        return direct(scene, hit, material, rng)
    if depth == 0:
        return BLACK  # No invented environment leak through an untraced interface.
    if isinstance(material, Mirror):
        return material.tint.hadamard(trace(scene, hit.spawn(reflect(ray.direction, hit.normal)),
                                            depth - 1, rng))
    if isinstance(material, Dielectric):
        eta_i, eta_t = (1.0, material.ior) if hit.front_face else (material.ior, 1.0)
        reflected, refracted, fresnel = interface(ray.direction, hit.normal, eta_i, eta_t)
        color = (trace(scene, hit.spawn(reflected), depth - 1, rng) * fresnel
                 if fresnel > 0.0 else BLACK)
        if refracted is not None and fresnel < 1.0:
            color = color + trace(scene, hit.spawn(refracted), depth - 1, rng) * (1.0 - fresnel)
        if not hit.front_face:
            color = color.hadamard(material.attenuation(hit.t))
        return color
    raise TypeError(f"unsupported material: {type(material).__name__}")
