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
started making a sketchbook-like interface for these receipts.

## 2022-06-20 Quiet Dice

Today I explored writing text in PostScript. I made a simple "quiet dice"
roller -- it's just a list of randomly generated numbers. Ideal for when you
need a lot of dice rolls (e.g. I sometimes procedurally generate dice) but
actual dice are either not available, or would be too noisy.

Next Steps:

* I have an idea for varying the hitomezashi patterns with variable widths
* I want to make tilings of the plane for more interesting grids to print.

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

## 2022-07-24 Braids

Yesterday and today, I tried making a simple tiling of strings crossed into
braids. It looks pretty cool, but there's more I could potentially do with it.
For example, I could take a sorting algorithm, keep track of the swaps and
generate a braid layout. Though I need to think through how to encode such
steps here

## 2022-09-03 Edge Direction Tiling

Today I made a rather tangled-looking tiling based on placing
arrows on each edge of the tiling, pointing in or out of the
tiles. Then lines are drawn inside the tile to connect the
arrows in such a way that the flow is consistent. Sometimes
this requires some special cases, like creating a source where
all the arrows point outwards or a sink where all the arrows
point inwards. Furthermore, there are cases where there are
multiple possible ways to draw the lines, I allow random
choices in such cases.

In retrospect, I could have implemented this by just randomly
placing tiles, since all the tiles except the edges connect at
all 4 edges. However, I did the extra effort to ensure the
two properties:

1. The flow of the arrows should be consistent. If you trace
    any path from a source, it should always lead to a sink
    (Or at least not lead to another source?)
2. For the "braid" like crossings, there's only one tile
    technically, but it can be rotated 90 degrees in checkerboard-fashion to make a more weave-like pattern.