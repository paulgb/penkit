import numpy as np

DEFAULT_SLOPE = 10

def map_texture_to_surface(texture, surface):
    texture_x, texture_y = texture
    surface_w, surface_h = surface.shape
    
    surface_x = np.clip(np.int32(surface_w * texture_x - 1e-9), 0, surface_w - 1)
    surface_y = np.clip(np.int32(surface_h * texture_y - 1e-9), 0, surface_h - 1)

    surface_z = surface[surface_x, surface_y]
    return surface_z


def project_texture(texture, surface, slope=DEFAULT_SLOPE):
    surface_z = map_texture_to_surface(texture, surface.T)
    surface_x, surface_y = texture
    return (surface_x, -surface_y * slope + surface_z)


def make_shadow_mask(surface, slope=DEFAULT_SLOPE):
    s = surface.shape[0]
    projected_surface = np.flipud(surface) * s + slope * np.expand_dims(np.arange(s), axis=1)
    projected_surface_max = np.maximum.accumulate(projected_surface)
    return np.flipud(projected_surface == projected_surface_max)


def remove_hidden_parts(surface, slope=DEFAULT_SLOPE):
    surface = np.copy(surface)
    surface[~make_shadow_mask(surface, slope)] = np.nan
    return surface


def project_and_occlude_texture(texture, surface, slope=DEFAULT_SLOPE):
    surface_occluded = remove_hidden_parts(surface, slope)
    result = project_texture(texture, surface_occluded)
    return result
