"""The ``surfaces`` module provides functions for generating **surfaces**.
Surfaces are 2D matrices which act as an elevation map.
"""

from scipy.ndimage.filters import gaussian_filter
import numpy as np

DEFAULT_DIMS = (500, 500)

def make_noise_surface(dims=DEFAULT_DIMS, blur=10, seed=None):
    """Makes a surface by generating random noise and blurring it.

    Args:
        dims (pair): the dimensions of the surface to create
        blur (float): the amount of Gaussian blur to apply
        seed (int): a random seed to use (optional)
    
    Returns:
        surface: A surface.
    """
    if seed is not None:
        np.random.seed(seed)

    return gaussian_filter(np.random.normal(size=dims), blur)


def make_gradients(dims=DEFAULT_DIMS):
    """Makes a pair of gradients to generate textures from numpy primitives.

    Args:
        dims (pair): the dimensions of the surface to create

    Returns:
        pair: A pair of surfaces.
    """
    return np.meshgrid(
        np.linspace(0.0, 1.0, dims[0]),
        np.linspace(0.0, 1.0, dims[1])
    )


def make_sine_surface(dims=DEFAULT_DIMS, offset=0.5, scale=1.0):
    """Makes a surface from the 3D sine function.

    Args:
        dims (pair): the dimensions of the surface to create
        offset (float): an offset applied to the function
        scale (float): a scale applied to the sine frequency

    Returns:
        surface: A surface.
    """
    gradients = (np.array(make_gradients(dims)) - offset) * scale * np.pi
    return np.sin(np.linalg.norm(gradients, axis=0))


def make_bubble_surface(dims=DEFAULT_DIMS, repeat=3):
    """Makes a surface from the product of sine functions on each axis.

    Args:
        dims (pair): the dimensions of the surface to create
        repeat (int): the frequency of the waves is set to ensure this many
            repetitions of the function
    
    Returns:
        surface: A surface.
    """
    gradients = make_gradients(dims)
    return (
        np.sin((gradients[0] - 0.5) * repeat * np.pi) *
        np.sin((gradients[1] - 0.5) * repeat * np.pi))

