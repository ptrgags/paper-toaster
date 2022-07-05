class Barcode:
    """
    Generic barcode rendering. Just provide the
    dimensions of each module and an array of 0s and 1s
    """
    def __init__(self, module_width, module_height):
        self.module_width = module_width
        self.module_height = module_height

    def make_definitions(self):
        return [
            "/bar {",
            "  /bar_y exch def",
            "  /bar_x exch def",
            "  bar_x bar_y moveto",
            f"  {self.module_width} 0 rlineto",
            f"  0 {self.module_height} rlineto",
            f"  {-self.module_width} 0 rlineto",
            f"  0 {-self.module_height} rlineto",
            "} def",
        ]

    def draw(self, start_x, start_y, bars):
        lines = ["newpath"]
        for i, digit in enumerate(bars):
            if digit == 1:
                x = start_x + i * self.module_width
                lines.append(f"{x} {start_y} bar")
        lines.append("closepath fill")
        return lines