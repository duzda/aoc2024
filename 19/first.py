#!/usr/bin/env python3

import sys
from collections.abc import Iterable
from functools import cache


def parse_input_towels(line: str) -> list[str]:
    return [towel.strip() for towel in line.split(",")]


def parse_wanted_towels(lines: Iterable[str]) -> list[str]:
    return [towel.strip() for towel in lines]


def is_possible(towels: Iterable[str], pattern: str, current_pattern: str = "") -> bool:
    @cache
    def is_possible_util(pattern: str, current_pattern: str) -> bool:
        if current_pattern == pattern:
            return True

        if not pattern.startswith(current_pattern) or len(current_pattern) > len(
            pattern
        ):
            return False

        for t in towels:
            if is_possible_util(pattern, current_pattern + t):
                return True

        return False

    return is_possible_util(pattern, current_pattern)


def count_possible(towels: Iterable[str], patterns: Iterable[str]) -> int:
    count = 0
    for pattern in patterns:
        if is_possible(towels, pattern):
            count += 1

    return count


def main() -> None:
    lines = sys.stdin.readlines()
    towels = parse_input_towels(lines[0])
    required_patterns = parse_wanted_towels(lines[2:])

    print(count_possible(towels, required_patterns))


if __name__ == "__main__":
    main()
