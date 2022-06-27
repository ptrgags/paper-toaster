from postscriptlib.vec2 import Vec2

class Rectangle:
    def __init__(self, x, y, w, h):
        self.min = Vec2(x, y)
        self.max = Vec2(x + w, y + h)
    
    def __repr__(self):
        x = self.min.x
        y = self.min.y
        w = self.width
        h = self.height
        return f"Rectangle({x}, {y}, {w}, {h})"

    @property
    def width(self):
        return self.max.x - self.min.x
    
    @property
    def height(self):
        return self.max.y - self.min.y

    def add_point(self, point):
        x = point.x
        y = point.y

        if x < self.min.x:
            self.min.x = x
        if x > self.max.x:
            self.max.x = x
        
        if y < self.min.y:
            self.min.y = y
        if y > self.max.y:
            self.max.y = y
