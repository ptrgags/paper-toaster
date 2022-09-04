import random

from postscriptlib import receipts
from postscriptlib.pq import PriorityQueue

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

RED = 0
GREEN = 1
BLUE = 2
WHITE = 3

WANG_TILES = [
    (2, 1, 1, 2),
    (4, 3, 3, 4),
    (5, 4, 4, 5),
    (3, 6, 6, 3),
    (5, 4, 3, 4),
    (3, 6, 3, 4),
    (4, 3, 4, 5),
    (4, 3, 6, 3),
    (1, 5, 2, 3),
    (1, 4, 2, 6),
    (1, 5, 1, 4),
    (2, 3, 2, 6),
    (6, 2, 4, 1),
    (3, 2, 5, 1),
    (6, 2, 3, 2),
    (4, 1, 5, 1),
]

'''
WANG_TILES = [
    (RED, RED, GREEN, RED),
    (RED, BLUE, GREEN, BLUE),
    (GREEN, RED, GREEN, GREEN),
    (BLUE, WHITE, BLUE, RED),
    (BLUE, BLUE, BLUE, WHITE),
    (WHITE, WHITE, WHITE, RED),
    (GREEN, RED, WHITE, BLUE),
    (WHITE, BLUE, RED, BLUE),
    (RED, BLUE, RED, WHITE),
    (GREEN, GREEN, RED, BLUE),
    (WHITE, RED, GREEN, RED)
]
'''

def init_tile_choices():
    result = {}
    for i, tile in enumerate(WANG_TILES):
        for direction, color in enumerate(tile):
            result.setdefault((direction, color), set()).add(i)
    return result

TILE_CHOICES = init_tile_choices()

class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.tile = None
        # Start with all options possible.
        self.choices = set(range(len(WANG_TILES)))
    
    def __len__(self):
        return len(self.choices)
    
    def select_tile(self):
        choices = list(self.choices)
        assert self.tile is None
        assert len(choices) > 0
        self.tile = random.choice(choices)
    
    def get_neighbors(self):
        assert self.tile is not None

        i = self.row
        j = self.column
        
        (right_color, up_color, left_color, down_color) = WANG_TILES[self.tile]
        
        # Get the neighbor tile coordinates, along with a constraint.
        # the adjacent tile will have the opposite direction, but the same
        # color
        return [
            (i, j + 1, (LEFT, right_color)),
            (i - 1, j, (DOWN, up_color)),
            (i, j - 1, (RIGHT, left_color)),
            (i + 1, j, (UP, down_color))
        ]
    
    def add_constraint(self, constraint):
        constraint_tiles = TILE_CHOICES[constraint]
        self.choices &= constraint_tiles

class WangTiles(receipts.Receipt):
    ARTWORK_ID = 'wang_tiles'
    
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
        self.tiles = [None for i in range(self.grid_width * self.grid_height)]
        self.priority_queue = PriorityQueue()

        self.init_grid()
        self.wavefunction_collapse()
    
    def init_grid(self):
        # Generate all the tiles in the grid, but do so in a random order
        # to prevent the priority queue from being biased towards the
        # top row of the grid
        coordinates = [
            (i, j)
            for i in range(self.grid_height)
            for j in range(self.grid_width)
        ]
        random.shuffle(coordinates)

        for (i, j) in coordinates:
            cell = Cell(i, j)
            self.tiles[i * self.grid_width + j] = cell

            # We want to visit tiles starting with the ones with lowest
            # entropy. In this case, all the tiles are equally likely, so
            # the number of choices can be used instead. Here, the fewer
            # choices, the sooner the cell will be picked. Since the priority
            # queue is a min-heap, we can use the count of choices directly.
            self.priority_queue.add(cell, len(cell))
    
    def wavefunction_collapse(self):
        cell = self.priority_queue.pop()
        while cell is not None:
            # 1. Randomly choose one of the remaining options
            cell.select_tile()

            # 2. for all the valid neighbors, update their set of choices
            #    and thus their priority
            for (i, j, constraint) in cell.get_neighbors():
                in_row_bounds = 0 <= i < self.grid_height
                in_col_bounds = 0 <= j < self.grid_width
                if not (in_row_bounds and in_col_bounds):
                    continue
                
                neighbor = self.tiles[i * self.grid_width + j]

                # We've already visited the neighbor
                if neighbor.tile is not None:
                    continue

                neighbor.add_constraint(constraint)

                # add() handles updating the priority
                self.priority_queue.add(neighbor, len(neighbor))

            cell = self.priority_queue.pop()
    
    def draw(self):
        pass