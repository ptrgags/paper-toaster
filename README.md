# Receipt Art (2022)

This repo is for generative art with PostScript output that can be printed
to standard `3 1/8 inch` receipt paper.

I like to make art at art trading card size (2.5 x 3.5 in), so this code is
designed around that.

## Usage

```bash
# Generate the postscript file in output/<artwork_id>.ps
# see -h for options. 
python main.py [options] <artwork_id> -- [<artwork_arg> ...]

# Convert to PDF (optional). Requires GhostScript:
ps2pdf output/<artwork_id>.ps

# Print the results!
```

The `--num-cards` option changes the height of the output from 1 art trading
card to multiple. For example, I sometimes print a column 3 cards tall.

## Artworks

Here is a list of artwork IDs and what they do:

* `grid` - prints basic graph paper
* `hitomezashi [options] <row_bits> <col_bits>` - Prints hitemozashi stitching
    patterns (inspired by [this Numberphile video](https://www.youtube.com/watch?v=JbfhzlMk2eY))
    `row_bits` and `col_bits` are any integer or `0bxxxxx` binary number. Each
    row/column of the grid will use one bit from the respective number. To get
    good variation, pick numbers with many bits set.
* `hex_grid` - prints a hexagonal grid pattern
* `fm_ring` - prints a generative art using frequency modulation and parametric
    equations.
* `turtle_dance [options] {natural,square,triangle,fibonacci} A B` - Generates
    patterns with turtle graphics taking a sequence of numbers and two integers
    `A` and `B` for modular arithmetic. This is a generalization of [This 
    Bridges math art paper](https://archive.bridgesmathart.org/2017/bridges2017-139.pdf)