#!/usr/bin/env python3

import math
import sys
from collections.abc import Iterable


def calculate_next(number: int) -> int:
    number ^= number * 64
    number %= 16777216
    number ^= math.floor(number / 32)
    number %= 16777216
    number ^= number * 2048
    number %= 16777216
    return number


def calculate_number(number: int, iteration_count: int) -> int:
    for _ in range(iteration_count):
        number = calculate_next(number)

    return number


def sum_iterations(numbers: Iterable[int], iteration_count: int) -> int:
    return sum(calculate_number(number, iteration_count) for number in numbers)


def parse_prices(lines: Iterable[str]) -> Iterable[int]:
    for line in lines:
        yield int(line.strip())


def main() -> None:
    lines = sys.stdin.readlines()
    prices = parse_prices(lines)

    print(sum_iterations(prices, 2000))


if __name__ == "__main__":
    main()
