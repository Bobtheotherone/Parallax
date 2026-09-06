"""Deterministic pixel sampling, bounded row tasks, and linear-light accumulation."""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import math
import multiprocessing
import os
from random import Random
from typing import Callable

from .camera import Camera
from .integrator import trace
from .math3d import BLACK
from .scene import Scene


@dataclass(frozen=True, slots=True)
class RenderConfig:
    width: int = 360
    height: int = 225
    samples: int = 4
    max_depth: int = 7
    seed: int = 20260905
    exposure: float = 1.0
    workers: int = min(4, os.cpu_count() or 1)

    def __post_init__(self) -> None:
        for name, lo, hi in (("width", 1, 8192), ("height", 1, 8192),
                             ("samples", 1, 4096), ("max_depth", 0, 16), ("workers", 1, 32)):
            value = getattr(self, name)
            if type(value) is not int or not lo <= value <= hi:
                raise ValueError(f"{name} must be an integer in [{lo}, {hi}]")
        if self.width * self.height > 16_777_216:
            raise ValueError("image must not exceed 16,777,216 pixels")
        if type(self.seed) is not int:
            raise ValueError("seed must be an integer")
        if not math.isfinite(self.exposure) or not 0 < self.exposure <= 128:
            raise ValueError("exposure must be finite and in (0, 128]")


def display_channel(linear: float, exposure: float = 1.0) -> int:
    """Reinhard highlight mapping followed by the piecewise sRGB transfer function."""
    if not math.isfinite(linear):
        raise ArithmeticError("nonfinite radiance reached image output")
    linear = max(0.0, linear) * exposure
    mapped = 1.0 - 1.0 / (1.0 + linear)
    encoded = 12.92 * mapped if mapped <= 0.0031308 else 1.055 * mapped ** (1 / 2.4) - 0.055
    return min(255, max(0, int(encoded * 255.0 + 0.5)))


def _tile(scene: Scene, camera: Camera, config: RenderConfig, start: int, end: int) -> tuple[int, bytes]:
    data = bytearray()
    width, height, samples = config.width, config.height, config.samples
    strata = math.isqrt(samples)
    square = strata * strata == samples
    for y in range(start, end):
        for x in range(width):
            # No global RNG, Python hash(), task-order dependence, or per-worker seed.
            pixel = y * width + x
            seed = ((config.seed & ((1 << 64)-1)) ^ ((pixel + 1) * 0x9E3779B97F4A7C15))
            rng = Random(seed)
            total = BLACK
            for sample in range(samples):
                if samples == 1:
                    dx = dy = 0.5
                elif square:
                    dx = (sample % strata + rng.random()) / strata
                    dy = (sample // strata + rng.random()) / strata
                else:
                    dx, dy = rng.random(), rng.random()
                ray = camera.ray((x + dx) / width, (y + dy) / height, width / height)
                total = total + trace(scene, ray, config.max_depth, rng)
            # Average in linear space before tone mapping and display conversion.
            data.extend(display_channel(c / samples, config.exposure) for c in total.xyz())
    return start, bytes(data)


# Worker-local, read-only snapshot. The parent never uses this state; the
# initializer owns its lifetime, avoiding scene serialization for every row task.
_worker_context: tuple[Scene, Camera, RenderConfig] | None = None


def _initialize(scene: Scene, camera: Camera, config: RenderConfig) -> None:
    global _worker_context
    _worker_context = scene, camera, config


def _work(bounds: tuple[int, int]) -> tuple[int, bytes]:
    if _worker_context is None:
        raise RuntimeError("render worker was not initialized")
    return _tile(*_worker_context, *bounds)


def render(scene: Scene, camera: Camera, config: RenderConfig,
           progress: Callable[[int, int], None] | None = None) -> bytes:
    """Return packed RGB bytes. Same scene/config gives identical pixels across workers.

    Embedders using multiple workers must call this from a guarded main function,
    as with any spawn-based multiprocessing program. The supplied CLI does so.
    """
    bounds = [(y, min(y + 8, config.height)) for y in range(0, config.height, 8)]
    output = bytearray(config.width * config.height * 3)

    def collect(results) -> None:
        for start, data in results:
            offset = start * config.width * 3
            output[offset:offset + len(data)] = data
            if progress:
                progress(min(start + 8, config.height), config.height)

    if config.workers == 1:
        collect(_tile(scene, camera, config, a, b) for a, b in bounds)
    else:
        with ProcessPoolExecutor(max_workers=config.workers,
                                 mp_context=multiprocessing.get_context("spawn"),
                                 initializer=_initialize, initargs=(scene, camera, config)) as pool:
            collect(pool.map(_work, bounds, chunksize=1))
    return bytes(output)
