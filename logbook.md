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