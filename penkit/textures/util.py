"""The ``textures.util`` module contains utility functions for working with textures.
"""

import numpy as np

def rotate_texture(texture, rotation, x_offset=0.5, y_offset=0.5):
    """Rotates the given texture by a given angle.

    Args:
        texture (texture): the texture to rotate
        rotation (float): the angle of rotation in degrees
        x_offset (float): the x component of the center of rotation (optional)
        y_offset (float): the y component of the center of rotation (optional)

    Returns:
        texture: A texture.
    """
    x, y = texture
    x = x.copy() - x_offset
    y = y.copy() - y_offset
    angle = np.radians(rotation)
    x_rot = x * np.cos(angle) + y * np.sin(angle)
    y_rot = x * -np.sin(angle) + y * np.cos(angle)
    return x_rot + x_offset, y_rot + y_offset


def fit_texture(layer):
    """Fits a layer into a texture by scaling each axis to (0, 1).

    Does not preserve aspect ratio (TODO: make this an option).

    Args:
        layer (layer): the layer to scale

    Returns:
        texture: A texture.
    """
    x, y = layer
    x = (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))
    y = (y - np.nanmin(y)) / (np.nanmax(y) - np.nanmin(y))
    return x, y