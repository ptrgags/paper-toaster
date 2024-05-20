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

# The fifth roots of unity are useful here
N = 5
TAU = 2.0 * math.pi
TAU_DEGREES = 360
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

RADIUS = 0.25


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


R = RobotCommand.right()
L = RobotCommand.left()


def generate_commands(length):
    choices = [R, L]
    commands = []
    for _ in range(length):
        command = random.choice(choices)
        commands.append(command)
    return commands


SCALE = 0.1


class RobotWalks(receipts.Receipt):
    ARTWORK_ID = "robot_walks"

    def setup(self):
        # A list of L or R commands describing how the robot turns
        self.commands = generate_commands(10) * 5

        print([x.label for x in self.commands])

    def draw(self):
        vertices = [Vec2(0.0, 0.0)]
        centers = []
        arcs = []

        robot_path = RobotCommand.identity()
        for command in self.commands:
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
                centers.append(center)
                end_angle = robot_path.orientation * TAU_DEGREES / 5
                start_angle = prev_orientation * TAU_DEGREES / 5
                arcs.append((center, start_angle, end_angle, 'arc'))
            else:
                prev_orientation = (robot_path.orientation + 1) % N
                offset = OFFSETS[robot_path.orientation]
                right = -(offset.normalize().rot90())
                center = (
                    vertex +
                    0.5 * -offset +
                    0.5 * OFFSET_MAGNITUDE * 1.0 / math.tan(TAU / 10) * right
                )
                centers.append(center)

                end_angle = 180 - robot_path.orientation * TAU_DEGREES / 5
                start_angle = 180 - prev_orientation * TAU_DEGREES / 5
                # arcn is weird and measures angles clockwise
                arcs.append((center, -start_angle, -end_angle, 'arcn'))

        self.add_lines([
            f"{self.width / 2} {self.height / 2} translate",
            f'{SCALE * self.PPI} {SCALE * self.PPI} scale',
            "0.005 setlinewidth",
        ])

        # lines = path.Path()
        # lines.polygon(vertices)
        # self.add_path(lines)
        # self.add_lines(["0.005 setlinewidth stroke"])

        self.add_lines(["newpath"])
        for center, start, end, ps_command in arcs:
            print(center, start, end, ps_command)
            self.add_lines([
                f"{center.x} {center.y} 1 {start} {end} {ps_command}",
            ])
        self.add_lines(["stroke"])

        dots = path.Path()
        for vertex in vertices:
            dots.circle(vertex, 0.04)
        # for center in centers:
        #    dots.circle(center, 0.04)
        self.add_path(dots)
