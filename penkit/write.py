import xml.etree.ElementTree as ET
import numpy as np

# Landscape Letter
DEFAULT_PAGE_WIDTH = 11
DEFAULT_PAGE_HEIGHT = 8.5
DEFAULT_PAGE_UNIT = 'in'
STROKE_THICKNESS_PCT = 0.003

# Plot-related defaults
DEFAULT_VIEW_BOX_MARGIN = 0.1
PLOT_COLORS = ['black', 'red', 'green', 'blue', 'cyan', 'orange']


def calculate_view_box(layers, aspect_ratio, margin=DEFAULT_VIEW_BOX_MARGIN):
    """Calculates the size of the SVG viewBox to use.

    Args:
        layers (list): the layers in the image
        aspect_ratio (float): the height of the output divided by the width
        margin (float): minimum amount of buffer to add around the image, relative
            to the total dimensions

    Returns:
        tuple: a 4-tuple of floats representing the viewBox according to SVG
            specifications ``(x, y, width, height)``.
    """
    min_x = min(np.nanmin(x) for x, y in layers)
    max_x = max(np.nanmax(x) for x, y in layers)
    min_y = min(np.nanmin(y) for x, y in layers)
    max_y = max(np.nanmax(y) for x, y in layers)
    height = max_y - min_y
    width = max_x - min_x

    if height > width * aspect_ratio:
        adj_height = height * (1. + margin)
        adj_width = adj_height / aspect_ratio
    else:
        adj_width = width * (1. + margin)
        adj_height = adj_width * aspect_ratio

    width_buffer = (adj_width - width) / 2.
    height_buffer = (adj_height - height) / 2.

    return (
        min_x - width_buffer,
        min_y - height_buffer,
        adj_width,
        adj_height
    )


def _layer_to_path_gen(layer):
    """Generates an SVG path from a given layer.

    Args:
        layer (layer): the layer to convert

    Yields:
        str: the next component of the path
    """
    draw = False
    for x, y in zip(*layer):
        if np.isnan(x) or np.isnan(y):
            draw = False
        elif not draw:
            yield 'M {} {}'.format(x, y)
            draw = True
        else:
            yield 'L {} {}'.format(x, y)


def layer_to_path(layer):
    """Generates an SVG path from a given layer.

    Args:
        layer (layer): the layer to convert

    Returns:
        str: an SVG path
    """
    return ' '.join(_layer_to_path_gen(layer))


def plot_to_svg(plot, width, height, unit='', stroke_thickness_pct=STROKE_THICKNESS_PCT):
    """Converts a plot (list of layers) into an SVG document.

    Args:
        plot (list): list of layers that make up the plot
        width (float): the width of the resulting image
        height (float): the height of the resulting image
        unit (str): the units of the resulting image if not pixels

    Returns:
        str: A stringified XML document representing the image
    """
    flipped_plot = [(x, -y) for x, y in plot]
    aspect_ratio = height / width
    view_box = calculate_view_box(flipped_plot, aspect_ratio=aspect_ratio)
    view_box_str = '{} {} {} {}'.format(*view_box)
    stroke_thickness = stroke_thickness_pct * (view_box[2])

    svg = ET.Element('svg', attrib={
        'xmlns': 'http://www.w3.org/2000/svg',
        'xmlns:inkscape': 'http://www.inkscape.org/namespaces/inkscape',
        'width': '{}{}'.format(width, unit),
        'height': '{}{}'.format(height, unit),
        'viewBox': view_box_str})

    for i, layer in enumerate(flipped_plot):
        group = ET.SubElement(svg, 'g', attrib={
            'inkscape:label': '{}-layer'.format(i),
            'inkscape:groupmode': 'layer',
        })

        color = PLOT_COLORS[i % len(PLOT_COLORS)]
        ET.SubElement(group, 'path', attrib={
            'style': 'stroke-width: {}; stroke: {};'.format(stroke_thickness, color),
            'fill': 'none',
            'd': layer_to_path(layer)
        })

    try:
        return ET.tostring(svg, encoding='unicode')
    except LookupError:
        # Python 2.x
        return ET.tostring(svg)


def layer_to_svg(layer, **kwargs):
    """Converts a layer into an SVG image.

    Wrapper around ``plot_to_svg``.

    Args:
        layer (layer): the layer to plot
        width (float): the width of the resulting image
        height (float): the height of the resulting image
        unit (str): the units of the resulting image if not pixels

    Returns:
        str: A stringified XML document representing the image
    """
    return plot_to_svg([layer], **kwargs)


def write_plot(plot, filename, width=DEFAULT_PAGE_WIDTH, height=DEFAULT_PAGE_HEIGHT, 
    unit=DEFAULT_PAGE_UNIT, stroke_thickness_pct=STROKE_THICKNESS_PCT):
    """Writes a plot SVG to a file.

    Args:
        plot (list): a list of layers to plot
        filename (str): the name of the file to write
        width (float): the width of the output SVG
        height (float): the height of the output SVG
        unit (str): the unit of the height and width
    """
    svg = plot_to_svg(plot, width, height, unit, stroke_thickness_pct=stroke_thickness_pct)
    with open(filename, 'w') as outfile:
        outfile.write(svg)
