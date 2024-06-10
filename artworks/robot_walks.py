import random
import math

'''
Robot walks like in Project Euler puzzle 208 Robot walks:
https://projecteuler.net/problem=208

This script doesn't solve the puzzle, just visualizes the paths since they
look cool.
'''

from postscriptlib import receipts, path
from postscriptlib.vec2 import Vec2

# We're only concerned with 1/5 turns
N = 5
TAU = 2.0 * math.pi
TAU_DEGREES = 360
FIFTH_TURN_DEGREES = TAU_DEGREES / N

# The fifth roots of unity are useful here
ROOTS = [
    Vec2.direction_vec(TAU * i / N)
    for i in range(N)
]

# If you take a straight line path instead of the circular arcs, the
# offsets are like drawing a unit pentagon
OFFSETS = [
    ROOTS[(i + 1) % N] - ROOTS[i]
    for i in range(N)
]

# All of the offsets are the same magnitude, which is not 1
OFFSET_MAGNITUDE = abs(OFFSETS[0])

PATH_LENGTH = 3

UNIT_LENGTH = 0.15
DOT_RADIUS = 0.1
LINE_WIDTH = 0.05


class RobotCommand:
    def __init__(self, offset_counts, orientation, label):
        # A list of five values indicating weights for the OFFSET vectors
        # to compute the displacement.
        self.offset_counts = offset_counts
        self.orientation = orientation
        self.label = label

    def __call__(self, other):
        offset_counts = other.offset_counts[:]
        for i, count in enumerate(self.offset_counts):
            offset_counts[(other.orientation + i) % N] += count
        orientation = (other.orientation + self.orientation) % 5
        label = other.label + self.label

        return RobotCommand(offset_counts, orientation, label)

    def __repr__(self):
        return f"{self.label}:{self.orientation}:{self.offset_counts}"

    @property
    def offset(self):
        result = Vec2(0.0, 0.0)
        for count, offset in zip(self.offset_counts, OFFSETS):
            result += count * offset
        return result

    @classmethod
    def identity(cls):
        return RobotCommand([0, 0, 0, 0, 0], 0, '')

    @classmethod
    def right(cls):
        return RobotCommand([0, 0, 0, 0, 1], 4, 'R')

    @classmethod
    def left(cls):
        return RobotCommand([1, 0, 0, 0, 0], 1, 'L')

    @classmethod
    def is_loop(cls, commands):
        current = cls.identity()
        for command in commands:
            current = command(current)

        identity = cls.identity()

        # The robot returns to the starting position if the counts of
        # all five offsets are equal. This is because the sum of all fifth
        # roots of unity is 0.
        returns_to_start = all(
            x == current.offset_counts[0] for x in current.offset_counts
        )

        return current.orientation == identity.orientation and returns_to_start


R = RobotCommand.right()
L = RobotCommand.left()


class RobotArc:
    """
    A simple struct for generating the PostScript arc or arcn commands
    for the robot arcs. These are always 1/5 turns
    """
    FIFTH_TURN = TAU_DEGREES / 5

    def __init__(self, center, start_angle, end_angle, clockwise):
        self.center = center

        if clockwise:
            # the arcn command is weird and measures angles clockwise
            self.start_angle = -(180 - start_angle * FIFTH_TURN_DEGREES)
            self.end_angle = -(180 - end_angle * FIFTH_TURN_DEGREES)
            self.arc_command = 'arcn'
        else:
            self.start_angle = start_angle * FIFTH_TURN_DEGREES
            self.end_angle = end_angle * FIFTH_TURN_DEGREES
            self.arc_command = 'arc'

    def __str__(self):
        """
        Generate the PostScript command
        """
        x = self.center.x
        y = self.center.y
        start = self.start_angle
        end = self.end_angle
        cmd = self.arc_command
        return f'{x} {y} 1 {start} {end} {cmd}'


def generate_commands(length):
    choices = [R, L]
    commands = []
    for _ in range(length):
        command = random.choice(choices)
        commands.append(command)

    # Repeat the commands 5 times. If the path loops back on itself, it
    # will do so after 5 times. The only other option is the path
    # goes off to infinity.
    return commands * 5


def generate_loop_commands(length):
    """
    Keep randomly generating loop commands until we find one.
    """
    attempts = 1
    while True:
        commands = generate_commands(length)
        if RobotCommand.is_loop(commands):
            print(f"Generating loop took {attempts} attempt(s)")
            return commands
        attempts += 1


def generate_geometry(commands):
    vertices = [Vec2(0.0, 0.0)]
    arcs = []

    robot_path = RobotCommand.identity()
    for command in commands:
        robot_path = command(robot_path)
        vertex = robot_path.offset
        vertices.append(vertex)

        if command.label == 'L':
            prev_orientation = (robot_path.orientation - 1) % N
            offset = OFFSETS[prev_orientation]
            left = offset.normalize().rot90()
            center = (
                vertex +
                0.5 * -offset +
                0.5 * OFFSET_MAGNITUDE * 1.0 / math.tan(TAU / 10) * left
            )

            arcs.append(RobotArc(
                center,
                prev_orientation,
                robot_path.orientation,
                False
            ))

        else:
            prev_orientation = (robot_path.orientation + 1) % N
            offset = OFFSETS[robot_path.orientation]
            right = -(offset.normalize().rot90())
            center = (
                vertex +
                0.5 * -offset +
                0.5 * OFFSET_MAGNITUDE * 1.0 / math.tan(TAU / 10) * right
            )

            arcs.append(RobotArc(
                center,
                prev_orientation,
                robot_path.orientation,
                True
            ))

    return (vertices, arcs)


class RobotWalks(receipts.Receipt):
    ARTWORK_ID = "robot_walks"

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            '-n',
            '--num-steps',
            type=int,
            default=10,
            help="Length of the robot's base path in steps. The path will be repeated 5 times to increase the chances of it looping nicely."
        )
        subparser.add_argument(
            '-l',
            '--loop',
            action='store_true',
            help="If set, the script will keep trying until it finds a path that loops."
        )

    def draw(self):
        if self.args.loop:
            commands = generate_loop_commands(self.args.num_steps)
        else:
            commands = generate_commands(self.args.num_steps)

        vertices, arcs = generate_geometry(commands)

        # The path is usually off-center. We can fix this with an
        # extra translate command.
        centroid = (1.0 / len(vertices)) * sum(vertices, start=Vec2(0.0, 0.0))

        # Outline the page before we adjust the coordinate system.
        self.outline_page()

        self.add_lines([
            f"{self.width / 2} {self.height / 2} translate",
            # Scale the coordinates to something more reasonable
            f'{UNIT_LENGTH * self.PPI} {UNIT_LENGTH * self.PPI} scale',
            f"{LINE_WIDTH} setlinewidth",

            # Center the drawing. This has to be done after the scaling
            # since the geometry assumes the arc radius is unit length.
            f'{-centroid.x} {-centroid.y} translate',
        ])

        self.add_lines(["newpath"])
        self.add_lines([str(arc) for arc in arcs])
        self.add_lines(["stroke"])

        dots = path.Path()
        for vertex in vertices:
            dots.circle(vertex, DOT_RADIUS)
        self.add_path(dots)
