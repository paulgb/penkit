import svgpathtools


def load_paths(filename):
    paths, _ = svgpathtools.svg2paths(filename)
    return paths
