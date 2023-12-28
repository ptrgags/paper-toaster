import random

from postscriptlib import receipts

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

IN = 0
OUT = 1
EDGE = 2

# sink: open circle in the middle connected to all 4 edges
# source: closed circle in the middle connected to all 4 edges
# truchet: circular arcs connecting adjacent edges. In the default position,
#   the bottom and right edges are connected
# cross: a braid-like crossing. Unrotated, the over strand goes from left to
#   right. Note that the rotation is determined by the diagonal number rather
#   than the in/out directions for better weaving.
# fork3: from the bottom of the cell, draw arcs to the left and right, and a
#  line to the top of the cell

TILE_CHOICES = {
    # (right, up, left, down) -> set((tile_type, rotation))
    # where rotation is the number of 90 degree CCW rotations to apply
    (IN, IN, IN, IN): {("sink4", 0)},
    (IN, IN, IN, OUT): {("fork3", 0)},
    (IN, IN, OUT, IN): {("fork3", 3)},
    (IN, IN, OUT, OUT): {("truchet", 0), ("cross", 0)},
    (IN, OUT, IN, IN): {("fork3", 2)},
    (IN, OUT, IN, OUT): {("truchet", 0), ("truchet", 1)},
    (IN, OUT, OUT, IN): {("truchet", 1), ("cross", 0)},
    (IN, OUT, OUT, OUT): {("fork3", 1)},
    (OUT, IN, IN, IN): {("fork3", 1)},
    (OUT, IN, IN, OUT): {("truchet", 1), ("cross", 0)},
    (OUT, IN, OUT, IN): {("truchet", 0), ("truchet", 1)},
    (OUT, IN, OUT, OUT): {("fork3", 2)},
    (OUT, OUT, IN, IN): {("truchet", 0), ("cross", 0)},
    (OUT, OUT, IN, OUT): {("fork3", 3)},
    (OUT, OUT, OUT, IN): {("fork3", 0)},
    (OUT, OUT, OUT, OUT): {("source4", 0)},
}

# For edges, there are quite a few cases. To keep it simple, let's rotate
# the first edge so it's at the bottom. If there are 2 edges (corner), assume
# the second edge is on the right.
#
# In all 12 cases, there is only one choice, and the rotation is handled
# when rotating the boundary to the bottom of the tile, so this dictionary
# is simpler in a way
EDGE_TILE_CHOICES = {
    # (right, up, left) -> tile_type
    (IN, IN, IN): "sink3",
    (IN, IN, OUT): "l_fork2",
    (IN, OUT, IN): "fork2",
    (IN, OUT, OUT): "r_fork2",
    (OUT, IN, IN): "r_fork2",
    (OUT, IN, OUT): "fork2",
    (OUT, OUT, IN): "l_fork2",
    (OUT, OUT, OUT): "source3",
    (EDGE, IN, IN): "sink2",
    (EDGE, IN, OUT): "corner",
    (EDGE, OUT, IN): "corner",
    (EDGE, OUT, OUT): "source2",
}

def left_shift_tuple4(tuple, places):
    return (
        tuple[places % 4],
        tuple[(1 + places) % 4],
        tuple[(2 + places) % 4],
        tuple[(3 + places) % 4]
    )

assert left_shift_tuple4((1, 2, 3, 4), 3) == (4, 1, 2, 3)


class EdgeDirectionTiling(receipts.Receipt):
    ARTWORK_ID = 'edge_directions'
    
    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            '-s',
            '--square-size',
            type=float,
            default=0.25,
            help="Size of a grid square in inches. Defaults to 1/4 inch"
        )

    def setup(self):
        square_size = self.args.square_size * self.PPI
        self.grid_width = int(self.width / square_size)
        self.grid_height = int(self.height / square_size)
        self.square_size = square_size

        self.grid = [
            [None] * self.grid_width
            for _ in range(self.grid_height)
        ]
        self.v_edges = [
            [None] * (self.grid_width + 1)
            for _ in range(self.grid_height)
        ]
        self.h_edges = [
            [None] * self.grid_width
            for _ in range(self.grid_height + 1)
        ]
        self.populate_edges()
        self.populate_tiles()
    
    def populate_edges(self):
        V_CHOICES = [LEFT, RIGHT]
        for i in range(self.grid_height):
            for j in range(1, (self.grid_width + 1) - 1):
                self.v_edges[i][j] = random.choice(V_CHOICES)
        
        H_CHOICES = [UP, DOWN]
        for i in range(1, (self.grid_height + 1) - 1):
            for j in range(self.grid_width):
                self.h_edges[i][j] = random.choice(H_CHOICES)
    
    def populate_tiles(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                right = self.v_edges[i][j + 1]
                up = self.h_edges[i][j]
                left = self.v_edges[i][j]
                down = self.h_edges[i + 1][j]
                tile = self.pick_tile((right, up, left, down))

                # For braid crossings, the over/under directions
                # are picked via a checkerboard to give a better
                # chance of weaving the threads
                if tile == ("cross", 0):
                    rotation = (i + j) % 2
                    tile = ("cross", rotation)

                self.grid[i][j] = tile
    
    def pick_tile(self, edges):
        (right_edge, up_edge, left_edge, down_edge) = edges
        if right_edge == RIGHT:
            right = OUT
        elif right_edge == LEFT:
            right = IN
        else:
            right = EDGE
        
        if up_edge == UP:
            up = OUT
        elif up_edge == DOWN:
            up = IN
        else:
            up = EDGE

        if left_edge == LEFT:
            left = OUT
        elif left_edge == RIGHT:
            left = IN
        else:
            left = EDGE
        
        if down_edge == DOWN:
            down = OUT
        elif down_edge == UP:
            down = IN
        else:
            down = EDGE
        
        key = (right, up, left, down)
        tile_choices = TILE_CHOICES.get(key, None)

        if tile_choices is None:
            return self.pick_edge_tile(key)
        
        return random.choice(tuple(tile_choices))
    
    def pick_edge_tile(self, key):
        # 4 edges to a tile
        N = 4

        # Find the first edge. This will always be defined
        first_edge = None
        for i in range(N):
            if key[i] == EDGE:
                first_edge = i
                break
        
        # Find the second edge. If it exists, this is a corner tile
        second_edge = None
        for i in range(first_edge + 1, N):
            if key[i] == EDGE:
                second_edge = i
                break

        # Determine which edge to put at the bottom. For corners, we want
        # the second edge to be on the right
        start_index = first_edge
        if second_edge is not None and (second_edge - first_edge) != 1:
            start_index = second_edge
        
        # How many 90 degree rotations are needed to rotate from the bottom
        # to the correct orientation.
        rotation = (start_index + 1) % N

        # cycle the key so that the edge is in the first slot
        # e.g. (IN, EDGE, OUT, OUT) -> (EDGE, OUT, OUT, IN). This is
        # symbolically like rotating the tile so that the edge is on the bottom.
        edge_key = left_shift_tuple4(key, start_index)

        # The lookup table assumes the first entry is EDGE since it's always
        # on the bottom
        tile = EDGE_TILE_CHOICES[edge_key[1:]]
        return (tile, rotation)
    
    def draw(self):
        thickness = 1.0 / self.square_size

        self.define_function("sink4", [
            "newpath",
            "0 0.5 moveto",
            "1 0.5 lineto",
            "0.5 0 moveto",
            "0.5 1 lineto",
            "stroke",
            "newpath",
            "0.5 0.5 0.125 0 360 arc",
            "gsave",
            "1 setgray",
            "fill",
            "grestore",
            "0 setgray",
            "stroke"
        ])

        self.define_function("source4", [
            "newpath",
            "0 0.5 moveto",
            "1 0.5 lineto",
            "0.5 0 moveto",
            "0.5 1 lineto",
            "stroke",
            "newpath",
            "0.5 0.5 0.125 0 360 arc",
            "fill",
        ])

        self.define_function("truchet", [
            "newpath",
            "1 0 0.5 90 180 arc",
            "stroke",
            "newpath",
            "0 1 0.5 270 360 arc",
            "stroke"
        ])

        self.define_function("fork3", [
            "newpath",
            "0 0 0.5 0 90 arc",
            "stroke",
            "newpath",
            "1 0 0.5 90 180 arc",
            "stroke",
            "newpath",
            "0.5 0 moveto",
            "0.5 1 lineto",
            "stroke"
        ])

        self.define_function("cross", [
            "newpath",
            "0 0.5 moveto",
            "1 0.5 lineto",
            "0.5 0 moveto",
            "0.5 0.4 lineto",
            "0.5 0.6 moveto",
            "0.5 1 lineto",
            "stroke"
        ])

        self.define_function("corner", [
            "newpath",
            "0 1 0.5 270 360 arc",
            "stroke",
        ])

        self.define_function("fork2", [
            "newpath",
            "0 1 0.5 270 360 arc",
            "stroke",
            "newpath",
            "1 1 0.5 180 270 arc",
            "stroke"
        ])

        self.define_function("l_fork2", [
            "newpath",
            "0 1 0.5 270 360 arc",
            "stroke",
            "newpath",
            "0 0.5 moveto", 
            "1 0.5 lineto",
            "stroke"
        ])

        self.define_function("r_fork2", [
            "newpath",
            "1 1 0.5 180 270 arc",
            "stroke",
            "newpath",
            "0 0.5 moveto", 
            "1 0.5 lineto",
            "stroke"
        ])

        self.define_function("sink2", [
            "newpath",
            "0 0.5 moveto",
            "0.5 0.5 lineto",
            "0.5 1 lineto",
            "stroke",
            "newpath",
            "0.5 0.5 0.125 0 360 arc",
            "gsave",
            "1 setgray",
            "fill",
            "grestore",
            "0 setgray",
            "stroke"
        ])

        self.define_function("sink3", [
            "newpath",
            "0 0.5 moveto",
            "1 0.5 lineto",
            "0.5 0.5 moveto",
            "0.5 1 lineto",
            "stroke",
            "newpath",
            "0.5 0.5 0.125 0 360 arc",
            "gsave",
            "1 setgray",
            "fill",
            "grestore",
            "0 setgray",
            "stroke"
        ])

        self.define_function("source2", [
            "newpath",
            "0 0.5 moveto",
            "0.5 0.5 lineto",
            "0.5 1 lineto",
            "stroke",
            "newpath",
            "0.5 0.5 0.125 0 360 arc",
            "fill",
        ])

        self.define_function("source3", [
            "newpath",
            "0 0.5 moveto",
            "1 0.5 lineto",
            "0.5 0.5 moveto",
            "0.5 1 lineto",
            "stroke",
            "newpath",
            "0.5 0.5 0.125 0 360 arc",
            "fill",
        ])

        self.define_function("rot90", [
            "0.5 0.5 translate",
            "90 mul rotate",
            "-0.5 -0.5 translate"
        ])

        self.add_lines([
            f"0 0 {self.width} {self.height} rectstroke",
            f"{self.square_size} {self.square_size} scale",
            f"{thickness} setlinewidth",
        ])

        for i in range(self.grid_height):
            y = (self.grid_height - 1) - i
            for j in range(self.grid_width):
                x = j
                tile = self.grid[i][j]
                if tile is not None:
                    (command, rotation) = tile
                    self.add_lines([
                        "gsave",
                        f"{x} {y} translate",
                        f"{rotation} rot90",
                        f"{command}",
                        "grestore"
                    ])