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