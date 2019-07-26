import svgpathtools

import numpy as np

def segment_svg(svg_file, output_file, segment_size=8)
    paths, _ = svgpathtools.svg2paths('./nyc.svg')

    lines = []

    for path in paths:
        for cp in path.continuous_subpaths():
            last_pos = None
            segments = int(cp.length() / segment_size)
            for frac in np.linspace(0., 1., segments):
                pos = cp.point(frac)
                if last_pos:
                    lines.append(svgpathtools.Line(last_pos, pos))
                last_pos = pos

    svgpathtools.wsvg(lines, filename=output_file)
