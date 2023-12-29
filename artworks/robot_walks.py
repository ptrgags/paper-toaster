import random
import math

from postscriptlib import receipts, path
from postscriptlib.vec2 import Vec2

# Working with the fifth roots of unity
N = 5
TAU = 2.0 * math.pi
BASIS = [
    Vec2.direction_vec(TAU * i / N)
    for i in range(N)
]
DIRECTIONS = [
    BASIS[(i + 1) % N] - BASIS[i]
    for i in range(N)
]
PATH_LENGTH = 1

class RobotWalks(receipts.Receipt):
    ARTWORK_ID = "robot_walks"

    def generate_commands(self):
        """
        Randomly pick a string of L and R commands, always in multiples
        of 5 of each so the path will return to the start.
        """
        for _ in range(PATH_LENGTH):
            if random.random() < 0.5:
                self.commands += ["L"] * N
            else:
                self.commands += ["R"] * N
        random.shuffle(self.commands)
    
    def generate_path(self):
        """
        Iterate over the list of L and R commands
        and simulate the robot walking. Save the path into self.path
        """
        for command in self.commands:
            if command == 'L':
                self.position[self.left_index] += 1
                self.orientation += 1
                self.left_index = (self.left_index + 1) % N
                self.right_index = (self.right_index + 1) % N
            else:
                self.position[self.right_index] += 1
                self.orientation -= 1
                self.left_index = (self.left_index - 1) % N
                self.right_index = (self.right_index - 1) % N

            self.path.append(
                # Make a copy of the position vector because it will be
                # modified
                (self.position[:], self.orientation)
            )

    def setup(self):
        # Array of integers determining how many of each of the basis vectors
        # to add together to get the true position.
        self.position = [0, 0, 0, 0, 0]
        self.orientation = 0
        self.left_index = 0
        self.right_index = 4

        # A list of L or R commands describing how the robot turns
        self.commands = []
        
        # The path of states the robot goes through
        self.path = [(self.position[:], self.orientation)]

        self.generate_commands()
        print(self.commands)
        self.generate_path()
    
    @classmethod
    def compute_position(cls, position_vec):
        position = Vec2(0.0, 0.0)
        for i, count in enumerate(position_vec):
            position += count * DIRECTIONS[i]
        return position
    
    def draw(self):
        center = Vec2(self.width / 2, self.height / 2)

        vertices = []
        for (position_vec, _) in self.path:
            position = RobotWalks.compute_position(position_vec)
            ps_position = 3 * position + center
            print(position_vec, position, ps_position)
            vertices.append(ps_position)
        
        lines = path.Path()
        lines.polygon(vertices)
        self.add_path(lines)
        self.add_lines(["0.1 setlinewidth stroke"])

        dots = path.Path()
        for vertex in vertices:
            dots.circle(vertex, 0.2)
        self.add_path(dots)
