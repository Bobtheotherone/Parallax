# Prism Studio · CPU Raytracer

A small, original Python renderer: polished chrome, refractive glass, warm diffuse
ceramic, and a triangle-built teal sculpture share a checkerboard studio. Two
rectangular area lights produce direct illumination and soft cast shadows. The
floor, wall, pedestal, sculpture, and light panels are real triangle geometry.
There are no downloaded assets, rendering libraries, or scene files to prepare.

**Requires Python 3.11+ and pip.** Pillow is the only runtime dependency and only
encodes the completed RGB image. Everything that produces the pixels is Python.

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
| `render`, `image`, `cli` | Seeded pixel sampling, bounded process tasks, linear sample accumulation, Reinhard + sRGB display conversion, PNG encoding, argument/error adaptation |

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
background through geometry. There is no mesh loader, denoiser, GPU path, or GUI.

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
output, and repeated/single-versus-multiple-worker rendering. These are public,
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
