import argparse


from artworks import ARTWORKS

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-cards",
        type=int,
        default=1,
        help="How many trading cards tall (3.5 inches) each page of the receipt should be"
    )
    parser.add_argument(
        "--page-width",
        type=float,
        default=2.5, # width of an art trading card
        help="Width of a single page in inches"
    )
    parser.add_argument(
        "--page-height",
        type=float,
        default=3.5, # height of an art trading card
        help="Height of a single page in inches"
    )
    parser.add_argument(
        "--landscape",
        action="store_true",
        help="If set, the pages will use landscape rather than portrait orientation"
    )
    subparsers = parser.add_subparsers(dest='artwork')

    # Each receipt will add a subparser, so the overall usage
    # becomes main.py [global_options] ARTWORK [artwork_options]
    for artwork in ARTWORKS:
        artwork.add_subparser(subparsers)

    args = parser.parse_args()

    # Receipt.add_subparser stores the class in the args
    try:
        ReceiptClass = args.receipt_class
        receipt = ReceiptClass(args)
        receipt.setup()
        receipt.draw()
        receipt.print(args.artwork)
    except AttributeError as error:
        print(error)
        # No subcommand was specified, so receipt_class
        # is not defined. Print a help message instead
        parser.print_help()