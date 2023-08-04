class Receipt:
    # PostScript uses 72 points per inch
    PPI = 72

    # I like to print things as art trading cards, which
    # are 2.5x3.5 inches.
    ATC_WIDTH_INCHES = 2.5
    ATC_HEIGHT_INCHES = 3.5
    ATC_WIDTH_POINTS = ATC_WIDTH_INCHES * PPI
    ATC_HEIGHT_POINTS = ATC_HEIGHT_INCHES * PPI

    @classmethod
    def add_subparser(cls, subparsers):
        """
        For each receipt, override this method
        and add a subparser. Additional arguments
        can be added as desired.
        """
        subparser = subparsers.add_parser(cls.ARTWORK_ID)
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
        w = self.ATC_WIDTH_POINTS
        h = self.num_cards * self.ATC_HEIGHT_POINTS
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
    
    def set_line_width(self, width):
        self.postscript_lines.append(f"{width} setlinewidth")

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

    def print(self, fname):
        """
        "print" to a PostScript file
        """
        with open(fname, "w") as f:
            for line in self.postscript_lines:
                f.write(f"{line}\n")
            f.write("showpage")