"""Pillow is used only here, to encode the renderer's already-complete RGB buffer."""
from __future__ import annotations

import os
from pathlib import Path
import tempfile


def write_png(path: str | Path, width: int, height: int, pixels: bytes) -> None:
    if width < 1 or height < 1 or len(pixels) != width * height * 3:
        raise ValueError("RGB buffer length does not match positive image dimensions")
    path = Path(path)
    if path.suffix.lower() != ".png":
        raise ValueError("output path must have a .png extension")
    from PIL import Image

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".raytracer-", suffix=".png", delete=False) as file:
            temporary = file.name
            with Image.frombytes("RGB", (width, height), pixels) as image:
                image.save(file, format="PNG")
        # A failed render/encode never leaves a half-written or truncated output.
        os.replace(temporary, path)
    finally:
        if temporary is not None and os.path.exists(temporary):
            os.unlink(temporary)
