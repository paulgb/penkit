from penkit.fractal.l_systems import l_system

RIGHT_ANGLE = 90
SIXTY_DEGREE_ANGLE = 60


def hilbert_curve(iterations=5, resolution=1):
    """Generates a Hilbert space-filling curve using an L-System.

    For more information see: https://en.wikipedia.org/wiki/Hilbert_curve

    Args:
        iterations (int): the number of times to iterate the transformation
        resolution (int): the number of midpoints along each line

    Returns:
        A texture
    """
    return l_system('L', {
        'L': '-RF+LFL+FR-',
        'R': '+LF-RFR-FL+'
    }, iterations, RIGHT_ANGLE, resolution)


def flowsnake(iterations=4, resolution=1):
    """Generates a Peano-Gosper curve using an L-System.

    For more information see: https://en.wikipedia.org/wiki/Gosper_curve

    Args:
        iterations (int): the number of times to iterate the transformation
        resolution (int): the number of midpoints along each line

    Returns:
        A texture
    """
    return l_system('A', {
        'A': 'A-B--B+A++AA+B-',
        'B': '+A-BB--B-A++A+B'
    }, iterations, SIXTY_DEGREE_ANGLE, resolution)


def tree(iterations=4, resolution=1, angle=22.5):
    """Generates an organic-looking tree.

    Args:
        iterations (int): the number of times to iterate the transformation
        resolution (int): the number of midpoints along each line
        angle (float): the angle of branching

    Returns:
        A texture
    """
    return l_system('A', {
        'F': 'FF',
        'A': 'F[+AF-[A]--A][---A]'
    }, iterations, angle, resolution)


def dragon_curve(iterations=4, resolution=1):
    """Generates an dragon curve using an L-System.

    For more information see: https://en.wikipedia.org/wiki/Dragon_curve

    Args:
        iterations (int): the number of times to iterate the transformation
        resolution (int): the number of midpoints along each line

    Returns:
        A texture
    """
    return l_system('FX', {
        'X': 'X+YF+',
        'Y': '-FX-Y'
        }, iterations, RIGHT_ANGLE, resolution)
