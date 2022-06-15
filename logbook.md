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