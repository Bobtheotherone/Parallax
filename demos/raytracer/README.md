# Prism Studio · CPU + Live GPU Raytracer

A small, original renderer with two execution paths: a deterministic Python CPU
reference and a progressive OpenGL-compute GPU viewer. Polished chrome, refractive
glass, warm diffuse ceramic, and a triangle-built teal sculpture share a checkerboard studio. Two
rectangular area lights produce direct illumination and soft cast shadows. The
floor, wall, pedestal, sculpture, and light panels are real triangle geometry.
There are no downloaded assets, rendering libraries, or scene files to prepare.

**Requires Python 3.11+ and pip.** The offline CPU path keeps Pillow as its only
runtime dependency. Live mode is an optional extra using ModernGL and GLFW to run
the authored ray/BVH/material shader on an OpenGL 4.3+ GPU.

## Quick Start

From the repository root on `demo/raytracer-control`, run this **one block**. The
first command installs the build tools and runtime dependency explicitly; the
editable install then needs no separate build-isolation download.

```sh
python -m pip install "setuptools>=77" "Pillow>=10"
python -m pip install --no-build-isolation -e ./demos/raytracer
python -m parallax_raytracer --output ./demos/raytracer/render.png
```

Open **`demos/raytracer/render.png`** in any image viewer. The default is 360 × 225,
4 samples per pixel, 7 secondary bounces, seed 20260905, and up to four CPU worker
processes. Progress goes to stderr; the final line gives the output and elapsed
time. The output is replaced atomically only after a successful render and encode.

## Live GPU mode

For a machine with an RTX 5090, install the optional viewer from the repository root
with `python -m pip install -e "./demos/raytracer[live]"`, then launch
`python -m parallax_raytracer.live` (or `parallax-raytracer-live`). The default window
is 1280 × 720 at full internal resolution. The same Python `showcase()` scene and
binned SAH BVH are packed into std430 buffers; an authored OpenGL 4.3 compute shader
performs intersections, BVH traversal, soft-shadow visibility, mirror recursion and
dielectric Fresnel/refraction on the GPU.

The viewer is **progressive**: while you move, accumulation is reset and the first
sample uses centered pixel/light sampling for a stable preview. When you stop, each
frame adds fresh anti-aliasing and area-light samples and the picture visibly cleans
up. The window title shows FPS, internal render resolution, accumulated samples per
pixel, and bounce depth.

Controls: **mouse** look, **W/A/S/D** fly, **Space/Ctrl** up/down, **Shift** boost,
**mouse wheel** field of view, **R** reset the camera, **Tab** release/capture the
mouse, and **Esc** quit. Useful 5090 settings include
`--width 1920 --height 1080 --spp-per-frame 2 --no-vsync`; for 4K, start with
`--width 3840 --height 2160 --render-scale 0.75` and raise the scale if the frame
rate remains comfortable. `--max-depth`, `--seed`, `--exposure`, `--move-speed`,
`--mouse-sensitivity`, and `--vsync/--no-vsync` are also available.

This path uses the 5090's general shader cores through OpenGL compute, **not the
dedicated RT cores**. For this compact BVH scene that still gives genuinely live
ray tracing without adding an OptiX/Vulkan dependency stack; the CPU renderer remains
the precision-oriented reference.

## Rendering controls

Both `python -m parallax_raytracer --help` and `parallax-raytracer --help` work.
Append options to the render command above:

| Option | Use |
|---|---|
| `--width 720 --height 450 --samples 64` | A much smoother, larger image; substantially more CPU work |
| `--samples 1` | Fast preview; square sample counts such as 4, 9, 16, 64 use 2D stratification |
| `--max-depth 10` | Retain more internal glass/mirror bounces; 0 disables secondary rays |
| `--workers 1` | Single-process execution for profiling or constrained environments |
| `--seed 123` | Change sampling, not scene geometry; repeat a seed to reproduce a render |
| `--exposure 1.5` | Brighten linear radiance before highlight mapping and sRGB conversion |
| `--output path/to/image.png --quiet` | Choose an output, create its parents, suppress row progress |

Non-square sample counts are supported without dropping samples. Dimensions are
1..8192, with a 16,777,216-pixel memory guard; samples are 1..4096, depth is 0..16,
and workers are 1..32. These are bounds, not promises that extreme settings are
quick. Pixel results do not depend on worker scheduling or worker count. Exact
PNG byte reproducibility is scoped to the same Python/Pillow environment.

## Architecture and numerical behavior

The library is under `src/parallax_raytracer/`. Construct `Sphere`, `Triangle`,
materials, `AreaLight`, `Scene`, and `Camera` directly to render a different scene;
`render(scene, camera, config)` returns packed RGB bytes, separately from file I/O.
The supplied `showcase()` is just one scene builder, not a specialized image generator.
When embedding multiple workers, use the normal Python `if __name__ == "__main__"`
guard; the CLI already does this.

| Module | Responsibility |
|---|---|
| `math3d`, `geometry` | Vectors, normalized rays, spheres, ray-aligned triangle edge tests, oriented normals, conservative boxes and surface offsets |
| `bvh` | Binned surface-area-heuristic construction and near-first traversal; stable scene-order ties; separate brute-force comparison path |
| `materials`, `integrator` | Lambert diffuse, tinted ideal mirror, Snell refraction, Schlick Fresnel, total internal reflection, Beer absorption, lighting and visibility |
| `scene`, `camera` | Immutable scene snapshots, finite geometry, explicit lights, perspective projection |
| `gpu_scene`, `live`, `shaders/` | Scene/BVH std430 packing, fly camera/input, OpenGL compute traversal/shading, progressive accumulation and live display |
| `render`, `image`, `cli` | Seeded CPU pixel sampling, bounded process tasks, linear sample accumulation, Reinhard + sRGB display conversion, PNG encoding, argument/error adaptation |

All normal rays, including shadows and recursive rays, use the BVH. Intersections
select the nearest distance in `(t_min, t_max]`. Sphere roots avoid the large-distance
discriminant cancellation; triangle edge functions include shared edges without a
world-space expansion. Normals face against the incident ray, retaining the original
outward normal for entering/exiting tests. Spawn offsets use a small floating-point
ULP error budget and outward rounding, not a large fixed scene epsilon. Geometry
constructors reject nonfinite or degenerate inputs. Arithmetic is double precision;
the tests cover uniform scales from 1e-8 to 1e8, not every ill-conditioned geometry.

### Deliberate scope

This is a Whitted-style technology demo, **not an unbiased path tracer**. Diffuse
surfaces receive sampled direct lighting plus a small explicit environment fill;
there is no diffuse global illumination. Glass view rays bend correctly, but shadow
rays use straight-line Fresnel/Beer attenuation, so there are no focused caustics.
Dielectrics must be non-overlapping closed solids surrounded by air: nested media,
participating volumes, dispersion, and rough microfacet transmission are not modeled.
The bounce limit intentionally discards untraced specular energy rather than leaking
background through geometry. There is no mesh loader, denoiser, diffuse global illumination, RT-core backend, or editor UI. The live viewer is a fly-through frontend for the built-in showcase rather than a scene authoring tool.

## Verification

From the repository root after installation, run
`python -m unittest discover -s demos/raytracer/tests -v`, then
`python demos/raytracer/checks.py --image ./demos/raytracer/render.png`.
The latter validates PNG structure, CRCs, dimensions, decompression, and scanlines,
and compares the BVH with brute force on 4,000 deterministic rays through 317 mixed
primitives, reporting actual intersection work. Pass `--width` and `--height` to
validate a non-default image.

The focused tests use analytic geometry/optics expectations, inside/outside and
surface-origin cases, shared triangle edges, scale and slab boundaries, direct-light
occlusion, depth termination, pixel normalization, subprocess errors, atomic image
output, repeated/single-versus-multiple-worker rendering, GPU-buffer layout, shader
resource interfaces, and live-camera invariants. These are public,
same-author checks with implementation diversity, not a held-out oracle or proof.
Visual inspection of the generated showcase remains a separate acceptance step.

## Methodology provenance

CONTROL, base `2a7a5a48e2e2238a5b02e1f5edffabb475235aad`, work branch
`demo/raytracer-control`. All 51 Markdown files at that base were read before design.
The selected route is **DIRECT**: small typed Python interfaces expose the actual
geometry, numerical invariants, and data flow. A rendering library is disallowed by
the task, the existing integer-sequence pack does not implement these semantics,
and a new capsule or language would add acquisition and validation work without
removing a meaningful renderer decision. Parallax's existing files and semantics
are unchanged; no other methodology branch or external raytracer source was used.
