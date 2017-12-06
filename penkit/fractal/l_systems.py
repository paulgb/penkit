from math import pi, sin, cos
import numpy as np

from penkit.turtle import turtle_to_texture

RIGHT_ANGLE = 90

def transform_sequence(sequence, transformations):
    return ''.join(transformations.get(c, c) for c in sequence)


def transform_multiple(sequence, transformations, iterations):
    for _ in range(iterations):
        sequence = transform_sequence(sequence, transformations)
    return sequence


def l_system(axiom, transformations, iterations=0, angle=45):
    turtle_program = transform_multiple(axiom, transformations, iterations)
    return turtle_to_texture(turtle_program, angle)


def hilbert_curve(iterations=5):
    return l_system('L', {
        'L': '-RF+LFL+FR-',
        'R': '+LF-RFR-FL+'
    }, iterations, RIGHT_ANGLE)
