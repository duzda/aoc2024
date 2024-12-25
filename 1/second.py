#!/usr/bin/env python3
from collections import Counter


def parse_line(input: str) -> tuple[int, int]:
    numbers = input.split("   ")
    return int(numbers[0]), int(numbers[1])


def parse_input_till_empty() -> tuple[list[int], list[int]]:
    l1: list[int] = []
    l2: list[int] = []

    try:
        while (line := input()) is not None:
            n1, n2 = parse_line(line)

            l1.append(n1)
            l2.append(n2)
    except EOFError:
        pass

    return l1, l2


def compute_similarities(l1: list[int], l2: list[int]) -> int:
    similarities: int = 0
    similarities_helper = Counter(l2)

    for number in l1:
        similarities += number * similarities_helper.get(number, 0)

    return similarities


def main() -> None:
    l1, l2 = parse_input_till_empty()
    similarities = compute_similarities(l1, l2)

    print(similarities)


if __name__ == "__main__":
    main()
