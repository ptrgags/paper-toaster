# Postscript points-per-inch
PPI = 72.0

# Art trading card size in inches
ATC_WIDTH_PTS = 2.5 * PPI
ATC_HEIGHT_PTS = 3.5 * PPI

# how many quarter inch squares fit on the
# art trading card
WIDTH_SQUARES = 10
HEIGHT_SQUARES = 14

SQUARE_SIZE = 0.25 * PPI

def main():
    with open("output/grid.ps", 'w') as f:
        f.write("%!\n")
        f.write(f"<< /PageSize [{ATC_WIDTH_PTS} {ATC_HEIGHT_PTS}] >> setpagedevice\n")

        f.write("newpath\n")
        for x in range(WIDTH_SQUARES + 1):
            f.write(f"{x * SQUARE_SIZE} 0 moveto\n")
            f.write(f"0 {ATC_HEIGHT_PTS} rlineto \n")
        for y in range(HEIGHT_SQUARES + 1):
            f.write(f"0 {y * SQUARE_SIZE} moveto\n")
            f.write(f"{ATC_WIDTH_PTS} 0 rlineto \n")
        f.write("stroke\n")

        f.write("showpage\n")


if __name__ == "__main__":
    main()