#!/usr/bin/env python3

NEEDLE = "XMAS"


def parse_input() -> list[str]:
    rows: list[str] = []

    try:
        while (line := input()) is not None:
            rows.append(line)
    except EOFError:
        pass

    return rows


def compute_diagonal_xmas(text: list[str]) -> int:
    count = 0
    for i in range(len(text) - 3):
        for j in range(len(text[0]) - 3):
            diagonal_string = (
                text[i][j]
                + text[i + 1][j + 1]
                + text[i + 2][j + 2]
                + text[i + 3][j + 3]
            )
            if diagonal_string == NEEDLE:
                count += 1
            if diagonal_string[::-1] == NEEDLE:
                count += 1

    for i in range(len(text) - 3):
        for j in range(len(text) - 1, 2, -1):
            diagonal_string = (
                text[i][j]
                + text[i + 1][j - 1]
                + text[i + 2][j - 2]
                + text[i + 3][j - 3]
            )
            if diagonal_string == NEEDLE:
                count += 1
            if diagonal_string[::-1] == NEEDLE:
                count += 1

    return count


def compute_xmas(text: list[str]) -> int:
    return sum(row.count(NEEDLE) for row in text)


def compute_all_xmas(text: list[str]) -> int:
    column_text = ["".join([row[i] for row in text]) for i in range(len(text[0]))]
    return sum(
        [
            compute_xmas(text[:]),
            compute_xmas([row[::-1] for row in text]),
            compute_xmas(column_text),
            compute_xmas([col[::-1] for col in column_text]),
            compute_diagonal_xmas(text),
        ]
    )


def main() -> None:
    text = parse_input()
    xmas_count = compute_all_xmas(text)

    print(xmas_count)


if __name__ == "__main__":
    main()
