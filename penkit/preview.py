"""Functions for displaying plots inline inside a Jupyter notebook.

These functions are useful for iterative development of plots.
"""

from IPython.display import SVG

from penkit.write import plot_to_svg

PREVIEW_WIDTH = 330
PREVIEW_HEIGHT = 255


def show_layer(layer, *args, **kwargs):
    """Shortcut for ``show_plot`` when the plot has only one layer.

    Args:
        layer (layer): the layer to plot
        width (int): the width of the preview
        height (int): the height of the preview
    
    Returns:
        An object that renders in Jupyter as the provided plot
    """
    return show_plot([layer], *args, **kwargs)


def show_plot(plot, width=PREVIEW_WIDTH, height=PREVIEW_HEIGHT):
    """Preview a plot in a jupyter notebook.

    Args:
        plot (list): the plot to display (list of layers)
        width (int): the width of the preview
        height (int): the height of the preview
    
    Returns:
        An object that renders in Jupyter as the provided plot
    """
    return SVG(data=plot_to_svg(plot, width, height))
