import numpy as np
from penkit import shapes
from penkit.write import write_plot
from penkit.textures.util import rotate_texture

def draw_recaman(n=50):
    """https://en.wikipedia.org/wiki/Recam%C3%A1n%27s_sequence"""

    plot = (np.array([0.]), np.array([0.]))
    current = 0
    visited = {0}
    flip = False
    for i in range(1, n):
        if current - i not in visited and current - i > 0:
            target = current - i  
        else:
            target = current + i
        center = ((current + target) / 2.0, 0.)
        radius = i

        if flip:
            start_angle = 0 if target < current else -np.pi
            end_angle = -np.pi if target < current else 0
        else:
            start_angle = 0 if target < current else np.pi
            end_angle = np.pi if target < current else 0

        visited.add(target)

        arc = shapes.arc(center, radius / 2.0, start_angle, end_angle)

        plot = (np.concatenate((plot[0],arc[0])), np.concatenate((plot[1], arc[1])))
        current = target
        flip = not flip
    return plot

write_plot([rotate_texture(draw_recaman(100), 90)], 'examples/recaman.svg', height=11.0, width=8.5)