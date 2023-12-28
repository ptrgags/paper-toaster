from postscriptlib.barcodes.barcode import Barcode

QUIET_ZONE = [0] * 10

def to_digit_array(digit_str):
    return [int(c) for c in digit_str]

# Encode table from https://en.wikipedia.org/wiki/Code_128#Bar_code_widths
# I'm only using Subcode B for now, but keeping the rest around just in case
# since processing look-up tables is a chore
#
# The special characters aren't properly listed here but oh well, they're
# handled separately anyway 
DATA_CHARS = [
    # [Subcode A, Subcode B, Subcode C, bar pattern]
    [" ", " ", "00", "11011001100"],
    ["!", "!", "01", "11001101100"],
    ["\"", "\"", "02", "11001100110"],
    ["#", "#", "03", "10010011000"],
    ["$", "$", "04", "10010001100"],
    ["%", "%", "05", "10001001100"],
    ["&", "&", "06", "10011001000"],
    ["'", "'", "07", "10011000100"],
    ["(", "(", "08", "10001100100"],
    [")", ")", "09", "11001001000"],
    ["*", "*", "10", "11001000100"],
    ["+", "+", "11", "11000100100"],
    [",", ",", "12", "10110011100"],
    ["-", "-", "13", "10011011100"],
    [".", ".", "14", "10011001110"],
    ["/", "/", "15", "10111001100"],
    ["0", "0", "16", "10011101100"],
    ["1", "1", "17", "10011100110"],
    ["2", "2", "18", "11001110010"],
    ["3", "3", "19", "11001011100"],
    ["4", "4", "20", "11001001110"],
    ["5", "5", "21", "11011100100"],
    ["6", "6", "22", "11001110100"],
    ["7", "7", "23", "11101101110"],
    ["8", "8", "24", "11101001100"],
    ["9", "9", "25", "11100101100"],
    [":", ":", "26", "11100100110"],
    [";", ";", "27", "11101100100"],
    ["<", "<", "28", "11100110100"],
    ["=", "=", "29", "11100110010"],
    [">", ">", "30", "11011011000"],
    ["?", "?", "31", "11011000110"],
    ["@", "@", "32", "11000110110"],
    ["A", "A", "33", "10100011000"],
    ["B", "B", "34", "10001011000"],
    ["C", "C", "35", "10001000110"],
    ["D", "D", "36", "10110001000"],
    ["E", "E", "37", "10001101000"],
    ["F", "F", "38", "10001100010"],
    ["G", "G", "39", "11010001000"],
    ["H", "H", "40", "11000101000"],
    ["I", "I", "41", "11000100010"],
    ["J", "J", "42", "10110111000"],
    ["K", "K", "43", "10110001110"],
    ["L", "L", "44", "10001101110"],
    ["M", "M", "45", "10111011000"],
    ["N", "N", "46", "10111000110"],
    ["O", "O", "47", "10001110110"],
    ["P", "P", "48", "11101110110"],
    ["Q", "Q", "49", "11010001110"],
    ["R", "R", "50", "11000101110"],
    ["S", "S", "51", "11011101000"],
    ["T", "T", "52", "11011100010"],
    ["U", "U", "53", "11011101110"],
    ["V", "V", "54", "11101011000"],
    ["W", "W", "55", "11101000110"],
    ["X", "X", "56", "11100010110"],
    ["Y", "Y", "57", "11101101000"],
    ["Z", "Z", "58", "11101100010"],
    ["[", "[", "59", "11100011010"],
    ["\\", "\\", "60", "11101111010"],
    ["]", "]", "61", "11001000010"],
    ["^", "^", "62", "11110001010"],
    ["_", "_", "63", "10100110000"],
    ["NUL", "`", "64", "10100001100"],
    ["SOH", "a", "65", "10010110000"],
    ["STX", "b", "66", "10010000110"],
    ["ETX", "c", "67", "10000101100"],
    ["EOT", "d", "68", "10000100110"],
    ["ENQ", "e", "69", "10110010000"],
    ["ACK", "f", "70", "10110000100"],
    ["BEL", "g", "71", "10011010000"],
    ["BS", "h", "72", "10011000010"],
    ["HT", "i", "73", "10000110100"],
    ["LF", "j", "74", "10000110010"],
    ["VT", "k", "75", "11000010010"],
    ["FF", "l", "76", "11001010000"],
    ["CR", "m", "77", "11110111010"],
    ["SO", "n", "78", "11000010100"],
    ["SI", "o", "79", "10001111010"],
    ["DLE", "p", "80", "10100111100"],
    ["DC1", "q", "81", "10010111100"],
    ["DC2", "r", "82", "10010011110"],
    ["DC3", "s", "83", "10111100100"],
    ["DC4", "t", "84", "10011110100"],
    ["NAK", "u", "85", "10011110010"],
    ["SYN", "v", "86", "11110100100"],
    ["ETB", "w", "87", "11110010100"],
    ["CAN", "x", "88", "11110010010"],
    ["EM", "y", "89", "11011011110"],
    ["SUB", "z", "90", "11011110110"],
    ["ESC", "{", "91", "11110110110"],
    ["FS", "|", "92", "10101111000"],
    ["GS", "}", "93", "10100011110"],
    ["RS", "~", "94", "10001011110"],
    ["US", "DEL", "95", "10111101000"],
    ["FNC 3", "FNC 3", "96", "10111100010"],
    ["FNC 2", "FNC 2", "97", "11110101000"],
    ["Shift B", "Shift A", "98", "11110100010"],
    ["Code C", "Code C", "99", "10111011110"],
    ["Code B", "FNC 4", "Code B", "10111101110"],
    ["FNC 4", "Code A", "Code A", "11101011110"],
    ["FNC 1", "FNC 1", "FNC 1", "11110101110"],
]

# there are 103 data characters. This also serves as the
# modulo for computing the checksum
assert len(DATA_CHARS) == 103

def make_char_tables():
    a_table = {}
    b_table = {}
    c_table = {}
    for a_char, b_char, c_char, bar_pattern in DATA_CHARS:
        a_table[a_char] = to_digit_array(bar_pattern)
        b_table[b_char] = to_digit_array(bar_pattern)
        c_table[c_char] = to_digit_array(bar_pattern)

    return {
        "A": a_table,
        "B": b_table,
        "C": c_table
    }

DATA_SYMBOLS = make_char_tables()

DATA_VALUES = {
    b_char: i
    for i, (_, b_char, _, _) in enumerate(DATA_CHARS)
}

START_SYMBOLS = {
    "A": to_digit_array("11010000100"),
    "B": to_digit_array("11010010000"),
    "C": to_digit_array("11010011100")
}

START_SYMBOL_VALUES = {
    "A": 103,
    "B": 104,
    "C": 105
}

# I'm using the longer form of this which includes the "final bar"
STOP_SYMBOL = to_digit_array("1100011101011")

class Code128:
    def __init__(self, module_width, module_height):
        self.barcode = Barcode(module_width, module_height)

    def make_definitions(self):
        return self.barcode.make_definitions()

    def encode(self, text):
        """
        Encode text as a a Code B barcode. This is highly
        simplified, a true encoder can switch between A, B, and C
        subcodes and support some non-printable characters. See
        https://en.wikipedia.org/wiki/Code_128 for more details
        """
        bars = QUIET_ZONE + START_SYMBOLS["B"]
        symbols = DATA_SYMBOLS["B"]

        # start codes have a weight of 1
        checksum = START_SYMBOL_VALUES["B"]

        weight = 0
        for c in text:
            if c not in symbols:
                print(f"Unsupported character: {c}")
                continue

            # we already accounted for the start code.
            weight += 1
            bars += symbols[c]
            checksum += weight * DATA_VALUES[c]
        
        checksum %= len(DATA_CHARS)
        _, _, _, checksum_pattern = DATA_CHARS[checksum]
        bars += to_digit_array(checksum_pattern)

        bars += STOP_SYMBOL + QUIET_ZONE

        return bars


    def draw(self, start_x, start_y, text):
        bars = self.encode(text)
        print(bars)

        return self.barcode.draw(start_x, start_y, bars)
            
        

