import random

from papertoaster import receipts
from papertoaster.vec2 import Vec2

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


class QuietDice(receipts.Receipt):
    ARTWORK_ID = 'quiet_dice'

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            "n",
            type=int,
            help="how many dice to roll"
        )
        subparser.add_argument(
            "sides",
            type=int,
            help="how many sides per die"
        )
        subparser.add_argument(
            "-m",
            "--modifier",
            type=int,
            default=0,
            help="Constant modifier to add to each roll"
        )

    def setup(self):
        self.n = self.args.n
        self.sides = self.args.sides
        self.modifier = self.args.modifier

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
                self.draw_text(Vec2(x, y), result_str)

        self.set_font("Courier-Bold", TITLE_SIZE)
        if self.modifier == 0:
            title = f"{self.n}d{self.sides}"
        else:
            title = f"{self.n}d{self.sides} + {self.modifier}"
        self.draw_text(Vec2(0, self.title_y), title)
