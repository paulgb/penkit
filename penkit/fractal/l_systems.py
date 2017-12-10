"""The ``l_systems`` module contains an implementation of Lindemeyer systems.
"""

from math import pi, sin, cos
import numpy as np

from penkit.turtle import turtle_to_texture


def transform_sequence(sequence, transformations):
    """Applies a given set of substitution rules to the given string or generator.
    
    For more background see: https://en.wikipedia.org/wiki/L-system

    Args:
        sequence (str): a string or generator onto which transformations are applied
        transformations (dict): a dictionary mapping each char to the string that is
            substituted for it when the rule is applied

    Yields:
        str: the next character in the output sequence.

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
    """Chains a transformation a given number of times.

    Args:
        sequence (str): a string or generator onto which transformations are applied
        transformations (dict): a dictionary mapping each char to the string that is
            substituted for it when the rule is applied
        iterations (int): how many times to repeat the transformation

    Yields:
        str: the next character in the output sequence.
    """
    for _ in range(iterations):
        sequence = transform_sequence(sequence, transformations)
    return sequence


def l_system(axiom, transformations, iterations=1, angle=45, resolution=1):
    """Generates a texture by running transformations on a turtle program.

    First, the given transformations are applied to the axiom. This is
    repeated `iterations` times. Then, the output is run as a turtle
    program to get a texture, which is returned.

    For more background see: https://en.wikipedia.org/wiki/L-system

    Args:
        axiom (str): the axiom of the Lindenmeyer system (a string)
        transformations (dict): a dictionary mapping each char to the string that is
            substituted for it when the rule is applied
        iterations (int): the number of times to apply the transformations
        angle (float): the angle to use for turns when interpreting the string
            as a turtle graphics program
        resolution (int): the number of midpoints to create in each turtle step

    Returns:
        A texture
    """
    turtle_program = transform_multiple(axiom, transformations, iterations)
    return turtle_to_texture(turtle_program, angle, resolution=resolution)
