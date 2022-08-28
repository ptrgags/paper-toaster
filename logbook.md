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

## 2022-08-23 Colored braids

Today I tried a variation on `braids` that keeps track of a color per strand.
I tried using an odd-even sort algorithm to generate the braid. It looks nice,
but the thing is the algorithm stops after `n` iterations, which produces a
square, not a rectangle of arbitrary size. I'll have to think about another
way of generating the braid.

## 2022-08-28 Shuffle instead of sort

Today I made the algorithm support an arbitrary number of rows by working
backwards. Instead of starting with a shuffled array and progressively sorting
it, I start with a sorted array and apply `n` passes where at each pair of
strands it randomly chooses whether to swap the strands. The rows use the
same odd/even staggering as before, which helps to make reasonably dense
braids.