import os

from papertoaster import receipts
from papertoaster.vec2 import Vec2

COLOR_STEPS = 16


class PrintSwatches(receipts.Receipt):
    ARTWORK_ID = 'print_swatches'

    def setup(self):
        self.square_size = 2.5 * self.PPI / (COLOR_STEPS + 1)

    def draw_page(self, position: Vec2, page_index: int):
        red = page_index / (COLOR_STEPS - 1)

        self.add_lines([
            "gsave",
            f"{position.x} {position.y} translate",
            # stroke the page outline
            "0 setgray",
            f"0 0 {2.5 * self.PPI} {3.5 * self.PPI} rectstroke"
        ])

        self.set_font("Courier-Bold", 8)
        self.draw_text(Vec2(2.5/2 * self.PPI, 2.5 * self.PPI + 3),
                       f"R: {page_index * 0x11:02x}")

        for i in range(16):
            self.draw_text(Vec2((i+1) * self.square_size, 3),
                           f"{i * 0x11:02x}")
            self.draw_text(Vec2(0, (i+1) * self.square_size + 3),
                           f"{i * 0x11:02x}")

        for i in range(16):
            y = (i + 1) * self.square_size
            green = i / (COLOR_STEPS - 1)
            for j in range(16):
                x = (j + 1) * self.square_size
                blue = j / (COLOR_STEPS - 1)
                self.add_lines([
                    f"{red} {green} {blue} setrgbcolor",
                    f"{x} {y} {self.square_size} {self.square_size} rectfill",
                ])

        self.add_lines([
            "grestore"
        ])

    def draw(self):
        for i in range(16):
            position = Vec2(0, 0)
            self.draw_page(position, i)
            self.add_lines(["showpage"])

    def print(self, work_dir: str, artwork_name: str):
        postscript_file = os.path.join(work_dir, f"{artwork_name}.ps")
        with open(postscript_file, "w") as f:
            for line in self.postscript_lines:
                f.write(f"{line}\n")
