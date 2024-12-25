#!/usr/bin/env python3

import re
import sys
from functools import reduce
from typing import Generator

MULTIPLY_REGEX = re.compile(r"mul\((\d+),(\d+)\)")


def read_multiply(text: str) -> Generator[tuple[int, int], None, None]:
    current_index = 0
    while current_index < len(text):
        matches = MULTIPLY_REGEX.match(text, current_index)
        if matches is not None:
            left, right = matches.group(1, 2)
            yield int(left), int(right)

        current_index += 1


def compute_sum_of_mul(line: str) -> int:
    return reduce(lambda a, b: a + b, (a * b for a, b in list(read_multiply(line))), 0)


def main() -> None:
    input_text = sys.stdin.read()
    sum_of_mul = compute_sum_of_mul(input_text)

    print(sum_of_mul)


if __name__ == "__main__":
    main()
