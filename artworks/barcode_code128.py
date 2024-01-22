import argparse

from postscriptlib import receipts
from postscriptlib.barcodes.code128 import Code128
from postscriptlib.path import Path

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

class Barcode128(receipts.Receipt):
    ARTWORK_ID = 'barcode128'

    @classmethod
    def add_arguments(cls, subparser):
        subparser.add_argument(
            'text',
            help="printable ASCII text to encode as a Code 128 barcode"
        )

    def setup(self):
        self.text = self.args.text

        module_width = 1
        module_height = PPI
        self.barcode = Code128(module_width, module_height)
    
    def draw(self):
        defines = self.barcode.make_definitions()
        barcode_lines = self.barcode.draw(0, 0, self.width, self.height, self.text)

        self.postscript_lines.extend(defines + barcode_lines)

        border = Path()
        border.rect(0, 0, self.width, self.height)
        self.add_path(border)
        self.stroke()