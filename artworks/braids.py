import random

from postscriptlib import receipts

class Braids(receipts.Receipt):
    ARTWORK_ID = 'braids'
    
    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            '-s',
            '--square-size',
            type=float,
            default=0.25,
            help="Size of a grid square in inches. Defaults to 1/4 inch"
        )
        subparser.add_argument(
            '-i',
            '--invert-colors',
            action="store_true",
            help="If set, use an inverted color scheme"
        )

    def setup(self):
        square_size = self.args.square_size * self.PPI
        self.grid_width = int(self.width / square_size)
        self.grid_height = int(self.height / square_size)
        self.square_size = square_size
        self.invert_colors = self.args.invert_colors
    
    def draw(self):
        thin = 2.0 / self.square_size
        thick = 3 * thin

        fg_color = 1 if self.invert_colors else 0
        bg_color = 0 if self.invert_colors else 1

        self.define_function("cross_under", [
            "newpath",
            "0 0 moveto",
            "0 0.5 1 0.5 1 1 curveto",
            f"{fg_color} setgray",
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
            f"{fg_color} setgray",
            "stroke",
        ])

        self.define_function("cross_over", [
            "newpath",
            "0 1 moveto",
            "0 0.5 1 0.5 1 0 curveto",
            f"{fg_color} setgray",
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
            f"{fg_color} setgray",
            "stroke",
        ])

        self.define_function("no_crossing", [
            "newpath",
            "0 0 moveto",
            "0 1 lineto",
            "1 0 moveto",
            "1 1 lineto",
            f"{fg_color} setgray",
            f"{thin} setlinewidth",
            "stroke",
        ])

        # Draw the background.
        self.add_lines([
            f"{bg_color} setgray",
            f"0 0 {self.width} {self.height} rectfill",
            f"{self.square_size} {self.square_size} scale",
        ])

        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if (i + j) % 2 == 1:
                    continue

                # Alternate the crossings else it's easy to end up with
                # strands crossing over many columns.
                crossing = "cross_over" if j % 2 == 0 else 'cross_under'

                # Not every tile needs to have a crossing
                tile = random.choice(["no_crossing", crossing, crossing])

                # Don't draw a crossing at the top and bottom most rows
                if i == 0 or i == self.grid_height - 1:
                    tile = 'no_crossing'

                self.add_lines([
                    "gsave",
                    f"{j} {i} translate",
                    tile,
                    "grestore"
                ])
            
            # On the left and right edges, every other row skips
            # the first string, so draw it by making a slightly off-page
            # tile
            if i % 2 == 1:
                self.add_lines([
                    "gsave",
                    f"-1 {i} translate",
                    "no_crossing",
                    "grestore"
                ])
            else:
                self.add_lines([
                    "gsave",
                    f"{self.grid_width} {i} translate",
                    "no_crossing",
                    "grestore"
                ])