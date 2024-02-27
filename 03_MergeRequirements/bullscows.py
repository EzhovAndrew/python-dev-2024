import argparse
import random
from typing import Callable
from urllib import request


def nonnegative_int(s: str) -> int:
    try:
        res = int(s)
        if res <= 0:
            raise TypeError
        return res
    except:
        raise argparse.ArgumentTypeError("Parameter must be positive int number.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dictionary",
        type=str,
        help="Dictionary file name or valid url to download file",
    )
    parser.add_argument(
        "length",
        nargs="?",
        default=5,
        type=nonnegative_int,
        help="Length of secret words.",
    )
    return parser.parse_args()


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls = 0
    cows = set()
    sc_len = len(secret)
    for i, char in enumerate(guess):
        if i < sc_len and guess[i] == secret[i]:
            bulls += 1
            continue
        if char in secret and char not in cows:
            cows.add(char)
    return bulls, len(cows)


def gameplay(ask: Callable, inform: Callable, words: list[str]) -> int:
    secret = words[random.randint(0, len(words) - 1)]
    guess = None
    ask_counter = 0
    while guess != secret:
        guess = ask("Введите слово: ", words)
        inform("Быки: {}, Коровы: {}", *bullscows(guess, secret))
        ask_counter += 1
    return ask_counter


def ask(prompt: str, valid: list[str] = None) -> str:
    while s := input(prompt):
        if valid is not None and s not in valid:
            print("Your word is not valid, try another")
            continue
        return s


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def download_by_url(url: str) -> list[str]:
    with request.urlopen(url) as f:
        data = f.read().decode()
    return data.split()


def read_from_file(filepath: str) -> list[str]:
    with open(filepath, "r") as f:
        return f.read().split()


def main() -> None:
    args = parse_args()
    try:
        words = download_by_url(args.dictionary)
    except:
        words = read_from_file(args.dictionary)
    words = list(filter(lambda x: len(x) == args.length, words))
    print("Number of attempts:", gameplay(ask, inform, words))


if __name__ == "__main__":
    main()
