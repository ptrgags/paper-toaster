class Path:
    def __init__(self):
        self.lines = []
    
    def line(self, x1, y1, x2, y2):
        self.lines.append(f"{x1:.4f} {y1:.4f} moveto")
        self.lines.append(f"{x2:.4f} {y2:.4f} lineto")

    def to_postscript(self):
        return ["newpath"] + self.lines
