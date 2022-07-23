import math

from postscriptlib import receipts, path
from postscriptlib.vec2 import Vec2
COS_60 = math.cos(math.pi / 3)
SIN_60 = math.sin(math.pi / 3)
UNIT_BASIS = [
    Vec2(1.0, 0.0),
    Vec2(COS_60, SIN_60),
    Vec2(-COS_60, SIN_60),
    Vec2(-1.0, 0.0),
    Vec2(-COS_60, -SIN_60),
    Vec2(COS_60, -SIN_60)
]

X_START = -7
X_END = 4
Y_START = 0
Y_END = 11

class HexGrid(receipts.Receipt):
    ARTWORK_ID = 'hex_grid'

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            '-s',
            '--side-length',
            type=float,
            default=0.25,
            help='Length of the sides of each hexaon in inches'
        )
        subparser.add_argument(
            '-e',
            '--expand-factor',
            type=float,
            default=1.0,
            help='Factor for expanding the grid for artistic effect (e.g. try 1.2)'
        )
        subparser.add_argument(
            '-d',
            '--dots',
            action='store_true',
            help='Draw the vertices of the hexagons as dots instead of lines'
        )

    def setup(self):
        self.side_length = self.args.side_length * self.PPI
        self.expand_factor = self.args.expand_factor
        
        # create the 6 vectors for the 6 sides of the polygon
        self.basis = [self.side_length * v for v in UNIT_BASIS]

        # translations between each grid cell
        self.t1 = self.basis[0] + self.basis[5]
        self.t2 = self.basis[0] + self.basis[1]

        # The grid vectors aren't aligned with the 
        # receipt so have to expand the grid quite a bit :/
        self.x_start = self.num_cards * X_START
        self.x_end = X_END
        self.y_start = Y_START
        self.y_end = self.num_cards * Y_END
    
    def draw_hexagon(self, corner):
        hex = path.Path()
        hex.rpolygon(corner, self.basis)
        self.add_path(hex)
        self.stroke()

    def draw_hexagons(self):
        for i in range(self.x_start, self.x_end):
            for j in range(self.y_start, self.y_end):
                corner = i * self.t1 + j * self.t2
                corner = self.expand_factor * corner
                self.draw_hexagon(corner)
    
    def draw_hexagon_vertices(self, start):
        hex = path.Path()
        vertex = start
        DOT_RADIUS = 2
        for v in self.basis:
            hex.circle(vertex, DOT_RADIUS)
            vertex += v
        self.add_path(hex)
        self.fill()
    
    def draw_hexagons_dots(self):
        for i in range(self.x_start, self.x_end):
            for j in range(self.y_start, self.y_end):
                start = i * self.t1 + j * self.t2
                start = self.expand_factor * start
                self.draw_hexagon_vertices(start)

    def draw(self):
        if self.args.dots:
            self.draw_hexagons_dots()
        else:
            self.draw_hexagons()

        border = path.Path()
        border.rect(0, 0, self.width, self.height)
        self.add_path(border)
        self.stroke()