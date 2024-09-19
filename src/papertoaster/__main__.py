#!/usr/bin/env python3
import os
import argparse
import random
import sys
import time
from typing import Optional

from papertoaster.artworks import ARTWORKS


def init_seed(seed: Optional[int]) -> int:
    """
    Set the random seed if --seed was specified, or choose a seed based on
    the current time in seconds. Returns the seed value that was used.
    """
    if seed is not None:
        random.seed(seed)
        return seed

    time_seed = int(time.time() % 10000)
    random.seed(time_seed)
    return time_seed


def get_work_dir() -> str:
    """
    Get the value of the environment variable WORK_DIR, and make sure it's a
    directory. This method may exit the program with an error message if not
    specified or invalid.
    """
    output_dir = os.environ.get('WORK_DIR')
    if output_dir is None:
        print("The environment variable WORK_DIR must be set to a directory where output files will be generated.")
        sys.exit(1)

    directory_exists = os.path.isdir(output_dir)
    if not directory_exists and output_dir == '/workdir':
        print("/workdir not found. Make sure to set a bind mount for this when running Docker!")
        sys.exit(1)

    if not directory_exists:
        print(f"{output_dir} not a directory. Make sure the environment variable WORK_DIR is set to a valid directory!")
        sys.exit(1)

    return output_dir


def make_receipt(args: argparse.Namespace, output_dir: str):
    # Receipt.add_subparser stores the class in the args
    try:
        ReceiptClass = args.receipt_class
        receipt = ReceiptClass(args)
        receipt.setup()
        receipt.draw()
        receipt.print(output_dir, args.artwork)
    except AttributeError as error:
        print(error)
        # No subcommand was specified, so receipt_class
        # is not defined. Print a help message instead
        parser.print_help()


if __name__ == "__main__":
    # Common options that will be added to every subcommand.
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--num-cards",
        type=int,
        default=1,
        help="How many trading cards tall (3.5 inches) each page of the receipt should be"
    )
    common_parser.add_argument(
        "--page-width",
        type=float,
        default=2.5,  # width of an art trading card
        help="Width of a single page in inches"
    )
    common_parser.add_argument(
        "--page-height",
        type=float,
        default=3.5,  # height of an art trading card
        help="Height of a single page in inches"
    )
    common_parser.add_argument(
        "--landscape",
        action="store_true",
        help="If set, the pages will use landscape rather than portrait orientation"
    )
    common_parser.add_argument(
        "--seed",
        type=int,
        help="If provided, random.seed() will be called so random generation will be reproducible. If not provided, the seed will be chosen automatically."
    )

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='artwork')

    # Each receipt will add a subparser, so the overall usage
    # becomes python -m papertoaster COMMAND [args]
    for artwork in ARTWORKS:
        artwork.add_subparser(subparsers, common_parser)

    args = parser.parse_args()

    seed = init_seed(args.seed)
    print(f"Using random seed {seed}")

    work_dir = get_work_dir()
    make_receipt(args, work_dir)
