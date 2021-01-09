from penkit.write import write_plot
from penkit.fractal import dragon_curve

curve = dragon_curve(12)
write_plot([curve], 'examples/dragon_curve.svg')

