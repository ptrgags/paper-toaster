import math

# Postscript points-per-inch
PPI = 72.0

# Art trading card size in inches
ATC_WIDTH_PTS = 2.5 * PPI
ATC_HEIGHT_PTS = 3.5 * PPI

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

def hexagon(f, x, y):
    f.write(f"{x:.4f} {y:.4f} moveto\n")
    for (bx, by) in BASIS:
        f.write(f"{bx:.4f} {by:.4f} rlineto\n")

# how many quarter inch squares fit on the
# art trading card
WIDTH_SQUARES = 10
HEIGHT_SQUARES = 14

SQUARE_SIZE = 0.25 * PPI

def main():
    with open("output/hex_grid.ps", 'w') as f:
        f.write("%!\n")
        f.write(f"<< /PageSize [{ATC_WIDTH_PTS} {ATC_HEIGHT_PTS}] >> setpagedevice\n")

        f.write("newpath\n")

        (t1x, t1y) = T1
        (t2x, t2y) = T2
        X_START = -7
        X_END = 4
        Y_START = 0
        Y_END = 11
        for i in range(X_START, X_END):
            for j in range(Y_START, Y_END):
                x = i * t1x + j * t2x
                y = i * t1y + j * t2y

                # expand the grid
                x *= 1.2
                y *= 1.2

                hexagon(f, x, y)
        
        f.write(f"0 0 moveto\n")
        f.write(f"{ATC_WIDTH_PTS} 0 rlineto\n")
        f.write(f"0 {ATC_HEIGHT_PTS} rlineto\n")
        f.write(f"{ATC_WIDTH_PTS} neg 0 rlineto\n")
        f.write(f"0 {ATC_HEIGHT_PTS} neg rlineto\n")
        f.write("stroke\n")

        f.write("showpage\n")


if __name__ == "__main__":
    main()