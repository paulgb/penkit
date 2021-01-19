import numpy as np
from penkit import shapes
from penkit.preview import show_layer
from penkit.textures.util import concat, rotate_texture, translate, center
from penkit.write import write_plot

x_count = 18
y_count = 12
grid_spacing = 1.7
jitter = 0.9

l = ([], [])
for i in range(x_count * y_count):
    x, y = (i % x_count), (i // x_count)
    polygon = shapes.ngon(np.random.randint(3, 7))
    polygon = rotate_texture(polygon, np.random.uniform(0, 360))
    polygon = center(polygon)
    polygon = translate(polygon, (grid_spacing*x, grid_spacing*y))
    polygon = translate(polygon, (jitter * np.random.uniform(), jitter * np.random.uniform()))
    l = concat([l, polygon])

write_plot([l], 'examples/polygon_confetti.svg', height=8.5, width=11.0)