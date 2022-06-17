import argparse

from postscriptlib import receipts, path

PPI = receipts.Receipt.PPI

# Use quarter-inch squares
SQUARE_SIZE = 0.25 * PPI

def bin_or_dec(s):
    if s.startswith("0b"):
        return int(s[2:], 2)
    return int(s)

class Receipt(receipts.Receipt):
    def setup(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "row_bits", 
            type=bin_or_dec, 
            help="one bit for row of the grid. 0b notation is allowed."
        )
        parser.add_argument(
            "col_bits", 
            type=bin_or_dec, 
            help="One bit per column of the grid. 0b notation is allowed."
        )
        parser.add_argument(
            "--fill",
            help="If true, fill in with an odd/even coloring"
        )
        args = parser.parse_args(self.args)

        self.row_bits = args.row_bits
        self.col_bits = args.col_bits
        self.fill = args.fill

        self.grid_width = int(self.width / SQUARE_SIZE)
        self.grid_height = int(self.height / SQUARE_SIZE)
        self.grid = [0 for x in range(self.grid_width * self.grid_height)]
        
        if self.fill:
            self.compute_odd_even()
    
    def compute_odd_even(self):
        w = self.grid_width
        h = self.grid_height
        grid = self.grid
        grid[0] = 1

        raise Exception("NOBODY EXPECTS THE SPANISH INQUISITION!")

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
    
    def draw(self):
        stitches = path.Path()
        self.draw_columns(stitches)
        self.draw_rows(stitches)
        self.add_path(stitches)
        self.stroke()
        
        if self.fill:
            self.fill_squares()