import argparse
import random

from postscriptlib import receipts, path

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

SQUARE_SIZE = 0.25 * PPI

FONT_SIZE = 12
# Determined empirically. Probably would be better to
# learn how stringwidth works in PostScript instead...
COLUMNS = 6
CHARS_PER_COLUMN = 3
CHAR_WIDTH = 7

TITLE_SIZE = 2 * FONT_SIZE

class Receipt(receipts.Receipt):
    def setup(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "n", 
            type=int, 
            help="how many dice to roll"
        )
        parser.add_argument(
            "sides", 
            type=int, 
            help="how many sides per die"
        )
        parser.add_argument(
            "-m",
            "--modifier",
            type=int,
            default=0,
            help="Constant modifier to add to each roll"
        )
        args = parser.parse_args(self.args)
        self.n = args.n
        self.sides = args.sides
        self.modifier = args.modifier

        # Divide the paper into rows of 12 points.
        # the title will go in the top 2 rows
        rows = int(self.height / FONT_SIZE)
        self.rows = rows - 2
        self.title_y = (rows - 2) * FONT_SIZE

        self.cols = COLUMNS

    def roll_dice(self):
        total = 0
        for i in range(self.n):
            total += random.randint(1, self.sides)
        return total + self.modifier
    
    def draw(self):
        self.set_font("Courier-Bold", FONT_SIZE)
        for i in range(self.rows):
            y = i * FONT_SIZE
            for j in range(self.cols):
                x = j * CHAR_WIDTH * (CHARS_PER_COLUMN + 1)
                result = self.roll_dice()
                result_str = f"{result:>{CHARS_PER_COLUMN}} "
                self.draw_text(x, y, result_str)
        
        self.set_font("Courier-Bold", TITLE_SIZE)
        title = f"{self.n}d{self.sides} + {self.modifier}"
        self.draw_text(0, self.title_y, title)