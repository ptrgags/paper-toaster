from postscriptlib import receipts
from postscriptlib.path import Path

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

BITS = 15

class LinearFeedbackShiftRegister(receipts.Receipt):
    """
    Create a linear-feedback shift register like on the original Gameboy's noise
    channel, but instead of making audio, let's visualize it like an automaton

    See https://gbdev.gg8.se/wiki/articles/Gameboy_sound_hardware#Noise_Channel
    for a description of how this works.
    """
    ARTWORK_ID = "lfsr"

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            "-w",
            "--width_mode",
            action="store_true",
            help="If true, feedback is written to both bits 6 and 14. If false, it is only written to bit 14"
        )
        subparser.add_argument(
            "-f",
            "--frequency",
            type=int,
            default=1,
            help="how many times to advance the LFSR every frame"
        )
    
    def setup(self):
        self.grid_width = BITS
        self.square_size = self.width / BITS
        self.grid_height = int(self.height / self.square_size)

        # start out with all bits set to 1
        self.shift_register = (1 << BITS) - 1

    def advance(self):
        tap0 = self.shift_register & 1
        tap1 = (self.shift_register >> 1) & 1
        feedback = tap0 ^ tap1

        self.shift_register >>= 1
        if self.args.width_mode:
            self.shift_register |= (feedback << 14) | (feedback << 6)
        else:
            self.shift_register |= feedback << 14
    
    def draw_current_row(self, grid, i):
        y = i * self.square_size
        for j in range(BITS):
            bit_index = (BITS - 1) - j
            val = (self.shift_register >> bit_index) & 1

            if val == 1:
                x = j * self.square_size
                grid.rect(x, y, self.square_size, self.square_size)
    
    def draw(self):
        grid = Path()

        for i in range(self.grid_height):
            self.draw_current_row(grid, i)
            for i in range(self.args.frequency):
                self.advance()
            print(bin(self.shift_register))
        
        self.add_path(grid)
        self.fill()