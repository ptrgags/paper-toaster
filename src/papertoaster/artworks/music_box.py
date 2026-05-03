import math

from papertoaster import receipts
from papertoaster.path import Path
from papertoaster.vec2 import Vec2

# 72 points/inch * 1 inch/25.4 mm = points per mm
PPI = receipts.Receipt.PPI
POINTS_PER_MM = PPI / 25.4

# Each paper music box strip is 4cm wide. However, when I tried it, the paper
# was a little too narrow and would slip. So add a bit of padding
PADDING = 2 * POINTS_PER_MM
STRIP_WIDTH = 40 * POINTS_PER_MM + PADDING

# There's a margin of 6mm above/below the staff, plus the extra padding
# mentioned above
STAFF_MARGIN = 6 * POINTS_PER_MM + 0.5 * PADDING
# The 15 lines for notes are spaced 2mm apart
LINE_SPACING = 2 * POINTS_PER_MM
# The grid lines for note durations are spaced 4mm apart, twice the staff spacing.
GRID_SPACING = 4 * POINTS_PER_MM

NOTE_COUNT = 15

STAFF_LINE_INDICES = [4, 6, 8, 10, 12]
STAFF_LINE_THICKNESS = 3


class MusicBoxTemplate(receipts.Receipt):
    ARTWORK_ID = 'music_box'

    def setup(self):
        self.whole_strips: int = math.floor(self.width / STRIP_WIDTH)
        self.page_margin = 0.5 * (self.width - self.whole_strips * STRIP_WIDTH)

        self.grid_line_count: int = math.ceil(self.height / GRID_SPACING)

    def draw(self):
        for i in range(self.whole_strips):
            self.draw_music_box_strip(i)

    def draw_music_box_strip(self, strip_index: int):
        path = Path()
        offset_strip = self.page_margin + strip_index * STRIP_WIDTH

        # Draw the outline for the paper strip
        path.rect(offset_strip, 0, STRIP_WIDTH, self.height)

        staff_offset = offset_strip + STAFF_MARGIN

        # draw lines down the length the strip, one per note
        for i in range(NOTE_COUNT):
            path.line(Vec2(staff_offset + i * LINE_SPACING, 0),
                      Vec2(staff_offset + i * LINE_SPACING, self.height))

        # Draw lines across the staff every 4mm to make a grid to help with
        # timing
        for i in range(self.grid_line_count):
            path.line(Vec2(staff_offset, i * GRID_SPACING),
                      Vec2(staff_offset + (NOTE_COUNT - 1) * LINE_SPACING, i * GRID_SPACING))
        self.add_path(path)
        self.stroke()

        for i in STAFF_LINE_INDICES:
            self.rectfill(staff_offset + i * LINE_SPACING - 0.5 * STAFF_LINE_THICKNESS, 0,
                          STAFF_LINE_THICKNESS, self.height)
