# Paper Toaster (Thermal Receipt Printer Art) (2022, 2023)

This repo is for generative art with PostScript output that can be printed
to standard 3 1/8 inch (80 mm) thermal receipt paper. I personally use [this 
Rongta point-of-sale (POS) printer](https://www.amazon.com/gp/product/B08V4H7T47/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) to print my artwork.

I like to make my art at art trading card size (2.5 x 3.5 in), so this code is
designed around that. This size is conveniently just a little bit narrower
than the paper, so it pairs well.

I jokingly refer to my receipt printer as a "paper toaster" since a thermal
printer works by heating the thermal paper, darkening it. No ink is used.

## Dependencies

[GhostScript](https://www.ghostscript.com/) must be installed for PDF and PNG exports to work

## Usage

```bash
# Generate the postscript file in output/<artwork_id>.ps
# see -h for options. 
python main.py [options] <artwork_id> -- [<artwork_arg> ...]

# Print the results!
```

The `--num-cards` option changes the height of the output from 1 art trading
card to multiple. For example, I sometimes print a column 3 cards tall.

## Artworks

The sections below give a summary of the different artworks and explain the
parameters. They are listed in reverse chronological order to feature newest
artworks

Examples marked with :test_tube: indicate artistic experiments by messing
with the parameters in ways I didn't originally intend.

### Hex Grid (2022-06)

Hex grid with some optional gaps between hexagons. It also can render dots
instead of lines.

This artwork only supports a single card-length receipt

**Parameters:**

| Parameter | Description |
|---|---|
| `-s/--side-length SIDE_LENGTH` | The side length of each hexagon in inches. Defaults to 1/4 inch |
| `-e/--expand-factor EXPAND_FACTOR` | How much to expand/contract the grid for artistic effect |
| `-d/--dots` | Draw the hexagon vertices, but do not connect them. This can be used to make a hex grid  |

**Examples:**

| Example | Command | Description |
|---|---|---|
| ![Default hex grid](figures/hex_grid_default.png) | `main.py hex_grid` | Default settings |
| ![Hex grid with gaps](figures/hex_grid_gaps.png) | `main.py hex_grid -e 1.2` | Increase the expand factor to create gaps between the hexagons |
| ![Hex grid dots](figures/hex_grid_dots.png) | `main.py hex_grid --dots` | Just render a hexagon grid with just dots|
| ![Experiment: overlap](figures/hex_grid_overlap.png) | `main.py hex_grid -e 0.8` | :test_tube: Decrease the expand factor to make the hexagons overlap for neat effect |
| ![Experiment: contracted dots](figures/hex_grid_contracted_dots.png) | `main.py hex_grid --dots -e 0.8` | :test_tube: Turn on dots, but also contract the hexagons like the overlap case |

### Grid (2022-06)

This was a warm-up exercise, this makes a card with graph paper.

**Parameters:**

| Parameter | Description |
|---|---|
| `-s/--square-size SQUARE_SIZE` | The size of each grid square. Defaults to 1/4 inch |

**Examples:**

| Example | Command | Description |
| --- | --- | --- | 
| ![Default grid](figures/grid_default.png) | `python main.py grid` | Default settings (1/4 inch grid when printed)
| ![1/8 inch grid](figures/grid_eighth.png) | `python main.py grid -s 0.125` | finer 1/8 inch grid |

<!--

* `hitomezashi -- [options] <row_bits> <col_bits>` - Prints hitemozashi stitching
    patterns (inspired by [this Numberphile video](https://www.youtube.com/watch?v=JbfhzlMk2eY))
    `row_bits` and `col_bits` are any integer or `0bxxxxx` binary number. Each
    row/column of the grid will use one bit from the respective number. To get
    good variation, pick numbers with many bits set.
* `fm_ring` - prints a generative art using frequency modulation and parametric
    equations.
* `barcode_code128 <text>` - Encodes text as a
    [Code 128](https://en.wikipedia.org/wiki/Code_128) barcode.
* `turtle_dance [options] {natural,square,triangle,fibonacci} A B` - Generates
    patterns with turtle graphics taking a sequence of numbers and two integers
    `A` and `B` for modular arithmetic. This is a generalization of
    ["Let the Numbers Do the Walking:
Generating Turtle Dances on the Plane from Integer Sequences"](https://archive.bridgesmathart.org/2017/bridges2017-139.pdf)
* `quiet_dice -- <n> <sides> [-m <modifier>]` - rolls the give dice expression
    `<n>d<s> + <modifier>` many times and prints a table of results. Perfect for
    when there are no dice available or rolling dice would be to noisy.

-->

## Logbook

This project is a bunch of artistic experiments. As I went, I kept a log
of what I worked on and more context. You can find it here:

[Logbook](logbook.md)