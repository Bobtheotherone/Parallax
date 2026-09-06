#version 430 core

uniform sampler2D u_accum;
uniform float u_exposure;
in vec2 v_uv;
out vec4 out_color;

vec3 linear_to_srgb(vec3 x) {
    bvec3 low = lessThanEqual(x, vec3(0.0031308));
    vec3 a = 12.92 * x;
    vec3 b = 1.055 * pow(max(x, vec3(0.0)), vec3(1.0 / 2.4)) - 0.055;
    return mix(b, a, low);
}

void main() {
    vec4 sum = texture(u_accum, v_uv);
    float samples = max(1.0, sum.a);
    vec3 linear = max(vec3(0.0), sum.rgb / samples) * u_exposure;
    vec3 mapped = linear / (vec3(1.0) + linear);
    out_color = vec4(linear_to_srgb(mapped), 1.0);
}
