import numpy as np

def arc(center, radius, start_angle, end_angle, resolution=100):
    """Draws an arc

    Args:
        center (pair): the center of the circle inferred by the arc
        radius (float): the radius of the circle inferred by the arc
        start_angle (float): the starting angle position of the arc
        end_angle (float): the ending angle position of the arc
    
    Returns:
        layer: A layer.
    """
    linspace = np.linspace(0., 1., resolution)
    angles = start_angle + (end_angle - start_angle) * linspace
    return (
        (np.cos(angles) * radius) + center[0],
        (np.sin(angles) * radius) + center[1],
    )

def circle(center, radius, resolution=100):
    return arc(center, radius, 0, 2*np.pi, resolution)

def line(origin, end=None, vector=None, length=None, angle=None, resolution=2):
    """Draws a line. One of these must be specified: end, vector, or (length, angle)

    Args:
        origin (pair): the origin of the line
        end (pair): optional. the coordinates of end of the line
        vector (pair): optional. the x and y lengths of the line
        length (float): optional. the length of the line
        angle (float): optional. the angle of the line
    
    Returns:
        layer: A layer.
    """

    if end is not None:
        return (
            np.linspace(origin[0], end[0], resolution), 
            np.linspace(origin[1], end[1], resolution)
        )

    if vector is not None:
        return (
            np.linspace(origin[0], origin[0] + vector[0], resolution), 
            np.linspace(origin[1], origin[1] + vector[1], resolution)
        )

    if length is not None and angle is not None:
        return (
            np.linspace(origin[0], origin[0] + length * np.cos(angle), resolution), 
            np.linspace(origin[1], origin[1] + length * np.sin(angle), resolution)
        )

def hexagon(center, diameter=1.0, resolution=2):
    return ngon(6, center, diameter, resolution)

def ngon(n, origin=(0,0), diameter=1.0, resolution=2):
    segment_length = 2 * np.sin(np.pi / n)
    ngon_inner_angle = np.pi * (n - 2) / n
    ngon_outer_angle = np.pi - ngon_inner_angle

    segments = []
    for i in range(n):
        if i == 0:
            from_pt = origin
        else:
            last_segment = segments[-1]
            from_pt = (last_segment[0][-1], last_segment[1][-1])

        segment = line(from_pt, length=segment_length, angle=i*ngon_outer_angle, resolution=resolution)
        segments.append(segment)

    segments.append(([np.nan], [np.nan]))
    
    ngon_layer = (
        np.concatenate([s[0] for s in segments]),
        np.concatenate([s[1] for s in segments])
    )

    return ngon_layer

