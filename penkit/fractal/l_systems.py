from math import pi, sin, cos
import numpy as np

from penkit.turtle import turtle_to_texture

RIGHT_ANGLE = 90
SIXTY_DEGREE_ANGLE = 60


def transform_sequence(sequence, transformations):
    """
    Applies a given set of substitution rules to the given string or generator.

    For more background see: https://en.wikipedia.org/wiki/L-system

    Params:
    - sequence: a string or generator onto which transformations are applied
    - transformations: a dictionary mapping each char to the string that is
        substituted for it when the rule is applied

    Returns: a generator of characters over the resulting string

    Examples:

    >>> ''.join(transform_sequence('ABC', {}))
    'ABC'
    >>> ''.join(transform_sequence('ABC', {'A': 'AC', 'C': 'D'}))
    'ACBD'
    """
    for c in sequence:
        for k in transformations.get(c, c):
            yield k


def transform_multiple(sequence, transformations, iterations):
    """
    Chains a transformation a given number of times.

    Params:
    - sequence: a string or generator onto which transformations are applied
    - transformations: a dictionary mapping each char to the string that is
        substituted for it when the rule is applied
    - iterations: how many times to repeat the transformation (positive int)

    Returns: a generator over the resulting string.
    """
    for _ in range(iterations):
        sequence = transform_sequence(sequence, transformations)
    return sequence


def l_system(axiom, transformations, iterations=1, angle=45, resolution=1):
    """
    Generates a texture by running transformations on a turtle program.

    First, the given transformations are applied to the axiom. This is
    repeated `iterations` times. Then, the output is run as a turtle
    program to get a texture, which is returned.

    For more background see: https://en.wikipedia.org/wiki/L-system

    Params:
    - axiom: the axiom of the Lindenmeyer system (a string)
    - transformations: a dictionary mapping each char to the string that is
        substituted for it when the rule is applied
    - iterations: the number of times to apply the transformations
    - angle: the angle to use for turns when interpreting the string
        as a turtle graphics program
    - resolution: the number of midpoints to create in each turtle step

    Returns: a texture
    """
    turtle_program = transform_multiple(axiom, transformations, iterations)
    return turtle_to_texture(turtle_program, angle, resolution=resolution)


def hilbert_curve(iterations=5, resolution=1):
    """
    Generates a Hilbert space-filling curve using an L-System.

    For more information see: https://en.wikipedia.org/wiki/Hilbert_curve

    Params:
    - iterations: the number of times to iterate the transformation
    - steps: the number of midpoints along each line

    Returns: a texture
    """
    return l_system('L', {
        'L': '-RF+LFL+FR-',
        'R': '+LF-RFR-FL+'
    }, iterations, RIGHT_ANGLE, resolution)


def flowsnake(iterations=5, resolution=1):
    """
    Generates a Peano-Gosper curve using an L-System.

    For more information see: https://en.wikipedia.org/wiki/Gosper_curve

    Params:
    - iterations: the number of times to iterate the transformation
    - steps: the number of midpoints along each line

    Returns: a texture
    """
    return l_system('A', {
        'A': 'A-B--B+A++AA+B-',
        'B': '+A-BB--B-A++A+B'
    }, iterations, SIXTY_DEGREE_ANGLE, resolution)
