
attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_eye_position;
uniform vec4 u_light_position[4];

varying vec4 v_normal;
varying vec4 v_s[4];
varying vec4 v_h[4];
varying vec2 v_uv;

void main(void)
{
    vec4 position   = vec4(a_position.x, a_position.y, a_position.z, 1.0);
    vec4 normal     = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

    // UV coords sent into per-pixel use
    v_uv = a_uv;

    position        = u_model_matrix * position;
    v_normal        = u_model_matrix * normal;

    for(int i = 0; i < 4; i++) {

        v_s[i]             = u_light_position[i] - position;
        vec4 v             = u_eye_position - position;
        v_h[i]             = v + v_s[i];
    }

    position        = u_view_matrix * position;
    position        = u_projection_matrix * position;

    gl_Position     = position;

}
