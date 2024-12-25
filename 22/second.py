#!/usr/bin/env python3

import math
import sys
from collections import Counter
from collections.abc import Iterable


def calculate_next(number: int) -> int:
    number ^= number * 64
    number %= 16777216
    number ^= math.floor(number / 32)
    number %= 16777216
    number ^= number * 2048
    number %= 16777216
    return number


def sum_iterations(numbers: Iterable[int], iteration_count: int) -> int:
    sequences: Counter[tuple[int, ...]] = Counter()

    for number in numbers:
        changes: list[int] = []
        last = number % 10

        seen: set[tuple[int, ...]] = set()

        for _ in range(iteration_count):
            number = calculate_next(number)
            price = number % 10
            diff = price - last
            last = price

            changes.append(diff)
            if len(changes) >= 4:
                sequence = tuple(changes[-4:])
                if sequence not in seen:
                    seen.add(sequence)
                    sequences[sequence] += price

    return sequences.most_common(1)[0][1]


def parse_prices(lines: Iterable[str]) -> Iterable[int]:
    for line in lines:
        yield int(line.strip())


def main() -> None:
    lines = sys.stdin.readlines()
    prices = parse_prices(lines)

    print(sum_iterations(prices, 2000))


if __name__ == "__main__":
    main()
