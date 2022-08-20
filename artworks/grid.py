from postscriptlib import receipts, path

class Grid(receipts.Receipt):
    ARTWORK_ID = 'grid'
    
    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            '-s',
            '--square-size',
            type=float,
            default=0.25,
            help="Size of a grid square in inches. Defaults to 1/4 inch"
        )

    def setup(self):
        square_size = self.args.square_size * self.PPI
        self.grid_width = int(self.width / square_size)
        self.grid_height = int(self.height / square_size)
        self.square_size = square_size
    
    def draw(self):
        grid = path.Path()
        for i in range(self.grid_width + 1):
            x = i * self.square_size
            grid.line(x, 0, x, self.height)
        
        for i in range(self.grid_height + 1):
            y = i * self.square_size
            grid.line(0, y, self.width, y)
        
        self.add_path(grid)
        self.stroke()