class Receipt:
    # PostScript uses 72 points per inch
    PPI = 72

    # I like to print things as art trading cards, which
    # are 2.5x3.5 inches.
    ATC_WIDTH_INCHES = 2.5
    ATC_HEIGHT_INCHES = 3.5
    ATC_WIDTH_POINTS = ATC_WIDTH_INCHES * PPI
    ATC_HEIGHT_POINTS = ATC_HEIGHT_INCHES * PPI

    def __init__(self, num_cards, receipt_args):
        self.num_cards = num_cards
        self.args = receipt_args
        self.width = self.ATC_WIDTH_POINTS
        self.height = num_cards * self.ATC_HEIGHT_POINTS
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
    
    def set_font(self, font_name, size_points):
        self.postscript_lines.extend([
            f"/{font_name} findfont",
            f"{size_points} scalefont",
            "setfont"
        ])

    def draw_text(self, x, y, text):
        self.postscript_lines.extend([
            f"{x} {y} moveto",
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