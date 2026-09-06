"""Command-line adapter; rendering math and scene construction do not own I/O."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from time import perf_counter

from . import __version__
from .image import write_png
from .render import RenderConfig, render
from .scene import showcase


def main(argv: list[str] | None = None) -> int:
    defaults = RenderConfig()
    parser = argparse.ArgumentParser(
        prog="parallax-raytracer",
        description="Render the Prism Studio with an original Python CPU raytracer.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--output", type=Path, default=Path("render.png"), help="PNG destination; parents are created")
    parser.add_argument("--width", type=int, default=defaults.width, help="image width in pixels (1..8192)")
    parser.add_argument("--height", type=int, default=defaults.height, help="image height in pixels (1..8192)")
    parser.add_argument("--samples", type=int, default=defaults.samples, help="samples per pixel (1..4096); square counts stratify in 2D")
    parser.add_argument("--max-depth", type=int, default=defaults.max_depth, help="maximum secondary-ray bounces (0..16)")
    parser.add_argument("--seed", type=int, default=defaults.seed, help="deterministic pixel sampling seed")
    parser.add_argument("--exposure", type=float, default=defaults.exposure, help="linear exposure multiplier (0..128]")
    parser.add_argument("--workers", type=int, default=defaults.workers, help="CPU processes (1..32); default uses up to four logical CPUs")
    parser.add_argument("--quiet", action="store_true", help="suppress row progress, not the final timing")
    args = parser.parse_args(argv)
    try:
        config = RenderConfig(args.width, args.height, args.samples, args.max_depth,
                              args.seed, args.exposure, args.workers)
        if args.output.suffix.lower() != ".png":
            raise ValueError("output must have a .png extension")
        if args.output.exists() and not args.output.is_file():
            raise ValueError("output is not a regular file")
    except ValueError as exc:
        parser.error(str(exc))
    last = -1

    def progress(done: int, total: int) -> None:
        nonlocal last
        percentage = done * 100 // total
        if percentage // 10 != last:
            last = percentage // 10
            print(f"Rendering {percentage:3d}%", file=sys.stderr)

    start = perf_counter()
    try:
        scene, camera = showcase()
        pixels = render(scene, camera, config, None if args.quiet else progress)
        write_png(args.output, config.width, config.height, pixels)
    except (OSError, ValueError, ArithmeticError) as exc:
        print(f"raytracer: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("raytracer: interrupted; no partial output saved", file=sys.stderr)
        return 130
    elapsed = perf_counter() - start
    print(f"Saved {args.output} | {config.width}x{config.height} | {config.samples} spp | "
          f"depth {config.max_depth} | seed {config.seed} | {config.workers} worker(s) | {elapsed:.3f}s")
    return 0
