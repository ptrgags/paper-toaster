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

## 2022-07-23 Start refactoring

Today I started refactoring `postscriptlib`, adding the following changes:

1. Added the `Vec2` class from a different branch
2. Refactored how the argparse usage works. Now each artwork adds its own
    subparser
3. Added a `circle()` command to draw dots
4. Refactored the existing artworks and added some more parameters as I went

Next steps:

* Refactor abstractions. A `Document` for global details and a `Page` for
    things that can be repeated
* Consider using context managers for paths and graphics states?
* Add a way to define functions at the document level.
* Some commands must be stroked immediately, how to handle these?

## 2022-07-24 Iso Grid

Today I made a script to render an isometric map given a grid of height
values. It works best when the heights increase towards the top right corner
of the grid, else things get occluded