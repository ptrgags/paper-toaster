import itertools

from postscriptlib import receipts
from postscriptlib.path import Path
from postscriptlib.psturtle import PSTurtle
from postscriptlib.lsystem import LSystem
from postscriptlib.rectangle import Rectangle

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

RULES = {
    "a": "aFLbFbFbLFaRFRaFaFaRFbFbLFaRFbL",
    "b": "RaFLbFRaFaFLbFbFbLFLbFRaFaFaRFb",

    # the spaces help with debugging
    #"a": "aFaFaF LbFbFbFbLF aF LbFbLF aRF RaFaFaRF bFbF RaFaFaFaFaRF bFbFbFbL".replace(' ', ''),
    #"b": "RaFaFaFa FLbFbFbFbFbL FaFa FLbFbFbL FLb FRaFaR Fb FRaFaFaFaR FbFbFb".replace(' ', ''),
}

ITERS = 4

class Receipt(receipts.Receipt):
    def setup(self):
        self.turtle = PSTurtle(angle_divisions=4)
        self.l_system = LSystem(RULES, "a")

        # make a 2 inch bounding box in which we will draw
        # the pattern
        cx = self.width / 2
        cy = 9.0 / 16.0 * self.height
        box_width = 2.0 * PPI
        self.drawing_bounds = Rectangle(
            cx - 0.5 * box_width,
            cy - 0.5 * box_width,
            box_width,
            box_width
        )
    
    def draw(self):
        gen = self.l_system.generate()
        production = next(itertools.islice(gen, ITERS, ITERS + 1))
        for c in production:
            if c == "F":
                self.turtle.forward(1.0)
            elif c == "L":
                self.turtle.turn(1)
            elif c == "R":
                self.turtle.turn(-1)

        curve = self.turtle.make_path(self.drawing_bounds)
        self.add_path(curve)
        self.set_line_width(0.1)
        self.stroke()

        border = Path()
        border.rect(0, 0, self.width, self.height)
        self.add_path(border)
        self.set_line_width(1)
        self.stroke()