#!/usr/bin/env python3

from typing import Literal

type Orientation = Literal["Up", "Right", "Down", "Left"]
type Map = list[list[str]]


def parse_input() -> Map:
    current_map: Map = []

    try:
        while (line := input()) is not None:
            current_map.append(list(line))
    except EOFError:
        pass

    return current_map


def find_guard(current_map: Map) -> tuple[int, int]:
    for y, line in enumerate(current_map):
        for x, c in enumerate(line):
            if c == "^":
                return x, y

    return -1, -1


def get_shifted_position(x: int, y: int, orientation: Orientation) -> tuple[int, int]:
    if orientation == "Up":
        return x, y - 1
    if orientation == "Right":
        return x + 1, y
    if orientation == "Down":
        return x, y + 1
    if orientation == "Left":
        return x - 1, y


def rotate_right(current_orientation: Orientation) -> Orientation:
    orientations: list[Orientation] = ["Up", "Right", "Down", "Left"]
    return orientations[(orientations.index(current_orientation) + 1) % 4]


def traverse_map(current_map: Map, default_orientation: Orientation = "Up") -> None:
    x, y = find_guard(current_map)
    orientation = default_orientation

    while True:
        new_x, new_y = get_shifted_position(x, y, orientation)
        current_map[y][x] = "X"
        if (
            new_x < 0
            or new_x >= len(current_map[0])
            or new_y < 0
            or new_y >= len(current_map)
        ):
            break

        if (
            current_map[new_y][new_x] == "X"
            or current_map[new_y][new_x] == "."
            or current_map[new_y][new_x] == "^"  # Probably useless
        ):
            x, y = new_x, new_y
        elif current_map[new_y][new_x] == "#":
            orientation = rotate_right(orientation)


def count_traversed(current_map: Map) -> int:
    return [c for line in current_map for c in line].count("X")


def main() -> None:
    current_map = parse_input()
    traverse_map(current_map)

    print(count_traversed(current_map))


if __name__ == "__main__":
    main()
