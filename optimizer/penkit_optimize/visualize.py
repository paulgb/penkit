import colorsys

import svgpathtools


def generate_color(hue, saturation=1.0, value=1.0):
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return 'rgb({},{},{})'.format(*[int(x * 255) for x in rgb])


def visualize_pen_transits(paths, svg_file):
    # We will construct a new image by storing (path, attribute)
    # pairs in this list.
    parts = list()

    last_end = None
    for i, path in enumerate(paths):
        start = path.start
        end = path.end

        # Generate a color based on how far along in the plot we are.
        frac = i / (len(paths) - 1)
        color = generate_color(frac, 1.0, 1.0)

        if last_end is not None:
            # If this isn't our first path, add a line between the end of
            # the last path and the start of this one.
            parts.append((
                svgpathtools.Line(last_end, start),
                {
                    'stroke': 'black',
                    'fill': 'none',
                }
            ))

        last_end = end

        # Also draw a faded, colorized version of this path.
        parts.append((
            path,
            {
                'stroke': color,
                'fill': 'none',
                'opacity': '0.5'
            }
        ))

    new_paths, new_attrs = zip(*parts)
    svgpathtools.wsvg(new_paths, attributes=new_attrs, filename=svg_file)
