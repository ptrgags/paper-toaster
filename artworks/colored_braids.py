import enum
import random

from postscriptlib import receipts

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

PALETTE = PALETTE_STRIPES
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

def odd_even_sort(array):
    sort_pass = 0
    is_sorted = False
    n = len(array)
    while not is_sorted:
        is_sorted = True
        row_commands = []
        first_index = sort_pass % 2

        if first_index == 1:
            row_commands.append((STRAIGHT1, 0, array[0]))

        for i in range(first_index, n, 2):
            if i + 1 == n:
                row_commands.append((STRAIGHT1, i, array[i]))
            elif array[i] > array[i + 1]:
                row_commands.append((CROSS, i, array[i], array[i + 1]))
                array[i], array[i + 1] = array[i + 1], array[i]
                is_sorted = False
            else:
                row_commands.append((STRAIGHT2, i, array[i], array[i + 1]))
        yield row_commands
        sort_pass += 1

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

        num_strands = self.grid_width
        self.groups = self.args.groups or [num_strands]
        self.strand_array = make_groups(self.groups, num_strands)

    def draw(self):
        bg_color = 0 if self.invert_colors else 1
        thin = 2.0 / self.square_size
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