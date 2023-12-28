"""
Turtle Dance

An exploration of the 2017 Bridges math art paper
"Let the Numbers Do the Walking:
Generating Turtle Dances on the Plane from Integer Sequences" by Adam Colestock

https://archive.bridgesmathart.org/2017/bridges2017-139.pdf
"""

import argparse
import itertools

from postscriptlib import receipts
from postscriptlib.path import Path
from postscriptlib.psturtle import PSTurtle
from postscriptlib.rectangle import Rectangle

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

SQUARE_SIZE = 0.25 * PPI

SEQUENCE_CHOICES = [
    "natural",
    "square",
    "fibonacci",
    "triangle"
]

def fibonacci_seq():
    """
    Fibonacci sequence:
    F(0) = 0
    F(1) = 1
    F(n) = F(n - 1) + F(n - 2) for n >= 2
    """
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b

def triangle_seq():
    """
    Triangle numbers: 
    T(1) = 1
    T(n) = T(n - 1) + n for n >= 2
    """
    a = 0
    for i in itertools.count(1):
        a += i
        yield a

def select_sequence(s):
    if s == "natural":
        return itertools.count(0)
    elif s == "square":
        return (x * x for x in itertools.count(0))
    elif s == "fibonacci":
        return fibonacci_seq()
    elif s == "triangle":
        return triangle_seq()

def modular_difference(seq, a, b):
    for x in seq:
        yield x % a - x % b

class TurtleDance(receipts.Receipt):
    ARTWORK_ID = 'turtle_dance'

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            "sequence",
            choices=SEQUENCE_CHOICES,
            help="Which sequence to use to generate the image"
        )
        subparser.add_argument("a", type=int, help="first modulus")
        subparser.add_argument("b", type=int, help="second modulus")
        subparser.add_argument(
            "--divisions",
            type=int,
            default=360,
            help="Angles used are 2 pi / divisions"
        )
        subparser.add_argument(
            "--fill",
            action="store_true",
            help="even/odd fill instead of stroke the path"
        )

    def setup(self):
        if self.num_cards > 1:
            raise ValueError("turtle_dance only supports 1 card")

        self.sequence = modular_difference(
            select_sequence(self.args.sequence),
            self.args.a,
            self.args.b
        )
        self.should_fill = self.args.fill

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

        self.turtle = PSTurtle(self.args.divisions)

    def turtle_dance(self):
        for i in itertools.count(1):
            self.turtle.forward(1.0)
            delta_heading = next(self.sequence)
            self.turtle.turn(delta_heading)

            if self.turtle.is_finished:
                print(f"Finished after {i} steps")
                break
    
    def draw(self):
        self.turtle_dance()
        
        dance = self.turtle.make_path(self.drawing_bounds)
        self.add_path(dance)
        if self.should_fill:
            self.even_odd_fill()
        else:
            self.stroke()

        border = Path()
        border.rect(0, 0, self.width, self.height)
        self.add_path(border)
        self.stroke()