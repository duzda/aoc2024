#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

type Map = list[list[str]]
type Antennas = dict[str, set[Position]]


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

    @staticmethod
    def is_valid(position: Position, antenna_map: Map) -> bool:
        return (
            position.x >= 0
            and position.x < len(antenna_map[0])
            and position.y >= 0
            and position.y < len(antenna_map)
        )


def parse_input() -> Map:
    antenna_map: Map = []

    try:
        while (line := input()) is not None:
            antenna_map.append(list(line))
    except EOFError:
        pass

    return antenna_map


def generate_antenna_dict(antenna_map: Map) -> Antennas:
    antennas: Antennas = defaultdict(set)
    for y, line in enumerate(antenna_map):
        for x, char in enumerate(line):
            if char == ".":
                continue

            antennas[char].add(Position(x, y))

    return antennas


def calculate_new_positions(a: Position, b: Position) -> list[Position]:
    diff = b - a
    return [a - diff, b + diff]


def get_unique_positions(antenna_map: Map, antennas: Antennas) -> set[Position]:
    positions: set[Position] = set()

    for antenna_positions in antennas.values():
        for antenna_a, antenna_b in combinations(antenna_positions, 2):
            for antinode in calculate_new_positions(antenna_a, antenna_b):
                if Position.is_valid(antinode, antenna_map):
                    positions.add(antinode)

    return positions


def main() -> None:
    antenna_map = parse_input()
    antennas = generate_antenna_dict(antenna_map)
    positions = get_unique_positions(antenna_map, antennas)

    print(len(positions))


if __name__ == "__main__":
    main()
