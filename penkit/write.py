import xml.etree.ElementTree as ET
import numpy as np

# Landscape Letter
DEFAULT_PAGE_WIDTH = 11
DEFAULT_PAGE_HEIGHT = 8.5
DEFAULT_PAGE_UNIT = 'in'

DEFAULT_VIEW_BOX_MARGIN = 0.1
STROKE_THICKNESS = 0.003 # Fraction of width of image

PLOT_COLORS = ['black', 'red', 'green', 'blue', 'cyan', 'orange']

def calculate_view_box(layers, aspect_ratio, margin=DEFAULT_VIEW_BOX_MARGIN):
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


def layer_to_path_gen(layer):
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
    return ' '.join(layer_to_path_gen(layer))


def plot_to_svg(plot, width, height, unit=''):
    flipped_plot = [(x, -y) for x, y in plot]
    aspect_ratio = height / width
    view_box = calculate_view_box(flipped_plot, aspect_ratio=aspect_ratio)
    view_box_str = '{} {} {} {}'.format(*view_box)
    stroke_thickness = STROKE_THICKNESS * (view_box[2])

    svg = ET.Element('svg', attrib={
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

    return ET.tostring(svg, encoding='unicode')


def layer_to_svg(layer, **kwargs):
    return plot_to_svg([layer], **kwargs)


def write_plot(plot, filename, width=DEFAULT_PAGE_WIDTH, height=DEFAULT_PAGE_HEIGHT, unit=DEFAULT_PAGE_UNIT):
    svg = plot_to_svg(plot, width, height, unit)
    with open(filename, 'w') as outfile:
        outfile.write(svg)
