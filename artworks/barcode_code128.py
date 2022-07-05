import argparse

from postscriptlib import receipts
from postscriptlib.barcodes.code128 import Code128

# Postscript points-per-inch
PPI = receipts.Receipt.PPI

class Receipt(receipts.Receipt):
    def setup(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("text", help="printable ASCII text to encode as a Code 128 barcode")
        args = parser.parse_args(self.args)

        self.text = args.text

        module_width = 1
        module_height = PPI
        self.barcode = Code128(module_width, module_height)
    
    def draw(self):
        defines = self.barcode.make_definitions()
        barcode_lines = self.barcode.draw(0, 0, self.text)

        self.postscript_lines.extend(defines + barcode_lines)