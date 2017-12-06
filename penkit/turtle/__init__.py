import numpy as np

DEGREES_TO_RADIANS = np.pi / 180.
DEFAULT_TURN = 45.
DEFAULT_INITIAL_ANGLE = 90.

FORWARD_COMMANDS = set('abcdefghijABCDEFGHIJ')
VISIBLE_COMMANDS = set('ABCDEFGHIJ')

def branching_turtle_generator(turtle_program, turn_amount=DEFAULT_TURN, initial_angle=DEFAULT_INITIAL_ANGLE):
    saved_states = list()
    state = (0, 0, DEFAULT_INITIAL_ANGLE)
    yield (0, 0)

    for command in turtle_program:
        x, y, angle = state

        if command in FORWARD_COMMANDS:            # Move forward (matches a-j and A-J)
            state = (x - np.cos(angle * DEGREES_TO_RADIANS),
                     y + np.sin(angle * DEGREES_TO_RADIANS),
                     angle)
            
            if command not in VISIBLE_COMMANDS:    # Add a break in the line if command matches a-j
                yield (np.nan, np.nan)

            yield (state[0], state[1])

        elif command == '+':                       # Turn +turn_amount
            state = (x, y, angle + turn_amount)

        elif command == '-':                       # Turn -turn_amount
            state = (x, y, angle - turn_amount)

        elif command == '[':                       # Push current state
            saved_states.append(state)

        elif command == ']':                       # Pop previous state
            state = saved_states.pop()
            yield (np.nan, np.nan)
            x, y, _ = state
            yield (x, y)

        # Note: We silently ignore unknown commands


def texture_from_generator(generator):
    return np.array(list(zip(*list(generator))))


def turtle_to_texture(turtle_program, turn_amount = DEFAULT_TURN, initial_angle=DEFAULT_INITIAL_ANGLE):
    generator = branching_turtle_generator(turtle_program, turn_amount, initial_angle)
    return texture_from_generator(generator)

