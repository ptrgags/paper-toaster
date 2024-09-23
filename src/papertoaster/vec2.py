import math


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2(x, y)

    def __mul__(self, other):
        x = self.x * other.x
        y = self.y * other.y
        return Vec2(x, y)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __repr__(self):
        return f'Vec2({self.x, self.y})'

    def __rmul__(self, scalar):
        """
        Scalar multiplication. Scalar goes on the left
        """
        x = self.x * scalar
        y = self.y * scalar
        return Vec2(x, y)

    def __truediv__(self, other):
        x = self.x / other.x
        y = self.y / other.y
        return Vec2(x, y)

    def __abs__(self):
        x = self.x
        y = self.y
        return math.sqrt(x * x + y * y)

    def normalize(self):
        r = abs(self)
        return 1.0 / r * self

    def rot90(self):
        return Vec2(-self.y, self.x)

    @classmethod
    def direction_vec(cls, angle_radians):
        """
        Get a unit vector at the given angle in radians
        """
        x = math.cos(angle_radians)
        y = math.sin(angle_radians)
        return cls(x, y)
