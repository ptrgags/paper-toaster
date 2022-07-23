import math

from postscriptlib import receipts, path

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

SIDE_LENGTH = 0.25 * PPI
L_COS_60 = SIDE_LENGTH * math.cos(math.pi / 3)
L_SIN_60 = SIDE_LENGTH * math.sin(math.pi / 3)

def add_vecs(a, b):
    (ax, ay) = a
    (bx, by) = b
    return (ax + bx, ay + by)

BASIS = [
    (SIDE_LENGTH, 0.0),
    (L_COS_60, L_SIN_60),
    (-L_COS_60, L_SIN_60),
    (-SIDE_LENGTH, 0.0),
    (-L_COS_60, -L_SIN_60),
    (L_COS_60, -L_SIN_60)
]

# Translation vectors between grid cells
T1 = add_vecs(BASIS[0], BASIS[5])
T2 = add_vecs(BASIS[0], BASIS[1])

EXPAND_FACTOR = 1.2
X_START = -7
X_END = 4
Y_START = 0
Y_END = 11

class HexGrid(receipts.Receipt):
    ARTWORK_ID = 'hex_grid'

    def setup(self):
        # The grid vectors aren't aligned with the 
        # receipt so have to expand the grid quite a bit :/
        self.x_start = self.num_cards * X_START
        self.x_end = X_END
        self.y_start = Y_START
        self.y_end = self.num_cards * Y_END
    
    def draw_hexagon(self, x, y):
        hex = path.Path()
        hex.rpolygon((x, y), BASIS)
        self.add_path(hex)
        self.stroke()

    def draw_hexagons(self):
        (t1x, t1y) = T1
        (t2x, t2y) = T2
        
        for i in range(self.x_start, self.x_end):
            for j in range(self.y_start, self.y_end):
                x = i * t1x + j * t2x
                y = i * t1y + j * t2y

                # expand the grid
                x *= EXPAND_FACTOR
                y *= EXPAND_FACTOR

                self.draw_hexagon(x, y)

    def draw(self):
        self.draw_hexagons()

        border = path.Path()
        border.rect(0, 0, self.width, self.height)
        self.add_path(border)
        self.stroke()