
uniform sampler2D u_tex01;

struct Light{
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
};

varying vec4 v_normal;
varying vec4 v_s[4];
varying vec4 v_h[4];
varying vec2 v_uv;

uniform vec4 u_light_ambient;
uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform float u_material_shininess;

uniform float u_is_texture;
uniform sampler2D texture;

#define NR_OF_LIGHTS 4
uniform Light lights[NR_OF_LIGHTS];

vec4 calculateLighting(Light light, vec4 mat_diffuse, int i);

void main(void)
{
    vec4 mat_diffuse = u_material_diffuse;
    if(u_is_texture == 1.0)
    {
        mat_diffuse *= texture2D(u_tex01, v_uv);
    }
    
    // Go through each light in the scene
    vec4 results = vec4(0, 0, 0, 0);
    for(int i = 0; i < NR_OF_LIGHTS; i++){
        results += calculateLighting(lights[i], mat_diffuse, i);
    }

    gl_FragColor    = results;
}

vec4 calculateLighting(Light light, vec4 mat_diffuse, int i)
{
    // At this point v_normal and v_s are not normalized so we need to make sure that they are
    float lambert   = max(0.0, dot(v_normal, v_s[i]) / (length(v_normal) * length(v_s[i])));
    float phong     = max(0.0, dot(v_normal, v_h[i]) / (length(v_normal) * length(v_h[i])));
    
    vec4 ambient    = light.ambient * mat_diffuse;
    return          ambient + light.diffuse * mat_diffuse * lambert
                    + light.specular * u_material_specular * pow(phong, u_material_shininess);
}