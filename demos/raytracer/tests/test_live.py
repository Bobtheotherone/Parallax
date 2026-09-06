"""Pure-Python checks for the live renderer's host-side contracts."""
from __future__ import annotations

import math
import struct
import unittest

from parallax_raytracer.gpu_scene import (
    MATERIAL_CHECKER,
    MATERIAL_DIELECTRIC,
    MATERIAL_EMISSIVE,
    MATERIAL_MIRROR,
    PRIMITIVE_SPHERE,
    PRIMITIVE_TRIANGLE,
    pack_scene,
)
from parallax_raytracer.live import LiveCamera, LiveConfig, shader_source
from parallax_raytracer.math3d import Vec3
from parallax_raytracer.scene import showcase


class GPUScenePackingTests(unittest.TestCase):
    def test_showcase_packing_matches_cpu_scene_and_bvh(self):
        scene, _ = showcase()
        packed = pack_scene(scene)
        self.assertEqual(packed.primitive_count, len(scene.objects))
        self.assertEqual(packed.light_count, len(scene.lights))
        self.assertEqual(packed.node_count, len(scene.bvh.nodes))
        self.assertEqual(len(packed.primitives), packed.primitive_count * 64)
        self.assertEqual(len(packed.materials), packed.material_count * 48)
        self.assertEqual(len(packed.lights), packed.light_count * 64)
        self.assertEqual(len(packed.node_bounds), packed.node_count * 32)
        self.assertEqual(len(packed.node_meta), packed.node_count * 16)
        self.assertEqual(len(packed.leaf_indices), packed.leaf_index_count * 4)

        leaf_ids = struct.unpack(f"<{packed.leaf_index_count}i", packed.leaf_indices)
        self.assertEqual(sorted(leaf_ids), list(range(len(scene.objects))))

        primitive_types = []
        material_ids = []
        for offset in range(0, len(packed.primitives), 64):
            values = struct.unpack_from("<12f4i", packed.primitives, offset)
            primitive_types.append(values[12])
            material_ids.append(values[13])
        self.assertIn(PRIMITIVE_SPHERE, primitive_types)
        self.assertIn(PRIMITIVE_TRIANGLE, primitive_types)
        self.assertTrue(all(0 <= mid < packed.material_count for mid in material_ids))

        material_types = [round(struct.unpack_from("<12f", packed.materials, offset)[3])
                          for offset in range(0, len(packed.materials), 48)]
        for expected in (MATERIAL_CHECKER, MATERIAL_MIRROR,
                         MATERIAL_DIELECTRIC, MATERIAL_EMISSIVE):
            self.assertIn(expected, material_types)

    def test_shader_resources_have_expected_interfaces(self):
        compute = shader_source("live.comp.glsl")
        self.assertIn("#version 430 core", compute)
        self.assertIn("layout(local_size_x = 8", compute)
        self.assertIn("readonly buffer PrimitiveBuffer", compute)
        self.assertIn("nearest_hit", compute)
        self.assertIn("dielectric_interface", compute)
        self.assertIn("visibility", compute)
        self.assertIn("u_sample == 0u", compute)
        self.assertIn("#version 430 core", shader_source("display.vert.glsl"))
        self.assertIn("linear_to_srgb", shader_source("display.frag.glsl"))


class LiveCameraTests(unittest.TestCase):
    def test_basis_is_orthonormal_and_movement_is_bounded(self):
        camera = LiveCamera(Vec3(1, 2, 3), 0.7, -0.2, 45.0)
        forward, right, vertical = camera.basis()
        for vector in (forward, right, vertical):
            self.assertAlmostEqual(vector.length(), 1.0)
        self.assertAlmostEqual(forward.dot(right), 0.0, places=12)
        self.assertAlmostEqual(forward.dot(vertical), 0.0, places=12)
        self.assertAlmostEqual(right.dot(vertical), 0.0, places=12)
        old = camera.eye
        self.assertTrue(camera.move(1, 1, 1, 2.5))
        self.assertAlmostEqual((camera.eye - old).length(), 2.5)
        self.assertFalse(camera.move(0, 0, 0, 3.0))

    def test_look_zoom_and_configuration_bounds(self):
        camera = LiveCamera(Vec3(0, 0, 0), 0, 0, 45)
        camera.look(0, 1e9, 0.002)
        self.assertGreaterEqual(camera.pitch, math.radians(-89))
        camera.look(0, -1e9, 0.002)
        self.assertLessEqual(camera.pitch, math.radians(89))
        camera.zoom(1000)
        self.assertEqual(camera.vertical_fov, 15)
        camera.zoom(-1000)
        self.assertEqual(camera.vertical_fov, 90)

        for values in ({"render_scale": 0.1}, {"max_depth": 17}, {"spp_per_frame": 0},
                       {"move_speed": 0}, {"mouse_sensitivity": math.nan}, {"width": 100}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                LiveConfig(**values)


if __name__ == "__main__":
    unittest.main()
