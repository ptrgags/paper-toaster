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
[this Numberphile video](https://www.youtube.com/watch?v=JbfhzlMk2eY). I also started making a sketchbook-like interface for these receipts.

## 2022-06-20 Quiet Dice

Today I explored writing text in PostScript. I made a simple "quiet dice"
roller -- it's just a list of randomly generated numbers. Ideal for when you
need a lot of dice rolls (e.g. I sometimes procedurally generate dice) but
actual dice are either not available, or would be too noisy.

Next Steps:

* I have an idea for varying the hitomezashi patterns with variable widths
* I want to make tilings of the plane for more interesting grids to print.

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

## 2022-06-28 Exploring Turtle Dances

Today I added the angle divisions and added a stopping condition. Not perfect,
but most of the time it gives decent results

Here are some example settings:

```text
natural 45 25 --fill
natural 80 65
natural 70 80
natural 35 710
natural 234 32
natural 237 30
square 100 200
square 90 100 --fill
square 90 270
square 360 46 --divisions 12
triangle 350 20
triangle 25 40
triangle 100 200
triangle 350 500
triangle 40 20 --fill
triangle 468 32 --divisions 12 --fill
fibonacci 20 30
fibonacci 60 30 --fill
fibonacci 500 50
fibonacci 100 200 --divisions 12
fibonacci 300 100 --divisions 12
```

One thing I notice is that sometimes the output looks non-uniformly scaled.
I think this is because the remapping to the square output doesn't account
for the aspect ratio... I should consider fixing that in the future.

Another thing, to concatenate postscript/PDF files to a single PDF, the
command is:

```bash
gswin64 -o output.pdf -sDEVICE=pdfwrite input0.ps input1.ps
```

Next Steps:

* I think I want to move on to another idea with turtle graphics concerning
    generalized Hilbert curves, but I'll do that on another branch.

## 2022-07-03 Code 128 Barcodes

Today I started learning about barcodes. There's many different types from
UPC-A (used for labeling products for sale) to Code 128 (general-purpose
alphanumeric codes), and others (EAN, QR, PDF 417, to name a few others). I
started with Code 128 since it isn't too complicated of an encoding scheme
and supports alphanumeric characters, not just numbers.

Next Steps:

* Figure out a better way to handle the barcode given it is variable size.
    maybe landscape? Or compute the module size based on the output length?
* Allow exporting a text file with the 0s and 1s of the barcode, might be
    interesting to try making musical rhythms from the results (if so, would be
    done in a different repo)

## 2022-07-09 Elementary Cellular Automaton

Today I added a simple sketch that generates elementary cellular automata.

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

## 2022-07-24 Iso Grid

Today I made a script to render an isometric map given a grid of height
values. It works best when the heights increase towards the top right corner
of the grid, else things get occluded

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

I also added `--page-width` and `--page-height` to the global command line
options so I can make larger prints if so desired.