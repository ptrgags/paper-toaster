import random

from papertoaster import receipts
from papertoaster.path import Path

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

# The grid will be pretty tiny, 1/32 of an inch
SQUARE_SIZE = PPI / 32.0


class ElementaryCA(receipts.Receipt):
    ARTWORK_ID = "elementary_ca"

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            "rule",
            type=int,
            help="rule number from 0 to 255")

    def setup(self):
        self.grid_width = int(self.width / SQUARE_SIZE)
        self.grid_height = int(self.height / SQUARE_SIZE)

        self.prev_row = [0] * self.grid_width
        self.current_row = [random.randint(0, 1)
                            for _ in range(self.grid_width)]
        self.rule = self.args.rule

    def compute_row(self):
        self.prev_row, self.current_row = self.current_row, self.prev_row
        for i in range(self.grid_width):
            left = self.prev_row[(i - 1) % self.grid_width]
            center = self.prev_row[i]
            right = self.prev_row[(i + 1) % self.grid_width]
            bit_index = left << 2 | center << 1 | right
            next_state_bit = self.rule >> bit_index & 1
            self.current_row[i] = next_state_bit

    def draw_current_row(self, grid, i):
        y = i * SQUARE_SIZE
        for j, val in enumerate(self.current_row):
            if val == 1:
                x = j * SQUARE_SIZE
                grid.rect(x, y, SQUARE_SIZE, SQUARE_SIZE)

    def draw(self):
        grid = Path()

        for i in range(self.grid_height):
            self.draw_current_row(grid, i)
            self.compute_row()

        self.add_path(grid)
        self.fill()
