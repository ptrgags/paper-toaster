class Path:
    def __init__(self):
        self.lines = []
    
    def line(self, start, end):
        self.lines.append(f"{start.x} {start.y} moveto")
        self.lines.append(f"{end.x} {end.y} lineto")

    def rect(self, x, y, w, h):
        self.lines.append(f"{x} {y} moveto")
        self.lines.append(f"{w} 0 rlineto")
        self.lines.append(f"0 {h} rlineto")
        self.lines.append(f"{-w} 0 rlineto")
        self.lines.append(f"0 {-h} rlineto")
    
    def circle(self, center, radius):
        # the arc command annoyingly draws a line from the currengt point
        # so it needs to be closed immediately to draw a circle :/
        # furthermore you need to fill immediately. I need to find a better
        # way to do this...
        self.lines.append(f"newpath {center.x} {center.y} {radius} 0 360 arc closepath fill")

    def polygon(self, vertices):
        for i, vertex in enumerate(vertices):
            if i == 0:
                self.lines.append(f"{vertex.x} {vertex.y} moveto")
            else:
                self.lines.append(f"{vertex.x} {vertex.y} lineto")
        last_vertex = vertices[-1]
        self.lines.append(f"{last_vertex.x} {last_vertex.y} lineto")
    
    def rpolygon(self, origin, displacements):
        self.lines.append(f"{origin.x} {origin.y} moveto")
        for offset in displacements:
            self.lines.append(f"{offset.x} {offset.y} rlineto")

    def close(self):
        self.lines.append("closepath")

    def to_postscript(self):
        return ["newpath"] + self.lines
