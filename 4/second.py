#!/usr/bin/env python3

NEEDLE = "MAS"


def parse_input() -> list[str]:
    rows: list[str] = []

    try:
        while (line := input()) is not None:
            rows.append(line)
    except EOFError:
        pass

    return rows


def compute_cross_mas(text: list[str]) -> int:
    count = 0
    for i in range(len(text) - 2):
        for j in range(len(text[0]) - 2):
            diagonal_string = text[i][j] + text[i + 1][j + 1] + text[i + 2][j + 2]
            diagonal_string_inverse = (
                text[i][j + 2] + text[i + 1][j + 1] + text[i + 2][j]
            )

            if (diagonal_string == NEEDLE or diagonal_string[::-1] == NEEDLE) and (
                diagonal_string_inverse == NEEDLE
                or diagonal_string_inverse[::-1] == NEEDLE
            ):
                count += 1

    return count


def main() -> None:
    text = parse_input()
    xmas_count = compute_cross_mas(text)

    print(xmas_count)


if __name__ == "__main__":
    main()
