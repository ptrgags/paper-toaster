import enum
import random

from papertoaster import receipts

STRAIGHT1 = 's1'
STRAIGHT2 = 's2'
CROSS = 'cr'

# Rainbow
PALETTE_RAINBOW = [
    "1 0 0",
    "1 0.5 0",
    "1 1 0",
    "0.5 1 0",
    "0 1 0",
    "0 1 0.5",
    "0 1 1",
    "0 0.5 1",
    "0 0 1",
]

GRAY_N = 10
GRAY_VALUES_NORMALIZED = [float(i) / (GRAY_N - 1) for i in range(GRAY_N)]
GRAY_VALUES = [0.5 * x + 0.25 for x in GRAY_VALUES_NORMALIZED]
PALETTE_GRAYSCALE = [f"{x} {x} {x}" for x in GRAY_VALUES]

PALETTE_STRIPES = [
    "1 0 0",
    "0.8 0.8 0.8",
    "1 1 1",
    "0.5 0.5 0.5",
    "0.5 0.5 0.5"
]

PALETTE_KINDLE = [
    "0 0 0",
    "0.25 0.25 0.25",
    "0.5 0.5 0.5"
]

PALETTE_INVERTED = [
    "0.5 0.5 0.5",
    "0.75 0.75 0.75",
    "1 1 1"
]

PALETTE = PALETTE_RAINBOW
PALETTE_SIZE = len(PALETTE)


def odd_even_shuffle(array, rows, swap_chance):
    n = len(array)
    for i in range(rows):
        row_commands = []
        first_index = i % 2

        if first_index == 1:
            # Handle a single strand on the left
            row_commands.append((STRAIGHT1, 0, array[0]))

        for j in range(first_index, n, 2):
            if j + 1 == n:
                # Handle a single strand on the right
                row_commands.append((STRAIGHT1, j, array[j]))
            elif random.random() < swap_chance:
                # Swap the two strands
                row_commands.append((CROSS, j, array[j], array[j + 1]))
                array[j], array[j + 1] = array[j + 1], array[j]
            else:
                # Keep the strands as-is
                row_commands.append((STRAIGHT2, j, array[j], array[j + 1]))

        yield row_commands


def strand_groups(s):
    return [int(x) for x in s.split(",")]


def make_groups(group_lengths, total_strands):
    all_strands = list(range(total_strands))

    strand_index = 0
    length_index = 0
    result = []
    while strand_index < total_strands:
        group_length = group_lengths[length_index]
        group = all_strands[strand_index:strand_index + group_length]
        result.append(group)

        # The slice might be smaller than group_length if we're at the end
        strand_index += len(group)

        # If group_lengths is too short, cycle around
        length_index += 1
        length_index %= len(group_lengths)

    return result


class ColoredBraids(receipts.Receipt):
    ARTWORK_ID = 'colored_braids'

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            '-s',
            '--square-size',
            type=float,
            default=0.125,
            help="Size of a grid square in inches. Defaults to 1/4 inch"
        )
        subparser.add_argument(
            "-w",
            "--stroke-width",
            type=float,
            default=2.0,
            help="width of a single strand in points"
        )
        subparser.add_argument(
            '-c',
            '--swap-chance',
            type=float,
            default=0.5,
            help=(
                "Chance of swapping a braid strand with its neighbor as a "
                "number in [0.0, 1.0]"
            )
        )
        subparser.add_argument(
            '-i',
            '--invert-colors',
            action="store_true",
            help="If set, use an inverted color scheme"
        )
        subparser.add_argument(
            '-g',
            '--groups',
            type=strand_groups,
            help=(
                "CSV of positive integers that determine groups of strands to "
                "weave. E.g. 3,4 means weave the first 3 strands, and the next "
                "4 strands separately. If not specified, all strands are woven."
            )
        )

    def setup(self):
        square_size = self.args.square_size * self.PPI
        self.grid_width = int(self.width / square_size)
        self.grid_height = int(self.height / square_size)
        self.square_size = square_size
        self.invert_colors = self.args.invert_colors
        self.swap_chance = self.args.swap_chance
        self.stroke_width = self.args.stroke_width

        num_strands = self.grid_width
        self.groups = self.args.groups or [num_strands]
        self.strand_array = make_groups(self.groups, num_strands)

    def draw(self):
        bg_color = 0 if self.invert_colors else 1
        thin = self.stroke_width / self.square_size
        thick = 3 * thin

        # usage: right_color left_color right_over_left
        # where the colors are
        # r g b
        self.define_function("right_over_left", [
            "newpath",
            "0 0 moveto",
            "0 0.5 1 0.5 1 1 curveto",
            # left strand color taken from stack
            "setrgbcolor",
            f"{thin} setlinewidth",
            "stroke",
            "newpath",
            "0 1 moveto",
            "0 0.5 1 0.5 1 0 curveto",
            "gsave",
            f"{thick} setlinewidth",
            f"{bg_color} setgray",
            "stroke",
            "grestore",
            f"{thin} setlinewidth",
            # right strand color taken from stack
            "setrgbcolor",
            "stroke",
        ])

        # usage: left_color right_color left_over_right
        # where the colors are
        # r g b
        self.define_function("left_over_right", [
            "newpath",
            "0 1 moveto",
            "0 0.5 1 0.5 1 0 curveto",
            # right strand color taken from stack
            "setrgbcolor",
            f"{thin} setlinewidth",
            "stroke",
            "newpath",
            "0 0 moveto",
            "0 0.5 1 0.5 1 1 curveto",
            "gsave",
            f"{thick} setlinewidth",
            f"{bg_color} setgray",
            "stroke",
            "grestore",
            f"{thin} setlinewidth",
            # left strand color taken from stack
            "setrgbcolor",
            "stroke",
        ])

        # usage right_color left_color straight2
        self.define_function("straight2", [
            "newpath",
            "0 0 moveto",
            "0 1 lineto",
            # left strand color taken from stack
            "setrgbcolor",
            f"{thin} setlinewidth",
            "stroke",
            "newpath",
            "1 0 moveto",
            "1 1 lineto",
            # right strand color taken from stack
            "setrgbcolor",
            f"{thin} setlinewidth",
            "stroke",
        ])

        # usage color straight1
        self.define_function("straight1", [
            "newpath",
            "0 0 moveto",
            "0 1 lineto",
            # color taken from stack
            "setrgbcolor",
            f"{thin} setlinewidth",
            "stroke"
        ])

        # Draw the background.
        self.add_lines([
            f"{bg_color} setgray",
            f"0 0 {self.width} {self.height} rectfill",
            f"{self.square_size} {self.square_size} scale",
            f"0.5 0 translate"
        ])

        start_column = 0
        for group in self.strand_array:
            self.draw_group(start_column, group)
            start_column += len(group)

    def draw_group(self, start_column, group):
        # Draw the strands straight for the first row
        for i, strand in enumerate(group):
            x = start_column + i
            color = PALETTE[strand % PALETTE_SIZE]
            self.add_lines([
                "gsave",
                f"{x} 0 translate",
                f"{color} straight1",
                "grestore"
            ])

        num_rows = self.grid_height - 1

        # Progressively swap strands and add draw the result
        shuffle_gen = odd_even_shuffle(group, num_rows, self.swap_chance)
        for i, commands in enumerate(shuffle_gen):
            y = i + 1
            for (command, *args) in commands:
                if command == STRAIGHT1:
                    x, strand = args
                    x += start_column
                    color = PALETTE[strand % PALETTE_SIZE]
                    self.add_lines([
                        "gsave",
                        f"{x} {y} translate",
                        f"{color} straight1",
                        "grestore"
                    ])
                elif command == STRAIGHT2:
                    x, strand1, strand2 = args
                    x += start_column
                    left_color = PALETTE[strand1 % PALETTE_SIZE]
                    right_color = PALETTE[strand2 % PALETTE_SIZE]
                    self.add_lines([
                        "gsave",
                        f"{x} {y} translate",
                        f"{right_color} {left_color} straight2",
                        "grestore"
                    ])
                elif command == CROSS:
                    x, strand1, strand2 = args
                    x += start_column
                    left_color = PALETTE[strand1 % PALETTE_SIZE]
                    right_color = PALETTE[strand2 % PALETTE_SIZE]
                    if x % 2 == 0:
                        self.add_lines([
                            "gsave",
                            f"{x} {y} translate",
                            f"{left_color} {right_color} left_over_right",
                            "grestore"
                        ])
                    else:
                        self.add_lines([
                            "gsave",
                            f"{x} {y} translate",
                            f"{right_color} {left_color} right_over_left",
                            "grestore"
                        ])
