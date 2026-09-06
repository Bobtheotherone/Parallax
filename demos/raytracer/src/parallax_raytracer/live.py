"""Interactive OpenGL-compute raytracing frontend.

The module imports without GPU/window dependencies. Install the ``live`` extra and
run ``python -m parallax_raytracer.live`` (or ``parallax-raytracer-live``) to open
the progressive renderer.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from importlib import resources
import math
import sys
from time import perf_counter

from . import __version__
from .gpu_scene import PackedScene, pack_scene
from .math3d import Vec3
from .scene import showcase


@dataclass(frozen=True, slots=True)
class LiveConfig:
    width: int = 1280
    height: int = 720
    render_scale: float = 1.0
    max_depth: int = 7
    seed: int = 20260905
    exposure: float = 1.0
    move_speed: float = 4.0
    mouse_sensitivity: float = 0.0020
    spp_per_frame: int = 1
    vsync: bool = True
    frames: int = 0

    def __post_init__(self) -> None:
        for name, lo, hi in (("width", 320, 7680), ("height", 240, 4320),
                             ("max_depth", 0, 16), ("spp_per_frame", 1, 8),
                             ("frames", 0, 1_000_000)):
            value = getattr(self, name)
            if type(value) is not int or not lo <= value <= hi:
                raise ValueError(f"{name} must be an integer in [{lo}, {hi}]")
        if self.width * self.height > 33_177_600:
            raise ValueError("window must not exceed 33,177,600 pixels")
        if type(self.seed) is not int:
            raise ValueError("seed must be an integer")
        for name, value, lo, hi in (
            ("render_scale", self.render_scale, 0.25, 1.0),
            ("exposure", self.exposure, 0.01, 128.0),
            ("move_speed", self.move_speed, 0.05, 100.0),
            ("mouse_sensitivity", self.mouse_sensitivity, 0.0001, 0.02),
        ):
            if not math.isfinite(value) or not lo <= value <= hi:
                raise ValueError(f"{name} must be finite and in [{lo}, {hi}]")


@dataclass(slots=True)
class LiveCamera:
    eye: Vec3
    yaw: float
    pitch: float
    vertical_fov: float

    @classmethod
    def from_camera(cls, camera) -> "LiveCamera":
        forward = camera.forward
        return cls(camera.eye,
                   math.atan2(forward.x, -forward.z),
                   math.asin(max(-1.0, min(1.0, forward.y))),
                   camera.vertical_fov)

    def basis(self) -> tuple[Vec3, Vec3, Vec3]:
        cp = math.cos(self.pitch)
        forward = Vec3(math.sin(self.yaw) * cp,
                       math.sin(self.pitch),
                       -math.cos(self.yaw) * cp).unit()
        world_up = Vec3(0.0, 1.0, 0.0)
        right = forward.cross(world_up).unit()
        vertical = right.cross(forward).unit()
        return forward, right, vertical

    def look(self, dx: float, dy: float, sensitivity: float) -> None:
        self.yaw += dx * sensitivity
        self.pitch = max(math.radians(-89.0), min(math.radians(89.0),
                                                  self.pitch - dy * sensitivity))

    def move(self, right_amount: float, up_amount: float, forward_amount: float,
             distance: float) -> bool:
        if right_amount == up_amount == forward_amount == 0.0:
            return False
        forward, right, _ = self.basis()
        delta = right * right_amount + Vec3(0.0, 1.0, 0.0) * up_amount + forward * forward_amount
        self.eye = self.eye + delta.unit() * distance
        return True

    def zoom(self, scroll_y: float) -> bool:
        if scroll_y == 0:
            return False
        self.vertical_fov = max(15.0, min(90.0, self.vertical_fov - scroll_y * 2.0))
        return True


def shader_source(name: str) -> str:
    return (resources.files("parallax_raytracer") / "shaders" / name).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    defaults = LiveConfig()
    parser = argparse.ArgumentParser(
        prog="parallax-raytracer-live",
        description="Explore the Prism Studio with a progressive GPU raytracer.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--width", type=int, default=defaults.width, help="initial window width")
    parser.add_argument("--height", type=int, default=defaults.height, help="initial window height")
    parser.add_argument("--render-scale", type=float, default=defaults.render_scale,
                        help="internal raytracing resolution as a fraction of the framebuffer")
    parser.add_argument("--max-depth", type=int, default=defaults.max_depth,
                        help="maximum specular/refraction bounces")
    parser.add_argument("--seed", type=int, default=defaults.seed,
                        help="deterministic progressive sampling seed")
    parser.add_argument("--exposure", type=float, default=defaults.exposure,
                        help="linear exposure before display mapping")
    parser.add_argument("--move-speed", type=float, default=defaults.move_speed,
                        help="camera movement speed in scene units/second")
    parser.add_argument("--mouse-sensitivity", type=float, default=defaults.mouse_sensitivity,
                        help="mouse-look radians per pixel")
    parser.add_argument("--spp-per-frame", type=int, default=defaults.spp_per_frame,
                        help="samples accumulated per displayed frame while stationary")
    parser.add_argument("--vsync", action=argparse.BooleanOptionalAction, default=defaults.vsync,
                        help="synchronize presentation to the display refresh rate")
    parser.add_argument("--frames", type=int, default=defaults.frames,
                        help="auto-exit after this many displayed frames; 0 runs interactively")
    return parser


def _load_dependencies():
    try:
        import glfw  # type: ignore
        import moderngl  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "live mode requires optional dependencies; install with "
            "python -m pip install -e './demos/raytracer[live]'"
        ) from exc
    return glfw, moderngl


class _GPUScene:
    def __init__(self, ctx, packed: PackedScene):
        # OpenGL does not permit zero-sized buffer objects. The showcase has all
        # buffer classes populated; one-word fallbacks keep generic packing safe.
        self.buffers = [
            ctx.buffer(packed.primitives or b"\x00" * 64),
            ctx.buffer(packed.materials or b"\x00" * 48),
            ctx.buffer(packed.lights or b"\x00" * 64),
            ctx.buffer(packed.node_bounds or b"\x00" * 32),
            ctx.buffer(packed.node_meta or b"\x00" * 16),
            ctx.buffer(packed.leaf_indices or b"\x00" * 4),
        ]
        for binding, buffer in enumerate(self.buffers):
            buffer.bind_to_storage_buffer(binding)

    def release(self) -> None:
        for buffer in self.buffers:
            buffer.release()


def _run(config: LiveConfig) -> int:
    glfw, moderngl = _load_dependencies()
    errors: list[str] = []

    def error_callback(code, description):
        text = description.decode("utf-8", "replace") if isinstance(description, bytes) else str(description)
        errors.append(f"GLFW {code}: {text}")

    glfw.set_error_callback(error_callback)
    if not glfw.init():
        detail = errors[-1] if errors else "GLFW initialization failed"
        raise RuntimeError(detail)

    window = None
    gpu_scene = None
    accumulation = None
    vao = None
    compute = None
    display = None
    try:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        window = glfw.create_window(config.width, config.height, "Prism Studio Live", None, None)
        if not window:
            detail = errors[-1] if errors else "could not create an OpenGL 4.3 window"
            raise RuntimeError(detail)
        glfw.make_context_current(window)
        glfw.swap_interval(1 if config.vsync else 0)
        ctx = moderngl.create_context(require=430)

        compute = ctx.compute_shader(shader_source("live.comp.glsl"))
        display = ctx.program(vertex_shader=shader_source("display.vert.glsl"),
                              fragment_shader=shader_source("display.frag.glsl"))
        vao = ctx.vertex_array(display, [])

        scene, camera = showcase()
        packed = pack_scene(scene)
        gpu_scene = _GPUScene(ctx, packed)
        compute["u_light_count"].value = packed.light_count
        compute["u_node_count"].value = packed.node_count
        compute["u_max_depth"].value = config.max_depth
        compute["u_seed"].value = config.seed & 0xFFFFFFFF
        display["u_accum"].value = 0
        display["u_exposure"].value = config.exposure

        initial = LiveCamera.from_camera(camera)
        live_camera = LiveCamera(initial.eye, initial.yaw, initial.pitch, initial.vertical_fov)
        mouse_captured = True
        mouse_dirty = False
        reset_requested = False
        first_mouse = True
        last_cursor = (0.0, 0.0)

        def apply_capture(enabled: bool) -> None:
            nonlocal mouse_captured, first_mouse
            mouse_captured = enabled
            first_mouse = True
            glfw.set_input_mode(window, glfw.CURSOR,
                                glfw.CURSOR_DISABLED if enabled else glfw.CURSOR_NORMAL)
            if hasattr(glfw, "RAW_MOUSE_MOTION") and glfw.raw_mouse_motion_supported():
                glfw.set_input_mode(window, glfw.RAW_MOUSE_MOTION,
                                    glfw.TRUE if enabled else glfw.FALSE)

        def cursor_callback(_window, x: float, y: float) -> None:
            nonlocal first_mouse, last_cursor, mouse_dirty
            if not mouse_captured:
                last_cursor = (x, y)
                return
            if first_mouse:
                last_cursor = (x, y)
                first_mouse = False
                return
            dx, dy = x - last_cursor[0], y - last_cursor[1]
            last_cursor = (x, y)
            if dx or dy:
                live_camera.look(dx, dy, config.mouse_sensitivity)
                mouse_dirty = True

        def scroll_callback(_window, _x: float, y: float) -> None:
            nonlocal mouse_dirty
            mouse_dirty = live_camera.zoom(y) or mouse_dirty

        def key_callback(_window, key: int, _scancode: int, action: int, _mods: int) -> None:
            nonlocal reset_requested
            if action != glfw.PRESS:
                return
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)
            elif key == glfw.KEY_TAB:
                apply_capture(not mouse_captured)
            elif key == glfw.KEY_R:
                reset_requested = True

        glfw.set_cursor_pos_callback(window, cursor_callback)
        glfw.set_scroll_callback(window, scroll_callback)
        glfw.set_key_callback(window, key_callback)
        apply_capture(True)

        print("Prism Studio Live controls:")
        print("  Mouse      look around      W/A/S/D   move")
        print("  Space/Ctrl move up/down     Shift     boost")
        print("  Wheel      change FOV       R         reset camera")
        print("  Tab        release/capture mouse       Esc quit")
        print(f"OpenGL renderer: {ctx.info.get('GL_RENDERER', 'unknown')}")
        print(f"OpenGL version:  {ctx.info.get('GL_VERSION', 'unknown')}")

        sample_index = 0
        render_size = (0, 0)
        last_time = perf_counter()
        title_time = last_time
        title_frames = 0
        title_fps = 0.0
        displayed_frames = 0

        while not glfw.window_should_close(window):
            glfw.poll_events()
            now = perf_counter()
            dt = min(0.1, max(0.0, now - last_time))
            last_time = now

            dirty = mouse_dirty
            mouse_dirty = False
            if reset_requested:
                live_camera.eye = initial.eye
                live_camera.yaw = initial.yaw
                live_camera.pitch = initial.pitch
                live_camera.vertical_fov = initial.vertical_fov
                reset_requested = False
                dirty = True

            right_amount = float(glfw.get_key(window, glfw.KEY_D) == glfw.PRESS) - float(
                glfw.get_key(window, glfw.KEY_A) == glfw.PRESS)
            up_amount = float(glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS) - float(
                glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS or
                glfw.get_key(window, glfw.KEY_RIGHT_CONTROL) == glfw.PRESS)
            forward_amount = float(glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) - float(
                glfw.get_key(window, glfw.KEY_S) == glfw.PRESS)
            boost = 3.0 if (glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or
                            glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS) else 1.0
            dirty = live_camera.move(right_amount, up_amount, forward_amount,
                                     config.move_speed * boost * dt) or dirty

            fb_width, fb_height = glfw.get_framebuffer_size(window)
            if fb_width <= 0 or fb_height <= 0:
                glfw.wait_events_timeout(0.05)
                continue
            wanted = (max(1, int(round(fb_width * config.render_scale))),
                      max(1, int(round(fb_height * config.render_scale))))
            if wanted != render_size:
                if accumulation is not None:
                    accumulation.release()
                accumulation = ctx.texture(wanted, 4, dtype="f4")
                accumulation.filter = (moderngl.LINEAR, moderngl.LINEAR)
                accumulation.bind_to_image(0, read=True, write=True)
                render_size = wanted
                dirty = True

            if dirty:
                sample_index = 0

            forward, right, vertical = live_camera.basis()
            compute["u_resolution"].value = render_size
            compute["u_eye"].value = live_camera.eye.xyz()
            compute["u_forward"].value = forward.xyz()
            compute["u_right"].value = right.xyz()
            compute["u_vertical"].value = vertical.xyz()
            compute["u_half_height"].value = math.tan(math.radians(live_camera.vertical_fov) / 2.0)
            compute["u_aspect"].value = render_size[0] / render_size[1]

            dispatches = 1 if dirty else config.spp_per_frame
            for _ in range(dispatches):
                compute["u_sample"].value = sample_index
                compute.run(group_x=(render_size[0] + 7) // 8,
                            group_y=(render_size[1] + 7) // 8,
                            group_z=1)
                sample_index += 1
            ctx.memory_barrier()

            ctx.screen.use()
            ctx.viewport = (0, 0, fb_width, fb_height)
            accumulation.use(location=0)
            vao.render(mode=moderngl.TRIANGLES, vertices=3)
            glfw.swap_buffers(window)
            displayed_frames += 1
            if config.frames and displayed_frames >= config.frames:
                glfw.set_window_should_close(window, True)

            title_frames += 1
            if now - title_time >= 0.5:
                title_fps = title_frames / (now - title_time)
                title_frames = 0
                title_time = now
                glfw.set_window_title(
                    window,
                    f"Prism Studio Live | {title_fps:5.1f} FPS | {render_size[0]}x{render_size[1]} | "
                    f"{sample_index} spp | depth {config.max_depth} | Tab releases mouse",
                )
        return 0
    finally:
        if accumulation is not None:
            accumulation.release()
        if vao is not None:
            vao.release()
        if display is not None:
            display.release()
        if compute is not None:
            compute.release()
        if gpu_scene is not None:
            gpu_scene.release()
        if window is not None:
            glfw.destroy_window(window)
        glfw.terminate()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        config = LiveConfig(args.width, args.height, args.render_scale, args.max_depth,
                            args.seed, args.exposure, args.move_speed,
                            args.mouse_sensitivity, args.spp_per_frame, args.vsync, args.frames)
    except ValueError as exc:
        parser.error(str(exc))
    try:
        return _run(config)
    except RuntimeError as exc:
        print(f"raytracer-live: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("raytracer-live: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
