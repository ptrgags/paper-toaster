from postscriptlib import receipts, path
from postscriptlib.vec2 import Vec2

class ToDoList(receipts.Receipt):
    ARTWORK_ID = 'todo'
    
    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            '-s',
            '--row-size',
            type=float,
            default=0.25,
            help="Size of a row in inches (including padding). Defaults to 1/4 inch"
        )

    def setup(self):
        self.row_size = self.args.row_size * self.PPI
        self.row_count = int(self.height / self.row_size)
    
    def draw(self):
        lines = path.Path()

        square_size = self.row_size * 0.75
        padding = 0.05 * self.width
        
        self.add_lines(["0.5 setlinewidth"])

        for i in range(self.row_count):
            y = self.row_size * i
            self.rectstroke(padding, y, square_size, square_size)
            lines.line(Vec2(2 * padding + square_size, y), Vec2(self.width - padding, y))
        
        self.add_path(lines)
        self.stroke()