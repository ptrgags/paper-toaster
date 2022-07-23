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

    def stroke(self):
        self.postscript_lines.append("stroke")

    def fill(self):
        self.postscript_lines.append("fill")
    
    def add_lines(self, lines):
        self.postscript_lines.extend(lines)

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