import argparse
import random
from pathlib import Path
from typing import Callable
from urllib import request

from cowsay import cowsay, get_random_cow, read_dot_cow

f = open(Path(__file__).parent / "my_cow.cow")
MY_COW_FILE = read_dot_cow(f)
f.close()


def nonnegative_int(s: str) -> int:
    try:
        res = int(s)
        if res <= 0:
            raise TypeError
        return res
    except:
        raise argparse.ArgumentTypeError(
            "Параметр должен быть положительным целым числом."
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dictionary",
        type=str,
        help="Путь до файла в файловой системе либо корректный url.",
    )
    parser.add_argument(
        "length",
        nargs="?",
        default=5,
        type=nonnegative_int,
        help="Длина слов в игре",
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
    while s := input(f"{cowsay(message=prompt, cowfile=MY_COW_FILE)}\n>"):
        if valid is not None and s not in valid:
            print("Ваше слово некорректное, попробуйте другое")
            continue
        return s


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay(message=format_string.format(bulls, cows), cow=get_random_cow()))


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
    print("Количество попыток:", gameplay(ask, inform, words))


if __name__ == "__main__":
    main()
