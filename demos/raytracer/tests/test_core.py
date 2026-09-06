"""Analytic expectations and adversarial boundaries, not golden-image self-validation."""
from __future__ import annotations

from dataclasses import replace
import math
from random import Random
import unittest
from unittest.mock import patch

from parallax_raytracer.bvh import BVH
from parallax_raytracer.camera import Camera
from parallax_raytracer.geometry import Bounds, Hit, Ray, Sphere, Triangle
from parallax_raytracer.integrator import trace, visibility
from parallax_raytracer.materials import Dielectric, Diffuse, Emissive, Mirror, interface
from parallax_raytracer.math3d import BLACK, WHITE, Vec3, reflect
from parallax_raytracer.render import RenderConfig, display_channel, render
from parallax_raytracer.scene import AreaLight, Scene, box, quad, showcase

MAT = Diffuse(WHITE)


class GeometryTests(unittest.TestCase):
    def assertVector(self, actual, expected, tolerance=1e-11):
        self.assertLessEqual((actual - expected).length(), tolerance)

    def test_unit_ray_camera_and_reflection(self):
        ray = Ray(Vec3(0, 0, 0), Vec3(0, 0, -9))
        self.assertVector(ray.direction, Vec3(0, 0, -1))
        with self.assertRaises(ValueError):
            Ray(BLACK, BLACK)
        with self.assertRaises(ValueError):
            Ray(BLACK, Vec3(math.nan, 0, 1))
        camera = Camera(Vec3(0, 0, 3), BLACK, 90)
        self.assertVector(camera.ray(0.5, 0.5, 1).direction, Vec3(0, 0, -1))
        corner = camera.ray(1, 0, 1).direction
        self.assertVector(corner, Vec3(1, 1, -1).unit())
        incoming = Vec3(1, -1, 0).unit()
        self.assertVector(reflect(incoming, Vec3(0, 1, 0)), Vec3(1, 1, 0).unit())
        with self.assertRaises(ValueError):
            Camera(BLACK, BLACK)
        with self.assertRaises(ValueError):
            Camera(BLACK, Vec3(0, 1, 0))  # Up and view direction are parallel.

    def test_sphere_roots_inside_tangent_and_surface_origins(self):
        sphere = Sphere(BLACK, 1, MAT)
        cases = ((Vec3(0, 0, 3), Vec3(0, 0, -1), 2),
                 (BLACK, Vec3(1, 0, 0), 1),
                 (Vec3(1, 0, 3), Vec3(0, 0, -1), 3),
                 (Vec3(0, 0, 1), Vec3(0, 0, -1), 2),
                 (Vec3(0, 0, 1), Vec3(0, 0, 1), None),
                 (Vec3(0, 0, 3), Vec3(0, 0, 1), None))
        for origin, direction, expected in cases:
            with self.subTest(origin=origin, direction=direction):
                self.assertEqual(sphere.intersect(Ray(origin, direction), 0, math.inf), expected)
        self.assertIsNone(sphere.intersect(Ray(Vec3(0, 0, 3), Vec3(0, 0, -1)), 0, 1.9))
        hit = BVH((sphere,)).nearest(Ray(BLACK, Vec3(1, 0, 0)))
        self.assertFalse(hit.front_face)
        self.assertVector(hit.normal, Vec3(-1, 0, 0))
        for radius in (0, -1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                Sphere(BLACK, radius, MAT)

    def test_distant_small_sphere_does_not_collapse_discriminant(self):
        sphere = Sphere(Vec3(0, 0, -100_000_000), 1, MAT)
        self.assertAlmostEqual(sphere.intersect(Ray(BLACK, Vec3(0, 0, -1)), 0, math.inf),
                               99_999_999, delta=2e-8)
        self.assertIsNone(sphere.intersect(Ray(Vec3(1.01, 0, 0), Vec3(0, 0, -1)), 0, math.inf))

    def test_scale_aware_offsets_do_not_skip_nearby_geometry(self):
        for scale in (1e-8, 1.0, 1e8):
            with self.subTest(scale=scale):
                sphere = Sphere(BLACK, scale, MAT)
                incoming = Ray(Vec3(0, 0, 3*scale), Vec3(0, 0, -1))
                hit = BVH((sphere,)).nearest(incoming)
                self.assertTrue(hit.front_face)
                outward = hit.spawn(Vec3(0, 0, 1))
                self.assertIsNone(BVH((sphere,)).nearest(outward))
                inward = hit.spawn(Vec3(0, 0, -1))
                exit_hit = BVH((sphere,)).nearest(inward)
                self.assertFalse(exit_hit.front_face)
                self.assertAlmostEqual(exit_hit.t / scale, 2.0, delta=1e-12)
                close = Sphere(Vec3(0, 0, 2.000001*scale), scale, MAT)
                self.assertIsNotNone(BVH((close,)).nearest(outward))
                self.assertLess(hit.error / scale, 1e-12)

    def test_triangle_edges_winding_parallel_and_uniform_scale(self):
        for scale in (1e-8, 1, 1e8):
            a, b, c, d = (Vec3(0, 0, 0), Vec3(scale, 0, 0),
                          Vec3(scale, scale, 0), Vec3(0, scale, 0))
            triangles = quad(a, b, c, d, MAT)
            for x, y in ((0, 0), (1, 1), (0.5, 0.5), (0, 0.4), (0.999999, 0.3)):
                ray = Ray(Vec3(x*scale, y*scale, scale), Vec3(0, 0, -1))
                hits = [t.intersect(ray, 0, math.inf) for t in triangles]
                self.assertTrue(any(t is not None for t in hits), (scale, x, y))
                accelerated = BVH(triangles).nearest(ray)
                self.assertAlmostEqual(accelerated.t / scale, 1.0, delta=1e-12)
            backward = Triangle(c, b, a, MAT)
            self.assertIsNotNone(backward.intersect(Ray(Vec3(0.75*scale, 0.25*scale, -scale),
                                                       Vec3(0, 0, 1)), 0, math.inf))
            self.assertIsNone(triangles[0].intersect(Ray(Vec3(0.5*scale, 0.25*scale, scale),
                                                       Vec3(1, 0, 0)), 0, math.inf))
        for vertices in ((BLACK, BLACK, WHITE), (BLACK, WHITE, WHITE*2)):
            with self.assertRaises(ValueError):
                Triangle(*vertices, MAT)

    def test_aabb_parallel_grazing_inside_and_finite_segment(self):
        bounds = Bounds((0, 0, 0), (1, 1, 1))
        self.assertIsNotNone(bounds.entry(Ray(Vec3(0, 0.5, -1), Vec3(-0.0, 0, 1)), 0, 3))
        self.assertIsNone(bounds.entry(Ray(Vec3(-1e-8, 0.5, -1), Vec3(0, 0, 1)), 0, 3))
        self.assertIsNotNone(bounds.entry(Ray(Vec3(-1, -1, -1), WHITE), 0, math.inf))
        self.assertEqual(bounds.entry(Ray(Vec3(0.5, 0.5, 0.5), WHITE), 0, math.inf), 0)
        self.assertIsNone(bounds.entry(Ray(Vec3(0.5, 0.5, -3), Vec3(1e-310, 0, 1)), 0, 2))
        # The direction is nonzero but too small to form a finite reciprocal.
        self.assertIsNotNone(bounds.entry(Ray(Vec3(0, 0.5, -1), Vec3(1e-310, 0, 1)), 0, 3))

    def test_nearest_hit_and_tie_identity(self):
        near = Sphere(BLACK, 1, MAT)
        far = Sphere(Vec3(0, 0, -4), 1, MAT)
        ray = Ray(Vec3(0, 0, 5), Vec3(0, 0, -1))
        self.assertEqual(BVH((far, near, near)).nearest(ray).primitive_id, 1)
        self.assertEqual(BVH((near,)*9).nearest(ray).primitive_id, 0)
        self.assertIsNone(BVH(()).nearest(ray))
        self.assertEqual(len(box(BLACK, WHITE, MAT)), 12)


class OpticsTests(unittest.TestCase):
    def test_snell_enter_exit_fresnel_and_total_internal_reflection(self):
        normal = Vec3(0, 1, 0)
        direction = Vec3(math.sin(math.pi/4), -math.cos(math.pi/4), 0)
        _, transmitted, weight = interface(direction, normal, 1, 1.5)
        self.assertAlmostEqual(transmitted.x, math.sin(math.pi/4) / 1.5)
        self.assertAlmostEqual(transmitted.length(), 1)
        self.assertGreater(weight, 0.04)
        # Reversibility is a strong discriminator for index/orientation mistakes.
        _, reverse, _ = interface(-transmitted, -normal, 1.5, 1)
        self.assertLess((reverse + direction).length(), 1e-12)
        _, normal_ray, normal_weight = interface(Vec3(0, -1, 0), normal, 1, 1.5)
        self.assertEqual(normal_ray, Vec3(0, -1, 0))
        self.assertAlmostEqual(normal_weight, 0.04)
        theta = math.radians(50)
        _, transmitted, weight = interface(Vec3(math.sin(theta), -math.cos(theta), 0), normal, 1.5, 1)
        self.assertIsNone(transmitted)
        self.assertEqual(weight, 1)
        _, transmitted, weight = interface(direction, normal, 1.0, 1.0)
        self.assertEqual(transmitted, direction)
        self.assertEqual(weight, 0)
        with self.assertRaises(ValueError):
            Dielectric(0)

    def test_beer_thickness_and_glass_shadow_interfaces(self):
        glass = Dielectric(1.5, Vec3(0.2, 0.1, 0.0))
        ray = Ray(Vec3(0, 0, 3), Vec3(0, 0, -1))
        scene = Scene((Sphere(BLACK, 1, glass),))
        actual = visibility(scene, ray, 6)
        expected = Vec3(math.exp(-0.4), math.exp(-0.2), 1) * (0.96**2)
        self.assertLess((actual - expected).length(), 1e-10)
        opaque = Scene((Sphere(BLACK, 1, MAT),))
        self.assertEqual(visibility(opaque, ray, 6), BLACK)
        self.assertEqual(visibility(opaque, ray, 1.5), WHITE)  # Blocker beyond endpoint.

    def test_reflective_and_index_matched_view_paths_and_depth(self):
        mirror = Sphere(BLACK, 1, Mirror(Vec3(1, 0.5, 0.25)))
        emitter = quad(Vec3(-3, -3, 5), Vec3(-3, 3, 5), Vec3(3, 3, 5), Vec3(3, -3, 5),
                       Emissive(Vec3(2, 2, 2)))
        ray = Ray(Vec3(0, 0, 3), Vec3(0, 0, -1))
        scene = Scene((mirror, *emitter))
        self.assertEqual(trace(scene, ray, 1, Random(1)), Vec3(2, 1, 0.5))
        self.assertEqual(trace(scene, ray, 0, Random(1)), BLACK)
        clear = Scene((Sphere(BLACK, 1, Dielectric(1.0)),))
        self.assertEqual(trace(clear, ray, 2, Random(1)), clear.background(ray.direction))
        self.assertEqual(trace(clear, ray, 1, Random(1)), BLACK)
        # Camera inside the solid still exits correctly.
        self.assertEqual(trace(clear, Ray(BLACK, Vec3(0, 0, 1)), 1, Random(1)),
                         clear.background(Vec3(0, 0, 1)))

    def test_lambert_area_light_inverse_square_and_occlusion(self):
        class CenterSamples:
            @staticmethod
            def random():
                return 0.5

        floor = quad(Vec3(-3, 0, -3), Vec3(-3, 0, 3), Vec3(3, 0, 3), Vec3(3, 0, -3),
                     Diffuse(Vec3(0.5, 0.5, 0.5)))
        ray = Ray(Vec3(0, 0.5, 0), Vec3(0, -1, 0))
        light = AreaLight(Vec3(0, 3, 0), Vec3(1, 0, 0), Vec3(0, 0, 1), Vec3(6, 6, 6))
        scene = Scene(floor, (light,), BLACK)
        actual = trace(scene, ray, 0, CenterSamples())
        self.assertAlmostEqual(actual.x, 0.5 * 6 * 4 / (math.pi * 9), delta=1e-12)
        farther = Scene(floor, (replace(light, center=Vec3(0, 6, 0)),), BLACK)
        self.assertAlmostEqual(trace(farther, ray, 0, CenterSamples()).x, actual.x/4, delta=1e-12)
        shadowed = Scene((*floor, Sphere(Vec3(0, 1.5, 0), 0.25, MAT)), (light,), BLACK)
        self.assertEqual(trace(shadowed, ray, 0, CenterSamples()), BLACK)


class SamplingTests(unittest.TestCase):
    def test_linear_sample_average_and_display_conversion(self):
        self.assertEqual(display_channel(0), 0)
        self.assertEqual(display_channel(-2), 0)
        self.assertEqual(display_channel(1), 188)  # Linear 1 -> mapped 0.5 -> sRGB.
        self.assertEqual(display_channel(0.5, 2.0), 188)
        self.assertEqual(display_channel(1e300), 255)
        with self.assertRaises(ArithmeticError):
            display_channel(math.nan)
        scene, camera = Scene(()), Camera(Vec3(0, 0, 3), BLACK)
        with patch("parallax_raytracer.render.trace", return_value=Vec3(1, 0.5, 0.25)):
            for samples in (1, 4, 7, 9):
                image = render(scene, camera, RenderConfig(2, 3, samples, workers=1))
                expected = bytes((188, display_channel(0.5), display_channel(0.25))) * 6
                self.assertEqual(image, expected)

        with patch("parallax_raytracer.render.trace", side_effect=[BLACK, Vec3(2, 0, 0)]):
            image = render(scene, camera, RenderConfig(1, 1, 2, workers=1))
            self.assertEqual(image, bytes((188, 0, 0)))  # Not the average of display values.

    def test_determinism_across_repetition_and_worker_count(self):
        scene, camera = showcase()
        config = RenderConfig(24, 16, 4, 5, 27, workers=1)
        first = render(scene, camera, config)
        self.assertEqual(first, render(scene, camera, config))
        self.assertEqual(first, render(scene, camera, replace(config, workers=2)))
        self.assertNotEqual(first, render(scene, camera, replace(config, seed=28)))
        self.assertGreater(len(set(first)), 50)

    def test_configuration_boundaries(self):
        for values in ({"samples": 0}, {"width": -1}, {"height": 0}, {"max_depth": -1},
                       {"max_depth": 17}, {"workers": 0}, {"exposure": math.nan}, {"width": True}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                RenderConfig(**values)


if __name__ == "__main__":
    unittest.main()
