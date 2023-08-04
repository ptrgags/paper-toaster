import random

from postscriptlib import receipts
from postscriptlib.path import Path
from postscriptlib.vec2 import Vec2

def make_grid(n):
    # blank nxn grid, all at height 1
    grid = [[1] * n for i in range(n)]

    # fill in the bottom row and leftmost column, either keeping the same value
    # or increasing by 1-2 more
    for i in range(1, n):
        last_row = n - 1
        increase = random.choice([0, 1, 2])
        grid[last_row][i] = grid[last_row][i - 1] + increase

        row = (n - 1) - i
        increase = random.choice([0, 1, 2])
        grid[row][0] = grid[row + 1][0] + increase

    # For the rest of the grid, take the max of the 2 neighbors and add the
    # increase
    for i in range(1, n):
        row = (n - 1) - i
        for col in range(1, n):
            left_neighbor = grid[row][col - 1]
            bottom_neighbor = grid[row + 1][col]
            increase = random.choice([0, 1, 2])
            grid[row][col] = max(left_neighbor, bottom_neighbor) + increase
    
    return grid

def grid_max(grid):
    return max(max(row) for row in grid)

def back_to_front(grid):
    rows = len(grid)
    cols = len(grid[0])

    # iterate diagonally starting in the top row
    for i in range(cols):
        col = (cols - 1) - i
        row = 0
        while row < rows and col < cols:
            height = grid[row][col]
            yield (Vec2(col, (rows - 1) - row), height)
            col += 1
            row += 1
    
    # iterate diagonally, this time starting in the leftmost column
    for i in range(1, rows):
        row = i
        col = 0
        while row < rows and col < cols:
            height = grid[row][col]
            yield (Vec2(col, (rows - 1) - row), height)
            col += 1
            row += 1
        

class IsoGrid(receipts.Receipt):
    ARTWORK_ID = 'iso_grid'

    def setup(self):
        n = 6
        self.grid = make_grid(n)

        # dimensions of the grid
        self.grid_rows = n
        self.grid_columns = n
        self.grid_height = grid_max(self.grid)

        # in isometric projection, how many tiles will be needed in the
        # horizontal and vertical direction of the page. Each tile is a diamond
        # that fits in a 4x2 box, but the bounding box overlaps with neighboring
        # tiles
        self.tile_rows = self.grid_rows + self.grid_columns + self.grid_height * self.num_cards
        self.tile_columns = 2 * (self.grid_rows + self.grid_columns)

        # compute the width of each tile so it just fits horizontally
        self.tile_size = self.width / self.tile_columns

        # basis vectors in isometric projection are pointing on diagonals in
        # page coordinates
        self.iso_x = Vec2(2 * self.tile_size, self.tile_size)
        self.iso_y = Vec2(-2 * self.tile_size, self.tile_size)
        self.iso_z = Vec2(0, self.tile_size * self.num_cards)

        # Since we're looking at the grid from the bottom-right corner, the
        # bottom left corner is shifted to the bottom
        self.iso_origin = Vec2(2 * self.grid_rows * self.tile_size, 0)
        
    def draw_tile(self, tile_coords, height):
        top_color = 0.8
        front_color = 0.5
        right_color = 0.2

        bottom_corner = self.iso_origin + tile_coords.x * self.iso_x + tile_coords.y * self.iso_y
        top_corner = bottom_corner + height * self.iso_z

        top_face = Path()
        top_face.rpolygon(top_corner, [
            self.iso_x,
            self.iso_y,
            -self.iso_x,
            -self.iso_y
        ])
        self.add_path(top_face)
        self.add_lines([f"{top_color} setgray fill"])

        right_face = Path()
        right_face.rpolygon(bottom_corner, [
            self.iso_x,
            height * self.iso_z,
            -self.iso_x,
            -height * self.iso_z
        ])
        self.add_path(right_face)
        self.add_lines([f"{right_color} setgray fill"])

        front_face = Path()
        front_face.rpolygon(bottom_corner, [
            height * self.iso_z,
            self.iso_y,
            -height * self.iso_z,
            -self.iso_y
        ])
        self.add_path(front_face)
        self.add_lines([f"{front_color} setgray fill"])


    def draw(self):
        self.fill_page()
        
        for (corner, height) in back_to_front(self.grid):
            self.draw_tile(corner, height)