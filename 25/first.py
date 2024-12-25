#!/usr/bin/env python3

import sys
from collections.abc import Iterable

type Key = list[int]
type Pin = list[int]


KEY_SIZE = (5, 7)


def parse_map(lines: Iterable[str]) -> list[int]:
    sizes: list[int] = [0] * KEY_SIZE[0]

    for line in lines:
        for i, c in enumerate(line):
            if c == "#":
                sizes[i] += 1

    return sizes


def is_key(lines: list[str]) -> bool:
    return lines[0][0] == "#"


def parse_input(lines: list[str]) -> tuple[list[Key], list[Pin]]:
    current_map: list[str] = []

    keys: list[Key] = []
    pins: list[Pin] = []

    for i, line in enumerate(lines):
        if line == "\n" or i == len(lines) - 1:
            if is_key(current_map):
                keys.append(parse_map(current_map))
            else:
                pins.append(parse_map(current_map))

            current_map = []
        else:
            current_map.append(line.strip())

    return keys, pins


def fits(key: Key, pin: Pin) -> bool:
    for i in range(KEY_SIZE[0]):
        if key[i] + pin[i] > KEY_SIZE[1]:
            return False

    return True


def count_pairs(keys: list[Key], pins: list[Pin]) -> int:
    correct = 0
    for key in keys:
        for pin in pins:
            if fits(key, pin):
                correct += 1

    return correct


def main() -> None:
    lines = sys.stdin.readlines()
    keys, pins = parse_input(lines)

    print(count_pairs(keys, pins))


if __name__ == "__main__":
    main()
