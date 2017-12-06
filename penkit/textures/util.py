import numpy as np

def rotate_texture(texture, angle, x_offset=0.5, y_offset=0.5):
    x, y = texture
    x -= x_offset
    y -= y_offset
    x_rot = x * np.cos(angle) + y * np.sin(angle)
    y_rot = x * -np.sin(angle) + y * np.cos(angle)
    return x_rot + x_offset, y_rot + y_offset


def fit_texture(texture):
    x, y = texture
    x = (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))
    y = (y - np.nanmin(y)) / (np.nanmax(y) - np.nanmin(y))
    return x, y