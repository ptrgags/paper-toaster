from hex_grid import ATC_HEIGHT_PTS, ATC_WIDTH_PTS


class Receipt:
    # PostScript uses 72 points per inch
    PPI = 72

    # I like to print things as art trading cards, which
    # are 2.5x3.5 inches.
    ATC_WIDTH_INCHES = 2.5
    ATC_HEIGHT_INCHES = 3.5
    ATC_WIDTH_PNTS = ATC_WIDTH_INCHES * PPI
    ATC_HEIGHT_PNTS = ATC_HEIGHT_INCHES * PPI

    def __init__(self, num_cards, receipt_args):
        self.num_cards = num_cards
        self.args = receipt_args
        self.width = ATC_WIDTH_PTS
        self.height = num_cards * ATC_HEIGHT_PTS
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