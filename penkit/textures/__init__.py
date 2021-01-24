"""The ``textures`` module includes functions to generate textures.
"""

import numpy as np

from penkit.textures.util import fit_texture


def make_lines_texture(num_lines=10, resolution=50, keep_prob=None):
    """Makes a texture consisting of a given number of horizontal lines.

    Args:
        num_lines (int): the number of lines to draw
        resolution (int): the number of midpoints on each line
        keep_prob (None or float): if provided, should be a number between
            0 and 1. Lines will be randomly discarded with probability 1-keep_prob.

    Returns:
        A texture.
    """
    line_locations = np.linspace(0, 1, num_lines)

    if keep_prob is not None:
        mask = np.random.uniform(size=num_lines) > keep_prob
        line_locations = line_locations[mask]

    x, y = np.meshgrid(
        np.hstack([np.linspace(0, 1, resolution), np.nan]),
        line_locations,
    )
    
    y[np.isnan(x)] = np.nan
    return x.flatten(), y.flatten()


def make_grid_texture(num_h_lines=10, num_v_lines=10, resolution=50):
    """Makes a texture consisting of a grid of vertical and horizontal lines.

    Args:
        num_h_lines (int): the number of horizontal lines to draw
        num_v_lines (int): the number of vertical lines to draw
        resolution (int): the number of midpoints to draw on each line

    Returns:
        A texture.
    """
    x_h, y_h = make_lines_texture(num_h_lines, resolution)
    y_v, x_v = make_lines_texture(num_v_lines, resolution)
    return np.concatenate([x_h, x_v]), np.concatenate([y_h, y_v])

def make_plaid_texture(num_h_lines=10, num_v_lines=10, resolution=50, keep_prob=0.5):
    """Makes a texture consisting of a grid of plaid vertical and horizontal lines.

    Args:
        num_h_lines (int): the number of horizontal lines to draw
        num_v_lines (int): the number of vertical lines to draw
        resolution (int): the number of midpoints to draw on each line
        keep_prob (float): the probability a given line is kept

    Returns:
        A texture.
    """
    x_h, y_h = make_lines_texture(num_h_lines, resolution, keep_prob=keep_prob)
    y_v, x_v = make_lines_texture(num_v_lines, resolution, keep_prob=keep_prob)
    return np.concatenate([x_h, x_v]), np.concatenate([y_h, y_v])


def make_spiral_texture(spirals=6.0, ccw=False, offset=0.0, resolution=1000):
    """Makes a texture consisting of a spiral from the origin.

    Args:
        spirals (float): the number of rotations to make
        ccw (bool): make spirals counter-clockwise (default is clockwise)
        offset (float): if non-zero, spirals start offset by this amount
        resolution (int): number of midpoints along the spiral

    Returns:
        A texture.
    """
    dist = np.sqrt(np.linspace(0., 1., resolution))
    if ccw:
        direction = 1.
    else:
        direction = -1.
    angle = dist * spirals * np.pi * 2. * direction
    spiral_texture = (
        (np.cos(angle) * dist / 2.) + 0.5,
        (np.sin(angle) * dist / 2.) + 0.5
    )
    return spiral_texture


def make_hex_texture(grid_size = 2, resolution=1):
    """Makes a texture consisting on a grid of hexagons.

    Args:
        grid_size (int): the number of hexagons along each dimension of the grid
        resolution (int): the number of midpoints along the line of each hexagon
    
    Returns:
        A texture.
    """
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

def make_hex_texture2(grid_size=2, resolution=0):
    """An alternative implementation of make_hex_texture which draws every inner line twice.

    Args:
        grid_size (int): the number of hexagons along each dimension of the grid
        resolution (int): the number of midpoints along the line of each hexagon
    
    Returns:
        A texture.
    """
    grid = (np.array([]), np.array([]))

    hexagon = shapes.hexagon((0,0), resolution=resolution+2)

    hex_row_zero_origin = (
        np.concatenate([hexagon[0] + 3.0 * i for i in range(int(n/2))]),
        np.concatenate([hexagon[1] for i in range(int(n/2))])
    )

    for i in range(n):
        if i % 2 == 0:
            grid = (
                np.concatenate([grid[0], hex_row_zero_origin[0]]),
                np.concatenate([grid[1], hex_row_zero_origin[1] - np.sqrt(3)/2 * i])
            )
        else:
            grid = (
                np.concatenate([grid[0], hex_row_zero_origin[0] + 1.5 ]),
                np.concatenate([grid[1], hex_row_zero_origin[1] - np.sqrt(3)/2 * i])
            )

    return grid