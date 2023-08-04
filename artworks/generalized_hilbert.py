import itertools

from postscriptlib import receipts
from postscriptlib.path import Path
from postscriptlib.psturtle import PSTurtle
from postscriptlib.lsystem import LSystem
from postscriptlib.rectangle import Rectangle

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

def swap_symbols(pattern, symbol_a, symbol_b, temp_symbol):
    return (pattern
        .replace(symbol_a, temp_symbol)
        .replace(symbol_b, symbol_a)
        .replace(temp_symbol, symbol_b)
    )

def get_rule_b(rule_a):
    """
    Rule b is the backwards version of a. This involves:
    1. reverse the string
    2. swap a <-> b
    3. swap L <-> R

    Note that F stays unchanged.
    """
    backwards = rule_a[::-1]
    swapped = swap_symbols(backwards, 'a', 'b', '$')
    return swap_symbols(swapped, 'L', 'R', '$')

def make_rules(rule_a):
    rule_a = rule_a.replace(' ', '')
    return {
        "a": rule_a,
        "b": get_rule_b(rule_a)
    }

RULE_SPIRAL = "aFaFaF LbFbFbFbLF aF LbFbLF aRF RaFaFaRF bFbF RaFaFaFaFaRF bFbFbFbL"
RULE_CUTOUT = "aFLbFbFbLFaRFRaFaFaRFbFbLFaRFbL"
RULE_M = "LbF RaF aRF bLF LbF RaF aRF bL"
RULE_PULSE = "LbF bF bF RaF aF aRF bF bF bLF a"
RULE_UP_AND_DOWN = (
    "LbF RaF aRF bF"
    "bF  bLF LbF bF"
    "bF  bF  RaF aRF"
    "bF  bF  bLF LbF"
    "Ra"
)
RULE_INTERLOCKING = (
    "aF  aF  LbF bF  bF"
    "bLF aF  aRF bF  bF"
    "bF  RaF aF  LbF bF"
    "bF  bF  RaF aRF bF" 
    "bF  bF  bF  bF  bF"
    "bF  bF  bF  bF  bLF"
    "aF  LbF bF  bLF aRF"
    "RaF aF  LbF bF  bF"
    "bF  RaF aRF bF  bF"
    "bF  bF  bF  RaF LbF"
    "bLF a"
)

DIVISIONS = 4
RULE = RULE_SPIRAL
ITERS = 2

class GeneralizedHilbert(receipts.Receipt):
    ARTWORK_ID = 'generalized_hilbert'

    def setup(self):
        self.turtle = PSTurtle(angle_divisions=DIVISIONS)
        self.l_system = LSystem(make_rules(RULE), "a")

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