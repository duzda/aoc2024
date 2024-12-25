#!/usr/bin/env python3


def parse_line(input: str) -> list[int]:
    numbers = input.split(" ")
    return [int(n) for n in numbers]


def parse_input_till_empty() -> list[list[int]]:
    levels = []

    try:
        while (line := input()) is not None:
            levels.append(parse_line(line))
    except EOFError:
        pass

    return levels


def _is_limited(numbers: list[int], low_limit: int, high_limit: int) -> bool:
    for i in range(len(numbers) - 1):
        diff = numbers[i] - numbers[i + 1]
        if not (diff >= low_limit and diff <= high_limit):
            return False

    return True


def is_limited(numbers: list[int], low_limit: int, high_limit: int) -> bool:
    if _is_limited(numbers, low_limit, high_limit):
        return True

    for i in range(len(numbers)):
        if _is_limited(
            [*numbers[:i], *numbers[i + 1 :]],
            low_limit,
            high_limit,
        ):
            return True

    return False


def is_safe(numbers: list[int]) -> bool:
    return is_limited(numbers, 1, 3) or is_limited(numbers, -3, -1)


def compute_safe(levels: list[list[int]]) -> int:
    return [is_safe(numbers) for numbers in levels].count(True)


def main() -> None:
    levels = parse_input_till_empty()
    safe = compute_safe(levels)

    print(safe)


if __name__ == "__main__":
    main()
