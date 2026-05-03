from papertoaster.artworks.barcode_code128 import Barcode128
from papertoaster.artworks.braids import Braids
from papertoaster.artworks.colored_braids import ColoredBraids
from papertoaster.artworks.edge_directions import EdgeDirectionTiling
from papertoaster.artworks.elementary_ca import ElementaryCA
from papertoaster.artworks.grid import Grid
from papertoaster.artworks.hex_grid import HexGrid
from papertoaster.artworks.hitomezashi import Hitomezashi
from papertoaster.artworks.iso_grid import IsoGrid
from papertoaster.artworks.print_swatches import PrintSwatches
from papertoaster.artworks.music_box import MusicBoxTemplate
from papertoaster.artworks.quiet_dice import QuietDice
from papertoaster.artworks.robot_walks import RobotWalks
from papertoaster.artworks.todo import ToDoList
from papertoaster.artworks.turtle_dance import TurtleDance
from papertoaster.receipts import Receipt

ARTWORKS: list[type[Receipt]] = [
    Barcode128,
    Braids,
    ColoredBraids,
    EdgeDirectionTiling,
    ElementaryCA,
    Grid,
    HexGrid,
    Hitomezashi,
    IsoGrid,
    MusicBoxTemplate,
    QuietDice,
    PrintSwatches,
    RobotWalks,
    ToDoList,
    TurtleDance
]
