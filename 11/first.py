#!/usr/bin/env python3

import sys

YEAR = 2024


def string_to_stones(line: str) -> list[int]:
    return [int(stone) for stone in line.split()]


def apply_rules(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)

        elif len(str(stone)) % 2 == 0:
            new_stones.append(int(str(stone)[: len(str(stone)) // 2]))
            new_stones.append(int(str(stone)[len(str(stone)) // 2 :]))

        else:
            new_stones.append(stone * YEAR)

    return new_stones


def main() -> None:
    input_stones = sys.stdin.read().strip()
    stones = string_to_stones(input_stones)
    for _ in range(25):
        stones = apply_rules(stones)

    print(len(stones))


if __name__ == "__main__":
    main()
