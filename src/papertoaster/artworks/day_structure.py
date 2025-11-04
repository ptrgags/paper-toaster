from papertoaster import path
from papertoaster.receipts import Receipt
from papertoaster.vec2 import Vec2

ROW_HEIGHT = 0.25 * Receipt.PPI


class DayStructure(Receipt):
    ARTWORK_ID = 'day_structure'

    def setup(self):
        pass

    def draw_schedule(self, lines: path.Path, start_y):
        # Outline half card
        lines.rect(0, start_y, self.width, self.height / 2)

        # Schedule outline
        lines.rect(ROW_HEIGHT, ROW_HEIGHT + start_y,
                   2.0 * Receipt.PPI, Receipt.PPI)

        # horizontal lines dividing the schedule into 4 rows,
        # each representing 4 hours for 16 waking hours total
        for i in range(3):
            y = 0.5 + i * 0.25
            lines.line(Vec2(ROW_HEIGHT, y * Receipt.PPI + start_y),
                       Vec2(2.25 * Receipt.PPI, y * Receipt.PPI + start_y))

        # ticks halfway across the schedule
        # denoting 2 hour marks
        for i in range(4):
            y_top = 2 * ROW_HEIGHT + i * ROW_HEIGHT
            y_bottom = y_top - 0.5 * ROW_HEIGHT
            lines.line(Vec2(self.width / 2, y_top + start_y),
                       Vec2(self.width / 2, y_bottom + start_y))

        # ticks 1/4 and 3/4 across the schedule
        # denoting 2 hour marks
        x_quarter = self.width / 2 - 0.5 * Receipt.PPI
        x_3_quarters = self.width / 2 + 0.5 * Receipt.PPI
        for i in range(4):
            y_top = 2 * ROW_HEIGHT + i * ROW_HEIGHT + start_y
            y_bottom = y_top - 0.25 * ROW_HEIGHT
            print(x_quarter, x_3_quarters)
            lines.line(Vec2(x_quarter, y_top),
                       Vec2(x_quarter, y_bottom))
            lines.line(Vec2(x_3_quarters, y_top),
                       Vec2(x_3_quarters, y_bottom))

        # Line at the top for date and other context
        lines.line(Vec2(0.25 * Receipt.PPI, 1.5 * Receipt.PPI + start_y),
                   Vec2(2.25 * Receipt.PPI, 1.5 * Receipt.PPI + start_y))

    def draw(self):
        lines = path.Path()

        # draw two schedules, each a half-card
        self.draw_schedule(lines, 0)
        self.draw_schedule(lines, self.height / 2)

        self.add_path(lines)
        self.stroke()
