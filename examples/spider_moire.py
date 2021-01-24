import numpy as np
from penkit import shapes
from penkit.textures.util import concat, crop
from penkit.write import write_plot

l = ([], [])

for i in range(130):
    arc = shapes.circle((0,0), i, 300)
    arc = crop(arc, -30, -20, 70, 80)

    arc2 = shapes.circle((1.5,2.3), i*1.05, 300)
    arc2 = crop(arc2, -30, -20, 70, 80)
    l = concat([l, arc, ([np.nan], [np.nan]), arc2, ([np.nan], [np.nan])])

write_plot([l], 'examples/spider_moire.svg', height=8.5, width=8.5, stroke_thickness_pct=0.0015)