import argparse
import os


class Receipt:
    # PostScript uses 72 points per inch
    PPI = 72
    ARTWORK_ID = "<receipt>"

    @classmethod
    def add_subparser(cls, subparsers, common_parser: argparse.ArgumentParser):
        """
        For each receipt, override this method
        and add a subparser. Additional arguments
        can be added as desired.
        """
        subparser = subparsers.add_parser(
            cls.ARTWORK_ID, parents=[common_parser])
        cls.add_arguments(subparser)
        subparser.set_defaults(receipt_class=cls)

    @classmethod
    def add_arguments(cls, subparser):
        """
        Each artwork can optionally add arguments by
        overriding this method
        """
        pass

    def __init__(self, args):
        self.args = args

        # configure the page layout
        self.num_cards = args.num_cards
        w = args.page_width * self.PPI
        h = self.num_cards * args.page_height * self.PPI
        if args.landscape:
            w, h = h, w
        self.width = w
        self.height = h

        self.postscript_lines = []
        self.add_preamble()

    def add_preamble(self):
        self.postscript_lines.extend([
            "%!",
            f"<< /PageSize [{self.width} {self.height}] >> setpagedevice",
        ])

    def add_path(self, path):
        self.postscript_lines.extend(path.to_postscript())

    def stroke(self):
        self.postscript_lines.append("stroke")

    def fill(self):
        self.postscript_lines.append("fill")

    def even_odd_fill(self):
        self.postscript_lines.append("eofill")

    def add_lines(self, lines):
        self.postscript_lines.extend(lines)

    def rectstroke(self, x, y, w, h):
        self.postscript_lines.append(f"{x} {y} {w} {h} rectstroke")

    def rectfill(self, x, y, w, h):
        self.postscript_lines.append(f"{x} {y} {w} {h} rectfill")

    def outline_page(self):
        self.rectstroke(0, 0, self.width, self.height)

    def fill_page(self):
        self.rectfill(0, 0, self.width, self.height)

    def define_function(self, name, lines):
        self.postscript_lines.append(f"/{name} {{")
        for line in lines:
            self.postscript_lines.append(f"  {line}")
        self.postscript_lines.append(f"}} def")

    def set_font(self, font_name, size_points):
        self.postscript_lines.extend([
            f"/{font_name} findfont",
            f"{size_points} scalefont",
            "setfont"
        ])

    def draw_text(self, position, text):
        self.postscript_lines.extend([
            f"{position.x} {position.y} moveto",
            f"({text}) show"
        ])

    def setup(self):
        pass

    def draw(self):
        pass

    def print(self, work_dir, artwork_name):
        """
        "print" to a PostScript file,
        and also generate some post-processed versions
        """
        postscript_file = os.path.join(work_dir, f"{artwork_name}.ps")
        with open(postscript_file, "w") as f:
            for line in self.postscript_lines:
                f.write(f"{line}\n")
            f.write("showpage")
