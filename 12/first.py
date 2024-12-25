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


def get_area_and_perimeter(
    position: Position, garden_map: GardenMap
) -> tuple[int, int, set[Position]]:
    needle = garden_map[position.y][position.x]

    queue: deque[Position] = deque()
    queue.append(position)

    visited_positions: set[Position] = {position}

    perimeter = 0

    while queue:
        position = queue.pop()

        for position in Position.get_nearby_positions(position):
            if position in visited_positions:
                continue

            if (
                not Position.is_valid(position, garden_map)
                or garden_map[position.y][position.x] != needle
            ):
                perimeter += 1
                continue

            queue.append(position)
            visited_positions.add(position)

    return len(visited_positions), perimeter, visited_positions


def calculate_price(garden_map: GardenMap) -> int:
    price = 0
    visited_positions: set[Position] = set()

    for y in range(len(garden_map)):
        for x in range(len(garden_map[0])):
            if Position(x, y) in visited_positions:
                continue

            area, perimeter, currently_visited = get_area_and_perimeter(
                Position(x, y), garden_map
            )
            price += area * perimeter
            visited_positions.update(currently_visited)

    return price


def main() -> None:
    garden_map = parse_input()

    print(calculate_price(garden_map))


if __name__ == "__main__":
    main()
