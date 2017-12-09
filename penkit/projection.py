"""The ``projection`` module provides functions for rotating 2D objects
(surfaces and textures) in 3D space and projecting them back to 2D.
"""

import numpy as np

DEFAULT_ANGLE = 45


def map_texture_to_surface(texture, surface):
    """Returns values on a surface for points on a texture.

    Args:
        texture (texture): the texture to trace over the surface
        surface (surface): the surface to trace along

    Returns:
        an array of surface heights for each point in the
        texture. Line separators (i.e. values that are ``nan`` in
        the texture) will be ``nan`` in the output, so the output
        will have the same dimensions as the x/y axes in the
        input texture.
    """
    texture_x, texture_y = texture
    surface_h, surface_w = surface.shape

    surface_x = np.clip(
        np.int32(surface_w * texture_x - 1e-9), 0, surface_w - 1)
    surface_y = np.clip(
        np.int32(surface_h * texture_y - 1e-9), 0, surface_h - 1)

    surface_z = surface[surface_y, surface_x]
    return surface_z


def project_texture(texture_xy, texture_z, angle=DEFAULT_ANGLE):
    """Creates a texture by adding z-values to an existing texture and projecting.

    When working with surfaces there are two ways to accomplish the same thing:

    1. project the surface and map a texture to the projected surface
    2. map a texture to the surface, and then project the result

    The first method, which does not use this function, is preferred because
    it is easier to do occlusion removal that way. This function is provided
    for cases where you do not wish to generate a surface (and don't care about
    occlusion removal.)

    Args:
        texture_xy (texture): the texture to project
        texture_z (np.array): the Z-values to use in the projection
        angle (float): the angle to project at, in degrees (0 = overhead, 90 = side view)

    Returns:
        layer: A layer.
    """
    z_coef = np.sin(np.radians(angle))
    y_coef = np.cos(np.radians(angle))
    surface_x, surface_y = texture
    return (surface_x, -surface_y * y_coef + surface_z * z_coef)


def project_surface(surface, angle=DEFAULT_ANGLE):
    """Returns the height of the surface when projected at the given angle.

    Args:
        surface (surface): the surface to project
        angle (float): the angle at which to project the surface

    Returns:
        surface: A projected surface.
    """
    z_coef = np.sin(np.radians(angle))
    y_coef = np.cos(np.radians(angle))

    surface_height, surface_width = surface.shape
    slope = np.tile(np.linspace(0., 1., surface_height), [surface_width, 1]).T

    return slope * y_coef + surface * z_coef


def project_texture_on_surface(texture, surface, angle=DEFAULT_ANGLE):
    """Maps a texture onto a surface, then projects to 2D and returns a layer.

    Args:
        texture (texture): the texture to project
        surface (surface): the surface to project onto
        angle (float): the projection angle in degrees (0 = top-down, 90 = side view)

    Returns:
        layer: A layer.
    """
    projected_surface = project_surface(surface, angle)
    texture_x, _ = texture
    texture_y = map_texture_to_surface(texture, projected_surface)
    return texture_x, texture_y


def _make_occlusion_mask(projected_surface):
    """Generates a binary matrix representing the parts of a surface that
    are occluded. This assumes the surface is already projected with
    project_surface.

    Args:
        projected_surface (surface): the surface to use

    Returns:
        np.matrix: a binary matrix with the same dimensions as the input surface.
    """
    projected_surface_max = np.maximum.accumulate(projected_surface)
    return projected_surface == projected_surface_max


def _remove_hidden_parts(projected_surface):
    """Removes parts of a projected surface that are not visible.

    Args:
        projected_surface (surface): the surface to use

    Returns:
        surface: A projected surface.
    """
    surface = np.copy(projected_surface)
    surface[~_make_occlusion_mask(projected_surface)] = np.nan
    return surface


def project_and_occlude_texture(texture, surface, angle=DEFAULT_ANGLE):
    """Projects a texture onto a surface with occluded areas removed.

    Args:
        texture (texture): the texture to map to the projected surface
        surface (surface): the surface to project
        angle (float): the angle to project at, in degrees (0 = overhead, 90 = side view)

    Returns:
        layer: A layer.
    """
    projected_surface = project_surface(surface, angle)
    projected_surface = _remove_hidden_parts(projected_surface)
    texture_y = map_texture_to_surface(texture, projected_surface)
    texture_x, _ = texture
    return texture_x, texture_y
