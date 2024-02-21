import argparse
import sys

import cowsay

preset_flags = ["b", "d", "g", "p", "s", "t", "w", "y"]


def len_equal_2(s: str):
    """Force command line parameter have length of 2 characters."""
    if len(s) == 2:
        return s
    raise argparse.ArgumentTypeError("Value must have length 2 characters")


def make_preset(args: argparse.Namespace) -> str | None:
    """Make preset string of passed preset parameters."""
    result = "".join(key for key in preset_flags if getattr(args, key))
    if not result:
        result = None
    return result


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Implementation of cowsay program.")
    parser.add_argument(
        "-e",
        type=str,
        help=(
            "specify the option to select the appearance of the cow's eyes,"
            "in which case the first two characters of the argument string eye_string will be used"
        ),
    )
    parser.add_argument(
        "-f",
        type=str,
        default="default",
        help="specifies a particular cow picture file ('cowfile') to use",
    )
    parser.add_argument("-l", action="store_true", help="Lists all cow file names")
    parser.add_argument(
        "-n",
        action="store_true",
        help="Specifies, the given message will be word-wrapped or not.",
    )
    parser.add_argument(
        "-T",
        type=len_equal_2,
        help=(
            "The tongue is similarly configurable through -T and tongue_string;"
            "it must be two characters and does not appear by default."
        ),
    )
    parser.add_argument(
        "-W",
        type=int,
        default=40,
        help=(
            "Specifies roughly where the message should be wrapped."
            "The default is equivalent to -W 40 i.e. wrap words at or before the 40th column. "
        ),
    )
    parser.add_argument("-b", action="store_true", help="Initiates Borg mode")
    parser.add_argument("-d", action="store_true", help="Causes the cow to appear dead")
    parser.add_argument("-g", action="store_true", help="Invokes greedy mode")
    parser.add_argument(
        "-p",
        action="store_true",
        help="Causes a state of paranoia to come over the cow",
    )
    parser.add_argument(
        "-s", action="store_true", help="Makes the cow appear thoroughly stoned"
    )
    parser.add_argument("-t", action="store_true", help="Yields a tired cow")
    parser.add_argument(
        "-w",
        action="store_true",
        help="Is somewhat the opposite of -t, and initiates wired mode",
    )
    parser.add_argument(
        "-y", action="store_true", help="brings on the cow's youthful appearance"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.l:
        cowsay.list_cows()
        return
    message = sys.stdin.read()
    kwargs = {
        "message": message,
        "cow": args.f,
        "width": args.W,
        "wrap_text": args.n,
        "preset": make_preset(args),
    }
    if args.e:
        kwargs["eyes"] = args.e
    if args.T:
        kwargs["tongue"] = args.T
    print(cowsay.cowsay(**kwargs))


if __name__ == "__main__":
    main()
