import math

# Postscript points-per-inch
PPI = 72.0

# Art trading card size in inches
ATC_WIDTH_PTS = 2.5 * PPI
ATC_HEIGHT_PTS = 3.5 * PPI

CENTER_X = ATC_WIDTH_PTS / 2
# A little bit above the center
CENTER_Y = 9 * ATC_HEIGHT_PTS / 16
CENTER = (CENTER_X, CENTER_Y)

# Divide the ouptut into concentric rings of this thickness
RADIUS_STEP = CENTER_X / 4

def polyline(f, origin, positions):
    (ox, oy) = origin
    f.write("newpath\n")
    f.write(f"0 0 moveto\n")
    for i, (x, y) in enumerate(positions):
        if i == 0:
            f.write(f"{x} {y} moveto\n")
        else:
            f.write(f"{x} {y} lineto\n")
    f.write("closepath\n")

def operator(amp, freq):
    def wave(t, phase):
        return amp * math.sin(2 * math.pi * freq * t - phase)
    return wave

# organ-like: just a simple addition of frequencies
def organ(op1, op2, op3):
    def wave(t, phase):
        t *= 4
        return op1(t, phase) + op2(t, phase) + op3(t, phase)
    return wave

# both op2 and op3 modulate op1 in parallel
def parallel_modulators(op1, op2, op3):
    def wave(t, phase):
        return op1(t, op2(t, phase) + op3(t, phase))
    return wave

# op3 modulates both op1 and op2
def parallel_carriers(op1, op2, op3):
    def wave(t, phase):
        mod = op3(t, phase)
        return op1(t, mod) + op2(t, mod)
    return wave

def circle(t):
    angle = 2 * math.pi * t
    return (math.cos(angle), math.sin(angle))

# wrap the FM wave around a circle inside the annulus with
# the given inner/outer radii
def fm_ring(wave, inner_radius, outer_radius, num_samples):
    results = [None] * num_samples
    for i in range(num_samples):
        t = i / num_samples
        mid_radius = (inner_radius + outer_radius) / 2.0
        amp = (outer_radius - inner_radius) / 2.0
        radius = (mid_radius + amp * wave(t, 0.0))
        (x, y) = circle(t)
        results[i] = (radius * x, radius * y)
    return results

def make_rings(f):
    PADDING = 0.1 * RADIUS_STEP
    R1 = RADIUS_STEP
    R2 = 2 * RADIUS_STEP
    R3 = 3 * RADIUS_STEP
    R4 = 4 * RADIUS_STEP

    # op2 -\
    #       --> op1
    # op3 -/
    op1 = operator(1.0, 1.0)
    op2 = operator(2, 2.0)
    op3 = operator(10, 3.0)
    ring1 = parallel_modulators(op1, op2, op3)

    # op4
    # op5
    # op6
    # in parallel
    op4 = operator(0.5, 1.0)
    op5 = operator(0.25, 10.0)
    op6 = operator(0.25, 7.0)
    ring2 = organ(op4, op5, op6)

    #       /--> op7
    # op9 --
    #       \--> op8
    op7 = operator(0.75, 0.5)
    op8 = operator(0.25, 2.0)
    op9 = operator(15.0, 5.0)
    ring3 = parallel_carriers(op7, op8, op9)

    f.write("gsave\n")
    (ox, oy) = CENTER
    f.write(f"{ox} {oy} translate\n")

    points = fm_ring(ring1, R1 + PADDING, R2 - PADDING, 1000)
    polyline(f, CENTER, points)
    f.write("stroke\n")

    points = fm_ring(ring2, R2 + PADDING, R3 - PADDING, 1000)
    polyline(f, CENTER, points)
    f.write("stroke\n")

    points = fm_ring(ring3, R3 + PADDING, R4 - PADDING, 1500)
    polyline(f, CENTER, points)
    f.write("stroke\n")

    f.write("grestore\n")

def main():
    with open("output/fm_ring.ps", 'w') as f:
        f.write("%!\n")
        f.write(f"<< /PageSize [{ATC_WIDTH_PTS} {ATC_HEIGHT_PTS}] >> setpagedevice\n")

        make_rings(f)
        
        # Draw a box around the ATC
        f.write("newpath\n")
        f.write(f"0 0 moveto\n")
        f.write(f"{ATC_WIDTH_PTS} 0 rlineto\n")
        f.write(f"0 {ATC_HEIGHT_PTS} rlineto\n")
        f.write(f"{ATC_WIDTH_PTS} neg 0 rlineto\n")
        f.write(f"0 {ATC_HEIGHT_PTS} neg rlineto\n")
        f.write("stroke\n")

        f.write("showpage\n")


if __name__ == "__main__":
    main()