from postscriptlib import receipts, path

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

SQUARE_SIZE = 0.25 * PPI

class Receipt(receipts.Receipt):
    def setup(self):
        self.grid_width = int(self.width / SQUARE_SIZE)
        self.grid_height = int(self.height / SQUARE_SIZE)
    
    def draw(self):
        grid = path.Path()
        for i in range(self.grid_width + 1):
            x = i * SQUARE_SIZE
            grid.line(x, 0, x, self.height)
        
        for i in range(self.grid_height + 1):
            y = i * SQUARE_SIZE
            grid.line(0, y, self.width, y)
        
        self.add_path(grid)
        self.stroke()