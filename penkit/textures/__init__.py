import numpy as np

from penkit.textures.util import fit_texture


def make_lines_texture(num_lines=10, resolution=50):
    x, y = np.meshgrid(
        np.hstack([np.linspace(0, 1, resolution), np.nan]),
        np.linspace(0, 1, num_lines),
    )
    
    y[np.isnan(x)] = np.nan
    return x.flatten(), y.flatten()


def make_grid_texture(num_h_lines=10, num_v_lines=10, resolution=50):
    x_h, y_h = make_lines_texture(num_h_lines, resolution)
    y_v, x_v = make_lines_texture(num_v_lines, resolution)
    return np.concatenate([x_h, x_v]), np.concatenate([y_h, y_v])


def make_spiral_texture(resolution=1000, offset=0.0, spirals=6.0):
    dist = np.sqrt(np.linspace(0., 1., resolution))
    angle = dist * spirals * np.pi * 2.
    spiral_texture = (
        (np.cos(angle) * dist / 2.) + 0.5,
        (np.sin(angle) * dist / 2.) + 0.5
    )
    return spiral_texture


def make_hex_texture(grid_size = 2, resolution=1):
    grid_x, grid_y = np.meshgrid(
        np.arange(grid_size),
        np.arange(grid_size)
    )
    ROOT_3_OVER_2 = np.sqrt(3) / 2
    ONE_HALF = 0.5
    
    grid_x = (grid_x * np.sqrt(3) + (grid_y % 2) * ROOT_3_OVER_2).flatten()
    grid_y = grid_y.flatten() * 1.5
    
    grid_points = grid_x.shape[0]
    
    x_offsets = np.interp(np.arange(4 * resolution),
        np.arange(4) * resolution, [
            ROOT_3_OVER_2,
            0.,
            -ROOT_3_OVER_2,
            -ROOT_3_OVER_2,
        ])
    y_offsets = np.interp(np.arange(4 * resolution),
        np.arange(4) * resolution, [
            -ONE_HALF,
            -1.,
            -ONE_HALF,
            ONE_HALF
        ])
    
    tmx = 4 * resolution
    x_t = np.tile(grid_x, (tmx, 1)) + x_offsets.reshape((tmx, 1))
    y_t = np.tile(grid_y, (tmx, 1)) + y_offsets.reshape((tmx, 1))
    
    x_t = np.vstack([x_t, np.tile(np.nan, (1, grid_x.size))])
    y_t = np.vstack([y_t, np.tile(np.nan, (1, grid_y.size))])
    
    return fit_texture((x_t.flatten('F'), y_t.flatten('F')))