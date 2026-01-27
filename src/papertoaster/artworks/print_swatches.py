import os

from papertoaster import receipts

COLOR_STEPS = 16


class PrintSwatches(receipts.Receipt):
    ARTWORK_ID = 'print_swatches'

    def setup(self):
        self.square_size = 2.5 * self.PPI / (COLOR_STEPS + 1)

    def draw_page(self, page_index: int):
        red = page_index / (COLOR_STEPS - 1)

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

        self.add_lines(["showpage"])

    def draw(self):
        for i in range(16):
            self.draw_page(i)

    def print(self, work_dir: str, artwork_name: str):
        postscript_file = os.path.join(work_dir, f"{artwork_name}.ps")
        with open(postscript_file, "w") as f:
            for line in self.postscript_lines:
                f.write(f"{line}\n")
