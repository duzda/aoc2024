#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

type Position = Vector

type Empty = Literal["."]
type Wall = Literal["#"]
type Map = list[list[Empty | Wall]]


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)


WIDTH = 71
HEIGHT = 71
BLOCK_COUNT = 1024


def parse_blocks(lines: Iterable[str]) -> set[Position]:
    positions: set[Position] = set()

    for line in lines:
        x, y = line.split(",")
        positions.add(Vector(int(x), int(y)))

    return positions


def create_map(x: int, y: int, blocks: set[Position]) -> Map:
    blocked_map: Map = []

    for i in range(y):
        blocked_map.append([])

        for j in range(x):
            if Vector(j, i) in blocks:
                blocked_map[-1].append("#")
            else:
                blocked_map[-1].append(".")

    return blocked_map


def get_valid_nearby_positions(block_map: Map, position: Position) -> list[Position]:
    new_positions = []

    for new_position in [
        position + v for v in [Vector(0, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0)]
    ]:
        if (
            new_position.x >= 0
            and new_position.x < len(block_map[0])
            and new_position.y >= 0
            and new_position.y < len(block_map)
            and block_map[new_position.y][new_position.x] != "#"
        ):
            new_positions.append(new_position)

    return new_positions


def find_exit(
    block_map: Map,
    position: Position = Vector(0, 0),
    end: Position = Vector(WIDTH - 1, HEIGHT - 1),
) -> int:
    visited: set[Position] = set()

    to_be_visited: deque[tuple[Position, int]] = deque()
    to_be_visited.append((position, 0))

    while len(to_be_visited) != 0:
        current_position, distance = to_be_visited.popleft()

        if current_position in visited:
            continue

        visited.add(current_position)

        if current_position == end:
            return distance

        to_be_visited.extend(
            [
                (p, distance + 1)
                for p in get_valid_nearby_positions(block_map, current_position)
            ]
        )

    return -1


def main() -> None:
    lines = sys.stdin.readlines()
    blocks = parse_blocks(lines[:BLOCK_COUNT])
    block_map = create_map(WIDTH, HEIGHT, blocks)

    print(find_exit(block_map))


if __name__ == "__main__":
    main()
