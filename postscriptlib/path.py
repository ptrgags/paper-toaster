class Path:
    def __init__(self):
        self.lines = []
    
    def line(self, x1, y1, x2, y2):
        self.lines.append(f"{x1:.4f} {y1:.4f} moveto")
        self.lines.append(f"{x2:.4f} {y2:.4f} lineto")
    
    def rect(self, x, y, w, h):
        self.lines.append(f"{x:.4f} {y:.4f} moveto")
        self.lines.append(f"{w:.4f} 0 rlineto")
        self.lines.append(f"0 {h:.4f} rlineto")
        self.lines.append(f"{-w:.4f} 0 rlineto")
        self.lines.append(f"0 {-h:.4f} rlineto")

    def polygon(self, vertices):
        for i, (x, y) in enumerate(vertices):
            if i == 0:
                self.lines.append(f"{x:.4f} {y:.4f} moveto")
            else:
                self.lines.append(f"{x:.4f} {y:.4f} lineto")
        (x, y) = vertices[-1]
        self.lines.append(f"{x:.4f} {y:.4f} lineto")
    
    def rpolygon(self, origin, displacements):
        (ox, oy) = origin
        self.lines.append(f"{ox:.4f} {oy:.4f} moveto")
        for (x, y) in displacements:
            self.lines.append(f"{x:.4f} {y:.4f} rlineto")

    def close(self):
        self.lines.append("closepath")

    def to_postscript(self):
        return ["newpath"] + self.lines
