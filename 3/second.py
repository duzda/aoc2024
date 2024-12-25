#!/usr/bin/env python3

import re
import sys
from functools import reduce
from typing import Generator

DO_REGEX = re.compile(r"do\(\)")
DONT_REGEX = re.compile(r"don't\(\)")
MULTIPLY_REGEX = re.compile(r"mul\((\d+),(\d+)\)")


def read_multiply(text: str) -> Generator[tuple[int, int], None, None]:
    current_index = 0
    skip = False
    while current_index < len(text):
        dont = DONT_REGEX.match(text, current_index)
        if dont is not None:
            skip = True

        do = DO_REGEX.match(text, current_index)
        if do is not None:
            skip = False

        matches = MULTIPLY_REGEX.match(text, current_index)
        if matches is not None and not skip:
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
