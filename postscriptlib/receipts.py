import subprocess

def run_program(args):
    result = subprocess.run(args, capture_output=True, shell=True)
    if result.stdout:
        print("stdout ------------")
        lines = result.stdout.split(b"\n")
        for line in lines:
            print(line.decode("utf-8"))
    
    if result.stderr:
        print("stdout ------------")
        lines = result.stderr.split(b"\n")
        for line in lines:
            print(line.decode("utf-8"))

class Receipt:
    # PostScript uses 72 points per inch
    PPI = 72

    @classmethod
    def add_subparser(cls, subparsers):
        """
        For each receipt, override this method
        and add a subparser. Additional arguments
        can be added as desired.
        """
        subparser = subparsers.add_parser(cls.ARTWORK_ID)
        cls.add_arguments(subparser)
        subparser.set_defaults(receipt_class=cls)

    @classmethod
    def add_arguments(cls, subparser):
        """
        Each artwork can optionally add arguments by
        overriding this method
        """
        pass

    def __init__(self, args):
        self.args = args
        
        # configure the page layout
        self.num_cards = args.num_cards
        w = args.page_width * self.PPI
        h = self.num_cards * args.page_height * self.PPI
        if args.landscape:
            w, h = h, w
        self.width = w
        self.height = h
        
        self.postscript_lines = []
        self.add_preamble()
    
    def add_preamble(self):
        self.postscript_lines.extend([
            "%!",
            f"<< /PageSize [{self.width} {self.height}] >> setpagedevice",
        ])
    
    def add_path(self, path):
        self.postscript_lines.extend(path.to_postscript())

    def stroke(self):
        self.postscript_lines.append("stroke")

    def fill(self):
        self.postscript_lines.append("fill")
    
    def even_odd_fill(self):
        self.postscript_lines.append("eofill")
    
    def add_lines(self, lines):
        self.postscript_lines.extend(lines)

    def rectstroke(self, x, y, w, h):
        self.postscript_lines.append(f"{x} {y} {w} {h} rectstroke")

    def rectfill(self, x, y, w, h):
        self.postscript_lines.append(f"{x} {y} {w} {h} rectfill")

    def outline_page(self):
        self.rectstroke(0, 0, self.width, self.height)
    
    def fill_page(self):
        self.rectfill(0, 0, self.width, self.height)

    def define_function(self, name, lines):
        self.postscript_lines.append(f"/{name} {{")
        for line in lines:
            self.postscript_lines.append(f"  {line}")
        self.postscript_lines.append(f"}} def")
    
    def set_font(self, font_name, size_points):
        self.postscript_lines.extend([
            f"/{font_name} findfont",
            f"{size_points} scalefont",
            "setfont"
        ])

    def draw_text(self, position, text):
        self.postscript_lines.extend([
            f"{position.x} {position.y} moveto",
            f"({text}) show"
        ])

    def setup(self):
        pass
    
    def draw(self):
        pass

    def print(self, artwork_name):
        """
        "print" to a PostScript file,
        and also generate some post-processed versions
        """
        postscript_file = f"output/{artwork_name}.ps"
        pdf_file = f"output/{artwork_name}.pdf"
        thumbnail_file = f"output/{artwork_name}_thumbnail.png"
        web_file = f"output/{artwork_name}_web.png"
        print_file = f"output/{artwork_name}_print.png"

        with open(postscript_file, "w") as f:
            for line in self.postscript_lines:
                f.write(f"{line}\n")
            f.write("showpage")
        
        # The following requires GhostScript to work!
            
        # Export a PDF file 
        print(f"Exporting PDF: {pdf_file}")
        run_program(['ps2pdf', postscript_file])

        # Export thumbnail image for 
        # for a single ATC, this is 250x350 px
        print(f"Exporting thumbnail (100 DPI): {thumbnail_file}")
        run_program([
            'gswin64c',
            '-o', thumbnail_file,
            '-sDEVICE=png16m', 
            "-r100", 
            postscript_file
        ])

        # Export image for my website
        # for a single ATC, this is 500x700 px
        print(f"Exporting web image (200 DPI): {thumbnail_file}")
        run_program([
            'gswin64c',
            '-o', web_file,
            '-sDEVICE=png16m', 
            "-r200", 
            postscript_file
        ])

        # If I ever want to print the image with a printing service, 300 DPI is
        # usually a good target resolution. For a single ATC this is 750x1050 px
        print(f"Exporting image for printing (300 DPI): {print_file}")
        run_program([
            'gswin64c',
            '-o', print_file,
            '-sDEVICE=png16m', 
            "-r300", 
            postscript_file
        ])