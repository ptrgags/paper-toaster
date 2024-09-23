from papertoaster import receipts, path
from papertoaster.vec2 import Vec2


def bin_or_dec(s):
    if s.startswith("0b"):
        return int(s[2:], 2)
    return int(s)


def flip_bit(b):
    return (~b) & 1


class Hitomezashi(receipts.Receipt):
    ARTWORK_ID = 'hitomezashi'

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            "row_bits",
            type=bin_or_dec,
            help="one bit per row of the grid. 0b notation is allowed."
        )
        subparser.add_argument(
            "col_bits",
            type=bin_or_dec,
            help="One bit per column of the grid. 0b notation is allowed."
        )
        subparser.add_argument(
            "-o",
            "--odd-even",
            action="store_true",
            help="If true, fill in with an odd/even coloring"
        )
        subparser.add_argument(
            "-s",
            "--square-size",
            type=float,
            default=0.25,
            help="Size of each square in inches"
        )

    def setup(self):
        self.row_bits = self.args.row_bits
        self.col_bits = self.args.col_bits
        self.odd_even = self.args.odd_even
        square_size = self.args.square_size * self.PPI

        self.square_size = square_size
        self.grid_width = int(self.width / square_size)
        self.grid_height = int(self.height / square_size)
        self.grid = [
            [0 for _ in range(self.grid_width)]
            for _ in range(self.grid_height)
        ]

        if self.odd_even:
            self.compute_odd_even()

    def compute_odd_even(self):
        w = self.grid_width
        h = self.grid_height
        grid = self.grid
        grid[0][0] = 1

        # Compute the first column since this impacts the rest of the row
        current = 1
        for i in range(1, h):
            bit = (self.row_bits >> i) & 1
            if bit == 0:
                # negate the current bit
                current = flip_bit(current)
            grid[i][0] = current

        # Now go row by row and fill in the remaining cells, starting
        # with the values we just calculated
        for i in range(h):
            current = grid[i][0]
            parity = i % 2
            for j in range(1, w):
                bit = (self.col_bits >> j) & 1
                if bit == parity:
                    current = flip_bit(current)
                grid[i][j] = current

    def draw_columns(self, stitches):
        cols = self.grid_width + 1
        rows = self.grid_height + 1
        for i in range(cols):
            parity = (self.col_bits >> i) & 1
            for j in range(rows):
                if j % 2 != parity:
                    continue

                x = i * self.square_size
                y1 = j * self.square_size
                y2 = (j + 1) * self.square_size
                stitches.line(Vec2(x, y1), Vec2(x, y2))

    def draw_rows(self, stitches):
        cols = self.grid_width + 1
        rows = self.grid_height + 1
        for i in range(rows):
            parity = (self.row_bits >> i) & 1
            for j in range(cols):
                if j % 2 != parity:
                    continue

                y = i * self.square_size
                x1 = j * self.square_size
                x2 = (j + 1) * self.square_size
                stitches.line(Vec2(x1, y), Vec2(x2, y))

    def fill_squares(self):
        filled = path.Path()
        for i in range(self.grid_width):
            x = i * self.square_size
            for j in range(self.grid_height):
                y = j * self.square_size
                if self.grid[j][i] == 1:
                    filled.rect(x, y, self.square_size, self.square_size)
        self.add_path(filled)
        self.fill()

    def draw(self):
        if self.odd_even:
            self.fill_squares()

        stitches = path.Path()
        self.draw_columns(stitches)
        self.draw_rows(stitches)
        self.add_path(stitches)
        self.stroke()
