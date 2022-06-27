# Receipt Art

## 2022-06-15 Starting Out

Today I started this repo with some prototype scripts to test out the receipt
printer. I found that the 2.5 x 3.5 inch art trading card size is actually
perfect for printing! (though you could easily go longer)

Eventually this should be turned into a sketchbook type format, though I need
to think more about what that should do, and how to account for the difference
in paper size.

As for the scripts themselves:

* `grid.py` is a very basic test of making 1/4 inch graph paper
* `hex_grid.py` makes a hexagonal grid, though I included some gaps between
    tiles just for the hell of it
* `fm_ring.py` takes the concept of FM synthesis and wraps it around the circle
    to make some interesting patterns. There might be more interesting ways
    to map FM to 2D, but I'll try that some other time.

Next Steps:

* Make a simple sketch-like interface
* Try other patterns
* Make the grids extendable to long receipts

## 2022-06-17 Hitomezashi Stitching Patterns

Today I implemented hitemozashi patterns, inspired by
[this Numberphile video](https://www.youtube.com/watch?v=JbfhzlMk2eY). I also
started making a sketchbook-like interface for these receipts. I still need
to refactor `hex_grid` and `fm_ring` though.

## 2022-06-27 Dancing Turtles

Today I tried out the math from 
[This 2017 Bridges paper](https://archive.bridgesmathart.org/2017/bridges2017-139.pdf)
to make turtle graphics "dances" with integer sequences and modular arithmetic.
The paper only shows the math for the sequence of natural numbers, but I'm
also trying other sequences. I'm also trying odd-even coloring (nice that
PostScript comes with a built-in `eofill` command!)

Next Steps:

* Add a parameter to control the angle divisions (default 360)
* Determine when to stop... the paper gives one formula, but can it be
    generalized for other sequences?
* Experiment with more sequences