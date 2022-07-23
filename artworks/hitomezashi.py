import argparse

from postscriptlib import receipts, path

PPI = receipts.Receipt.PPI

# Use quarter-inch squares
SQUARE_SIZE = 0.25 * PPI

def bin_or_dec(s):
    if s.startswith("0b"):
        return int(s[2:], 2)
    return int(s)

def flip_bit(b):
    return (~b) & 1

class Hitomezashi(receipts.Receipt):
    ARTWORK_ID = 'hitomezashi'

    def setup(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "row_bits", 
            type=bin_or_dec, 
            help="one bit per row of the grid. 0b notation is allowed."
        )
        parser.add_argument(
            "col_bits", 
            type=bin_or_dec, 
            help="One bit per column of the grid. 0b notation is allowed."
        )
        parser.add_argument(
            "--odd-even",
            action="store_true",
            help="If true, fill in with an odd/even coloring"
        )
        args = parser.parse_args(self.args)

        self.row_bits = args.row_bits
        self.col_bits = args.col_bits
        self.odd_even = args.odd_even

        self.grid_width = int(self.width / SQUARE_SIZE)
        self.grid_height = int(self.height / SQUARE_SIZE)
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

                x = i * SQUARE_SIZE
                y1 = j * SQUARE_SIZE
                y2 = (j + 1) * SQUARE_SIZE
                stitches.line(x, y1, x, y2)

    def draw_rows(self, stitches):
        cols = self.grid_width + 1
        rows = self.grid_height + 1
        for i in range(rows):
            parity = (self.row_bits >> i) & 1
            for j in range(cols):
                if j % 2 != parity:
                    continue

                y = i * SQUARE_SIZE
                x1 = j * SQUARE_SIZE
                x2 = (j + 1) * SQUARE_SIZE
                stitches.line(x1, y, x2, y)

    def fill_squares(self):
        filled = path.Path()
        for i in range(self.grid_width):
            x = i * SQUARE_SIZE
            for j in range(self.grid_height):
                y = j * SQUARE_SIZE
                if self.grid[j][i] == 1:
                    filled.rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
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