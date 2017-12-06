from scipy.ndimage.filters import gaussian_filter
import numpy as np

DEFAULT_DIMS = (500, 500)

def make_noise_surface(dims=DEFAULT_DIMS, blur=10, seed=None):
    if seed is not None:
        np.random.seed(seed)

    return gaussian_filter(np.random.normal(size=dims), blur)


def make_gradients(dims=DEFAULT_DIMS):
    return np.meshgrid(
        np.linspace(0.0, 1.0, dims[0]),
        np.linspace(0.0, 1.0, dims[1])
    )


def make_sine_surface(dims=DEFAULT_DIMS, offset=0.5, scale=1.0):
    gradients = (np.array(make_gradients(dims)) - offset) * scale * np.pi
    return np.sin(np.linalg.norm(gradients, axis=0))


def make_bubble_surface(dims=DEFAULT_DIMS, repeat=3):
    gradients = make_gradients(dims)
    return (
        np.sin((gradients[0] - 0.5) * repeat * np.pi) *
        np.sin((gradients[1] - 0.5) * repeat * np.pi))

