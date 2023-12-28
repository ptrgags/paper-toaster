def remap(in_min, in_max, out_min, out_max, value):
    in_width = in_max - in_min
    out_width = out_max - out_min
    return out_width * (value - in_min) / in_width + out_min