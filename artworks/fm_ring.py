import math

from postscriptlib import receipts, path

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

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

class Receipt(receipts.Receipt):
    def setup(self):
        if self.num_cards > 1:
            raise ValueError("fm_ring only supports 1 card")

        cx = self.width / 2
        # A little bit above the center
        cy = 9 * self.height / 16
        self.radius_step = cx / 4
        self.center = (cx, cy)
    
    def draw(self):
        self.make_rings()

        border = path.Path()
        border.rect(0, 0, self.width, self.height)
        self.add_path(border)
        self.stroke()
    
    def make_rings(self):
        PADDING = 0.1 * self.radius_step
        R1 = self.radius_step
        R2 = 2 * self.radius_step
        R3 = 3 * self.radius_step
        R4 = 4 * self.radius_step

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

        (ox, oy) = self.center
        self.add_lines([
            "gsave",
            f"{ox:.4f} {oy:.4f} translate"
        ])


        ring_path = path.Path()
        points = fm_ring(ring1, R1 + PADDING, R2 - PADDING, 1000)
        ring_path.polygon(points)
        self.add_path(ring_path)
        self.stroke()

        ring_path = path.Path()
        points = fm_ring(ring2, R2 + PADDING, R3 - PADDING, 1000)
        ring_path.polygon(points)
        self.add_path(ring_path)
        self.stroke()

        ring_path = path.Path()
        points = fm_ring(ring3, R3 + PADDING, R4 - PADDING, 1500)
        ring_path.polygon(points)
        self.add_path(ring_path)
        self.stroke()

        self.add_lines([
            "grestore"
        ])