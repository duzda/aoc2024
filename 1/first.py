#!/usr/bin/env python3


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


def compute_differences(l1: list[int], l2: list[int]) -> int:
    l1 = sorted(l1)
    l2 = sorted(l2)

    differences: int = 0

    for first, second in zip(l1, l2):
        differences += abs(first - second)

    return differences


def main() -> None:
    l1, l2 = parse_input_till_empty()
    differences = compute_differences(l1, l2)

    print(differences)


if __name__ == "__main__":
    main()
