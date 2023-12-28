import math

from postscriptlib.rectangle import Rectangle
from postscriptlib.vec2 import Vec2
from postscriptlib.mathutils import remap
from postscriptlib.path import Path

class PSTurtle:
    """
    Turtle graphics but for PostScript output, unlike Python's built in
    Turtle module.
    """
    def __init__(self, angle_divisions):
        # The heading is tracked as an integer modulo angle_divisions
        self.heading = 0
        self.angle_divisions = angle_divisions
        self.turn_angle = 2.0 * math.pi / self.angle_divisions

        self.bounds = Rectangle(0, 0, 0, 0)
        self.position = Vec2(0, 0)
        self.positions = [self.position]
        self.turn_count = 0
    
    @property
    def direction_vec(self):
        return Vec2.direction_vec(self.turn_angle * self.heading)
    
    def forward(self, distance):
        """
        Move forward in the current direction at the given distance
        """
        next_pos = self.position + distance * self.direction_vec
        self.position = next_pos
        self.positions.append(next_pos)
        self.bounds.add_point(next_pos)
    
    def turn(self, delta_heading):
        """
        Turn 
        """
        self.turn_count += 1
        self.heading += delta_heading
        self.heading %= self.angle_divisions

    @property
    def is_finished(self):
        """
        Check if we're close to the origin and facing to the right
        """
        origin = Vec2(0, 0)
        return self.heading == 0 and abs(self.position - origin) < 0.001

    def make_path(self, drawing_bounds):
        """
        Make a path, with positions shifted/scaled to drawing_bounds.

        drawing_bounds should be a square, else the output may look
        stretched
        """
        in_min = self.bounds.min
        in_max = self.bounds.max
        out_min = drawing_bounds.min
        out_max = drawing_bounds.max

        scaled_positions = [
            remap(in_min, in_max, out_min, out_max, v)
            for v in self.positions
        ]

        path = Path()
        path.polygon(scaled_positions)
        return path