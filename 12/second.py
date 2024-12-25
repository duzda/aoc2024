#!/usr/bin/env python3

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

type GardenMap = list[list[str]]


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

    @staticmethod
    def is_valid(position: Position, garden_map: GardenMap) -> bool:
        return (
            position.x >= 0
            and position.x < len(garden_map[0])
            and position.y >= 0
            and position.y < len(garden_map)
        )

    @staticmethod
    def get_nearby_positions(position: Position) -> list[Position]:
        return [
            position + Position(0, 1),
            position - Position(0, 1),
            position + Position(1, 0),
            position - Position(1, 0),
        ]


def parse_input() -> GardenMap:
    current_map: GardenMap = []

    try:
        while (line := input()) is not None:
            current_map.append(list(line))
    except EOFError:
        pass

    return current_map


def get_side_count(position: Position, garden_map: GardenMap) -> int:
    corners: int = 0
    needle = garden_map[position.y][position.x]

    # https://www.reddit.com/r/adventofcode/comments/1hcsfaz/comment/m1r2g42
    adjacencies = [
        Position.is_valid(p, garden_map) and garden_map[p.y][p.x] == needle
        for p in (
            p + position
            for p in [
                Position(0, 1),
                Position(1, 1),
                Position(1, 0),
                Position(1, -1),
                Position(0, -1),
                Position(-1, -1),
                Position(-1, 0),
                Position(-1, 1),
            ]
        )
    ]

    for i in range(0, 8, 2):
        corners += 1 if not adjacencies[i] and not adjacencies[(i + 2) % 8] else 0
        corners += (
            1
            if adjacencies[i] and adjacencies[(i + 2) % 8] and not adjacencies[i + 1]
            else 0
        )

    return corners


def get_area_and_sides(
    position: Position, garden_map: GardenMap
) -> tuple[int, int, set[Position]]:
    needle = garden_map[position.y][position.x]

    queue: deque[Position] = deque()
    queue.append(position)

    visited_positions: set[Position] = {position}

    sides = 0

    while queue:
        position = queue.pop()

        sides += get_side_count(position, garden_map)

        for position in Position.get_nearby_positions(position):
            if position in visited_positions:
                continue

            if (
                not Position.is_valid(position, garden_map)
                or garden_map[position.y][position.x] != needle
            ):
                continue

            queue.append(position)
            visited_positions.add(position)

    return len(visited_positions), sides, visited_positions


def calculate_price(garden_map: GardenMap) -> int:
    price = 0
    visited_positions: set[Position] = set()

    for y in range(len(garden_map)):
        for x in range(len(garden_map[0])):
            if Position(x, y) in visited_positions:
                continue

            area, sides, currently_visited = get_area_and_sides(
                Position(x, y), garden_map
            )
            price += area * sides
            visited_positions.update(currently_visited)

    return price


def main() -> None:
    garden_map = parse_input()

    print(calculate_price(garden_map))


if __name__ == "__main__":
    main()
