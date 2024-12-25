#!/usr/bin/env python3

import sys
from collections import defaultdict

YEAR = 2024


def string_to_stones(line: str) -> dict[str, int]:
    stones: dict[str, int] = defaultdict(int)
    for stone in line.split():
        stones[stone] += 1

    return stones


def strip_leading_zeros(string: str) -> str:
    stripped = string.lstrip("0")
    return "0" if len(stripped) == 0 else stripped


def apply_rules(stones: dict[str, int]) -> dict[str, int]:
    new_stones: dict[str, int] = defaultdict(int)
    for stone, count in stones.items():
        if stone == "0":
            new_stones["1"] += count

        elif len(stone) % 2 == 0:
            new_stones[stone[: len(stone) // 2]] += count
            new_stones[strip_leading_zeros(stone[len(stone) // 2 :])] += count

        else:
            new_stones[str(int(stone) * YEAR)] += count

    return new_stones


def main() -> None:
    input_stones = sys.stdin.read().strip()
    stones = string_to_stones(input_stones)
    for _ in range(75):
        stones = apply_rules(stones)

    print(sum(count for count in stones.values()))


if __name__ == "__main__":
    main()
