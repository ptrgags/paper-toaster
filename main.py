import argparse
import importlib

ARTWORK_LIST = [
    "grid",
    "hex_grid",
    "fm_ring",
    "hitomezashi",
    "turtle_dance"
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("artwork", choices=ARTWORK_LIST)
    parser.add_argument(
        "--num-cards",
        type=int,
        default=1,
        help="How many trading cards tall (3.5 inches) the receipt should be"
    )
    parser.add_argument(
        "artwork_args",
        nargs="*",
        help="additional arguments if needed"
    )
    args = parser.parse_args()

    module = importlib.import_module(f"artworks.{args.artwork}")
    light_show = module.Receipt(args.num_cards, args.artwork_args)
    light_show.setup()
    light_show.draw()
    light_show.print(f"output/{args.artwork}.ps")