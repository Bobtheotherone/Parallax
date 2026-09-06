#version 430 core

layout(local_size_x = 8, local_size_y = 8, local_size_z = 1) in;
layout(rgba32f, binding = 0) uniform image2D u_accum_image;

struct Primitive {
    vec4 a;
    vec4 b;
    vec4 c;
    ivec4 meta;
};

struct Material {
    vec4 p0;
    vec4 p1;
    vec4 p2;
};

struct Light {
    vec4 center;
    vec4 u;
    vec4 v;
    vec4 radiance;
};

layout(std430, binding = 0) readonly buffer PrimitiveBuffer { Primitive primitives[]; };
layout(std430, binding = 1) readonly buffer MaterialBuffer { Material materials[]; };
layout(std430, binding = 2) readonly buffer LightBuffer { Light lights[]; };
layout(std430, binding = 3) readonly buffer NodeBoundsBuffer { vec4 node_bounds[]; };
layout(std430, binding = 4) readonly buffer NodeMetaBuffer { ivec4 node_meta[]; };
layout(std430, binding = 5) readonly buffer LeafIndexBuffer { int leaf_indices[]; };

uniform ivec2 u_resolution;
uniform uint u_sample;
uniform uint u_seed;
uniform int u_light_count;
uniform int u_node_count;
uniform int u_max_depth;
uniform vec3 u_eye;
uniform vec3 u_forward;
uniform vec3 u_right;
uniform vec3 u_vertical;
uniform float u_half_height;
uniform float u_aspect;

const float INF = 3.402823466e+38;
const float PI = 3.14159265358979323846;
const int MAT_DIFFUSE = 0;
const int MAT_CHECKER = 1;
const int MAT_MIRROR = 2;
const int MAT_DIELECTRIC = 3;
const int MAT_EMISSIVE = 4;
const int PRIM_SPHERE = 0;
const int PRIM_TRIANGLE = 1;
const int BVH_STACK = 64;
const int RAY_STACK = 64;

struct Hit {
    float t;
    int primitive_id;
    int material_id;
    vec3 point;
    vec3 outward;
    vec3 normal;
    bool front_face;
};

struct RayState {
    vec3 origin;
    vec3 direction;
    vec3 weight;
    int depth;
};

uint pcg(inout uint state) {
    uint old = state;
    state = old * 747796405u + 2891336453u;
    uint word = ((old >> ((old >> 28u) + 4u)) ^ old) * 277803737u;
    return (word >> 22u) ^ word;
}

float rand01(inout uint state) {
    return float(pcg(state) >> 8u) * (1.0 / 16777216.0);
}

float adaptive_epsilon(vec3 p) {
    float scale = max(1.0, max(abs(p.x), max(abs(p.y), abs(p.z))));
    return 2.0e-5 * scale;
}

vec3 spawn_origin(vec3 p, vec3 outward, vec3 direction) {
    float side = dot(direction, outward) >= 0.0 ? 1.0 : -1.0;
    return p + outward * (adaptive_epsilon(p) * side);
}

float bounds_entry(int node_index, vec3 ro, vec3 rd, float t_min, float t_max) {
    vec3 lo = node_bounds[node_index * 2].xyz;
    vec3 hi = node_bounds[node_index * 2 + 1].xyz;
    for (int axis = 0; axis < 3; ++axis) {
        float origin = ro[axis];
        float direction = rd[axis];
        if (abs(direction) < 1.0e-20) {
            if (origin < lo[axis] || origin > hi[axis]) return -1.0;
            continue;
        }
        float a = (lo[axis] - origin) / direction;
        float b = (hi[axis] - origin) / direction;
        if (a > b) {
            float tmp = a; a = b; b = tmp;
        }
        t_min = max(t_min, a);
        t_max = min(t_max, b);
        if (t_max < t_min) return -1.0;
    }
    return t_min;
}

float intersect_primitive(int primitive_id, vec3 ro, vec3 rd, float t_min, float t_max) {
    Primitive p = primitives[primitive_id];
    if (p.meta.x == PRIM_SPHERE) {
        vec3 oc = ro - p.a.xyz;
        float h = dot(oc, rd);
        float c = dot(oc, oc) - p.a.w * p.a.w;
        float disc = h * h - c;
        if (disc < 0.0) return -1.0;
        float s = sqrt(max(0.0, disc));
        float t = -h - s;
        if (t > t_min && t <= t_max) return t;
        t = -h + s;
        return (t > t_min && t <= t_max) ? t : -1.0;
    }
    vec3 e1 = p.b.xyz - p.a.xyz;
    vec3 e2 = p.c.xyz - p.a.xyz;
    vec3 q = cross(rd, e2);
    float det = dot(e1, q);
    if (abs(det) < 1.0e-8) return -1.0;
    float inv_det = 1.0 / det;
    vec3 s = ro - p.a.xyz;
    float u = dot(s, q) * inv_det;
    if (u < 0.0 || u > 1.0) return -1.0;
    vec3 r = cross(s, e1);
    float v = dot(rd, r) * inv_det;
    if (v < 0.0 || u + v > 1.0) return -1.0;
    float t = dot(e2, r) * inv_det;
    return (t > t_min && t <= t_max) ? t : -1.0;
}

bool nearest_hit(vec3 ro, vec3 rd, float t_min, float t_max, out Hit hit) {
    if (u_node_count <= 0) return false;
    float root_entry = bounds_entry(0, ro, rd, t_min, t_max);
    if (root_entry < 0.0) return false;
    int stack[BVH_STACK];
    float near_stack[BVH_STACK];
    int sp = 0;
    stack[sp] = 0;
    near_stack[sp] = root_entry;
    sp++;
    float closest = t_max;
    int winner = -1;

    while (sp > 0) {
        --sp;
        int node_index = stack[sp];
        float near_value = near_stack[sp];
        if (near_value > closest) continue;
        ivec4 meta = node_meta[node_index];
        if (meta.w > 0) {
            for (int i = 0; i < meta.w; ++i) {
                int primitive_id = leaf_indices[meta.z + i];
                float t = intersect_primitive(primitive_id, ro, rd, t_min, closest);
                if (t >= 0.0 && (winner < 0 || t < closest || (t == closest && primitive_id < winner))) {
                    closest = t;
                    winner = primitive_id;
                }
            }
        } else {
            float left_entry = bounds_entry(meta.x, ro, rd, t_min, closest);
            float right_entry = bounds_entry(meta.y, ro, rd, t_min, closest);
            if (left_entry >= 0.0 && right_entry >= 0.0) {
                int near_node = meta.x;
                int far_node = meta.y;
                float near_distance = left_entry;
                float far_distance = right_entry;
                if (right_entry < left_entry) {
                    near_node = meta.y; far_node = meta.x;
                    near_distance = right_entry; far_distance = left_entry;
                }
                if (sp + 2 <= BVH_STACK) {
                    stack[sp] = far_node; near_stack[sp] = far_distance; ++sp;
                    stack[sp] = near_node; near_stack[sp] = near_distance; ++sp;
                }
            } else if (left_entry >= 0.0 && sp < BVH_STACK) {
                stack[sp] = meta.x; near_stack[sp] = left_entry; ++sp;
            } else if (right_entry >= 0.0 && sp < BVH_STACK) {
                stack[sp] = meta.y; near_stack[sp] = right_entry; ++sp;
            }
        }
    }

    if (winner < 0) return false;
    Primitive p = primitives[winner];
    vec3 point = ro + rd * closest;
    vec3 outward;
    if (p.meta.x == PRIM_SPHERE) {
        outward = normalize(point - p.a.xyz);
        point = p.a.xyz + outward * p.a.w;
    } else {
        outward = normalize(cross(p.b.xyz - p.a.xyz, p.c.xyz - p.a.xyz));
    }
    bool front = dot(rd, outward) < 0.0;
    hit.t = closest;
    hit.primitive_id = winner;
    hit.material_id = p.meta.y;
    hit.point = point;
    hit.outward = outward;
    hit.normal = front ? outward : -outward;
    hit.front_face = front;
    return true;
}

vec3 background(vec3 direction) {
    float t = clamp(direction.y * 0.5 + 0.5, 0.0, 1.0);
    return mix(vec3(0.10, 0.14, 0.21), vec3(0.48, 0.62, 0.82), t);
}

int material_type(int material_id) {
    return int(round(materials[material_id].p0.w));
}

vec3 diffuse_albedo(int material_id, vec3 point) {
    Material m = materials[material_id];
    int type = material_type(material_id);
    if (type == MAT_CHECKER) {
        int cx = int(floor(point.x / m.p1.w));
        int cz = int(floor(point.z / m.p1.w));
        return (((cx + cz) & 1) == 0) ? m.p0.xyz : m.p1.xyz;
    }
    return m.p0.xyz;
}

void dielectric_interface(vec3 direction, vec3 normal, float eta_i, float eta_t,
                          out vec3 reflected, out vec3 refracted, out float fresnel,
                          out bool has_refracted) {
    reflected = reflect(direction, normal);
    if (eta_i == eta_t) {
        refracted = direction;
        fresnel = 0.0;
        has_refracted = true;
        return;
    }
    float cosine_i = clamp(-dot(direction, normal), 0.0, 1.0);
    float ratio = eta_i / eta_t;
    float sine_t_squared = ratio * ratio * max(0.0, 1.0 - cosine_i * cosine_i);
    if (sine_t_squared >= 1.0) {
        refracted = vec3(0.0);
        fresnel = 1.0;
        has_refracted = false;
        return;
    }
    float cosine_t = sqrt(max(0.0, 1.0 - sine_t_squared));
    refracted = normalize(direction * ratio + normal * (ratio * cosine_i - cosine_t));
    float r0 = (eta_i - eta_t) / (eta_i + eta_t);
    r0 *= r0;
    float cosine = eta_i > eta_t ? cosine_t : cosine_i;
    fresnel = r0 + (1.0 - r0) * pow(1.0 - cosine, 5.0);
    has_refracted = true;
}

vec3 visibility(vec3 ro, vec3 rd, float distance) {
    vec3 transmission = vec3(1.0);
    float remaining = max(0.0, distance - adaptive_epsilon(ro));
    for (int step = 0; step < 32; ++step) {
        Hit h;
        if (!nearest_hit(ro, rd, 0.0, remaining, h)) return transmission;
        int type = material_type(h.material_id);
        if (type != MAT_DIELECTRIC) return vec3(0.0);
        Material m = materials[h.material_id];
        float eta_i = h.front_face ? 1.0 : m.p2.x;
        float eta_t = h.front_face ? m.p2.x : 1.0;
        vec3 reflected, refracted;
        float fresnel;
        bool has_refracted;
        dielectric_interface(rd, h.normal, eta_i, eta_t,
                             reflected, refracted, fresnel, has_refracted);
        if (!has_refracted) return vec3(0.0);
        transmission *= (1.0 - fresnel);
        if (!h.front_face) transmission *= exp(-m.p0.xyz * h.t);
        vec3 advanced = spawn_origin(h.point, h.outward, rd);
        remaining -= h.t + length(advanced - h.point);
        ro = advanced;
        if (remaining <= 0.0) return transmission;
    }
    return vec3(0.0);
}

vec3 direct_lighting(Hit hit, int material_id, inout uint rng) {
    vec3 albedo = diffuse_albedo(material_id, hit.point);
    vec3 result = albedo * vec3(0.10, 0.13, 0.18) *
                  (0.55 + 0.45 * max(0.0, hit.normal.y));
    for (int i = 0; i < u_light_count; ++i) {
        Light light = lights[i];
        vec2 xi = u_sample == 0u ? vec2(0.5) : vec2(rand01(rng), rand01(rng));
        vec3 target = light.center.xyz + light.u.xyz * (2.0 * xi.x - 1.0)
                                      + light.v.xyz * (2.0 * xi.y - 1.0);
        vec3 delta = target - hit.point;
        float distance = length(delta);
        if (distance <= 0.0) continue;
        vec3 direction = delta / distance;
        vec3 cross_uv = cross(light.u.xyz, light.v.xyz);
        float cross_length = length(cross_uv);
        if (cross_length <= 0.0) continue;
        vec3 light_normal = cross_uv / cross_length;
        float cosine = max(0.0, dot(hit.normal, direction));
        float emitter_cosine = max(0.0, -dot(light_normal, direction));
        if (cosine <= 0.0 || emitter_cosine <= 0.0) continue;
        vec3 origin = spawn_origin(hit.point, hit.outward, direction);
        delta = target - origin;
        distance = length(delta);
        direction = delta / distance;
        vec3 transmitted = visibility(origin, direction, distance);
        float area = 4.0 * cross_length;
        float weight = cosine * emitter_cosine * area / (PI * distance * distance);
        result += albedo * light.radiance.xyz * transmitted * weight;
    }
    return result;
}

vec3 trace_scene(vec3 origin, vec3 direction, inout uint rng) {
    RayState stack[RAY_STACK];
    int sp = 0;
    stack[sp].origin = origin;
    stack[sp].direction = direction;
    stack[sp].weight = vec3(1.0);
    stack[sp].depth = u_max_depth;
    ++sp;
    vec3 color = vec3(0.0);

    while (sp > 0) {
        --sp;
        RayState state = stack[sp];
        Hit hit;
        if (!nearest_hit(state.origin, state.direction, 0.0, INF, hit)) {
            color += state.weight * background(state.direction);
            continue;
        }
        Material material = materials[hit.material_id];
        int type = material_type(hit.material_id);
        if (type == MAT_EMISSIVE) {
            if (hit.front_face) color += state.weight * material.p0.xyz;
            continue;
        }
        if (type == MAT_DIFFUSE || type == MAT_CHECKER) {
            color += state.weight * direct_lighting(hit, hit.material_id, rng);
            continue;
        }
        if (state.depth <= 0) continue;
        if (type == MAT_MIRROR) {
            if (sp < RAY_STACK) {
                vec3 next_direction = reflect(state.direction, hit.normal);
                stack[sp].origin = spawn_origin(hit.point, hit.outward, next_direction);
                stack[sp].direction = next_direction;
                stack[sp].weight = state.weight * material.p0.xyz;
                stack[sp].depth = state.depth - 1;
                ++sp;
            }
            continue;
        }
        if (type == MAT_DIELECTRIC) {
            float eta_i = hit.front_face ? 1.0 : material.p2.x;
            float eta_t = hit.front_face ? material.p2.x : 1.0;
            vec3 reflected, refracted;
            float fresnel;
            bool has_refracted;
            dielectric_interface(state.direction, hit.normal, eta_i, eta_t,
                                 reflected, refracted, fresnel, has_refracted);
            vec3 base_weight = state.weight;
            if (!hit.front_face) base_weight *= exp(-material.p0.xyz * hit.t);

            // Push refraction first so reflection is processed next. The fixed stack
            // is ample for the showcase's one closed dielectric and depth <= 16.
            if (has_refracted && fresnel < 1.0 && sp < RAY_STACK) {
                stack[sp].origin = spawn_origin(hit.point, hit.outward, refracted);
                stack[sp].direction = refracted;
                stack[sp].weight = base_weight * (1.0 - fresnel);
                stack[sp].depth = state.depth - 1;
                ++sp;
            }
            if (fresnel > 0.0 && sp < RAY_STACK) {
                stack[sp].origin = spawn_origin(hit.point, hit.outward, reflected);
                stack[sp].direction = reflected;
                stack[sp].weight = base_weight * fresnel;
                stack[sp].depth = state.depth - 1;
                ++sp;
            }
        }
    }
    return color;
}

void main() {
    ivec2 pixel = ivec2(gl_GlobalInvocationID.xy);
    if (any(greaterThanEqual(pixel, u_resolution))) return;

    uint pixel_id = uint(pixel.y * u_resolution.x + pixel.x);
    uint rng = u_seed ^ (pixel_id + 1u) * 0x9E3779B9u ^ (u_sample + 1u) * 0x85EBCA6Bu;
    vec2 jitter = u_sample == 0u ? vec2(0.5) : vec2(rand01(rng), rand01(rng));
    vec2 uv = (vec2(pixel) + jitter) / vec2(u_resolution);
    float horizontal = (2.0 * uv.x - 1.0) * u_aspect * u_half_height;
    float vertical = (2.0 * uv.y - 1.0) * u_half_height;
    vec3 direction = normalize(u_forward + u_right * horizontal + u_vertical * vertical);
    vec3 sample_color = trace_scene(u_eye, direction, rng);

    vec4 previous = u_sample == 0u ? vec4(0.0) : imageLoad(u_accum_image, pixel);
    imageStore(u_accum_image, pixel,
               vec4(previous.rgb + sample_color, float(u_sample + 1u)));
}
