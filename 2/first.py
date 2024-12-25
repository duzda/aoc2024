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


def is_limited(numbers: list[int], low_limit: int, high_limit: int) -> bool:
    limited = True

    for i in range(len(numbers) - 1):
        diff = numbers[i] - numbers[i + 1]
        limited = limited and diff >= low_limit and diff <= high_limit

    return limited


def is_safe(numbers: list[int]) -> bool:
    if numbers[0] > numbers[1]:
        return is_limited(numbers, 1, 3)

    return is_limited(numbers, -3, -1)


def compute_safe(levels: list[list[int]]) -> int:
    safe: int = 0

    for numbers in levels:
        safe += 1 if is_safe(numbers) else 0

    return safe


def main() -> None:
    levels = parse_input_till_empty()
    safe = compute_safe(levels)

    print(safe)


if __name__ == "__main__":
    main()
