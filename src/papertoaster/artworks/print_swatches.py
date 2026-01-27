import os

from papertoaster import receipts


class PrintSwatches(receipts.Receipt):
    ARTWORK_ID = 'print_swatches'

    def draw(self):
        self.add_lines([
            "0 1.0 1.0 setrgbcolor",
            "0 0 72 72 rectfill",
            "0 1.0 1.0 setrgbcolor",
            "72 72 0 0 rectfill",
            "showpage",
            "0 1.0 1.0 setrgbcolor",
            "0 0 72 72 rectfill",
            "0 1.0 1.0 setrgbcolor",
            "72 72 0 0 rectfill",
            "showpage",
        ])

    def print(self, work_dir: str, artwork_name: str):
        postscript_file = os.path.join(work_dir, f"{artwork_name}.ps")
        with open(postscript_file, "w") as f:
            for line in self.postscript_lines:
                f.write(f"{line}\n")
