from IPython.display import HTML

from penkit.write import plot_to_svg

PREVIEW_WIDTH = 330
PREVIEW_HEIGHT = 255


def show_layer(layer):
    return show_plot([layer])


def show_plot(plot):
    return HTML(plot_to_svg(plot, PREVIEW_WIDTH, PREVIEW_HEIGHT))
