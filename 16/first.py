#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterable
from dataclasses import dataclass
from functools import total_ordering
from heapq import heappop, heappush
from typing import Literal

type Position = Vector

type Empty = Literal["."]
type Start = Literal["S"]
type End = Literal["E"]
type Wall = Literal["#"]
type Map = list[list[Empty | Start | End | Wall]]


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)


@total_ordering
class HeapQueueItem:
    position: Position
    direction: Vector
    price: int

    def __init__(
        self,
        position: Position,
        direction: Vector,
        price: int = 0,
    ):
        self.position = position
        self.direction = direction
        self.price = price

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HeapQueueItem):
            return False

        return self.price == other.price

    def __lt__(self, other: HeapQueueItem) -> bool:
        return self.price < other.price


PRICE_MOVE = 1
PRICE_ROTATE = 1000

DEFAULT_DIRECTION = Vector(1, 0)


def parse_map(lines: Iterable[str]) -> Map:
    return [list(line[:-1]) for line in lines]  # type: ignore[arg-type]


def rotate(current_direction: Vector, ccw: bool = False) -> Vector:
    direction = [Vector(0, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0)]
    return direction[
        direction.index(current_direction) + (-1 if ccw else 1) % len(direction)
    ]


def find_element(maze: Map, character: Start | End) -> Position:
    for i, row in enumerate(maze):
        for j, el in enumerate(row):
            if el == character:
                return Vector(j, i)

    return Vector(-1, -1)


def get_valid_next_moves(
    current_position: Position, maze: Map, visited: set[tuple[Position, Vector]]
) -> list[tuple[Position, Vector]]:
    moves: list[tuple[Position, Vector]] = []

    for m in [Vector(0, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0)]:
        p = current_position + m
        if (
            p.y >= 0
            and p.y < len(maze)
            and p.x >= 0
            and p.x < len(maze[0])
            and maze[p.y][p.x] != "#"
            and (p, m) not in visited
        ):
            moves.append((p, m))

    return moves


def get_rotation_count(current_direction: Vector, wanted_direction: Vector) -> int:
    if current_direction == wanted_direction:
        return 0
    if current_direction == -wanted_direction:
        return 2
    return 1


def find_cheapest_path(maze: Map, default_direction: Vector = DEFAULT_DIRECTION) -> int:
    priority_queue: list[HeapQueueItem] = []
    heappush(priority_queue, HeapQueueItem(find_element(maze, "S"), default_direction))

    lowest_price = sys.maxsize

    visited: set[tuple[Position, Vector]] = set()

    while len(priority_queue) > 0:
        item = heappop(priority_queue)

        visited.add((item.position, item.direction))

        if item.price >= lowest_price:
            continue

        if maze[item.position.y][item.position.x] == "E":
            lowest_price = item.price
            continue

        for position, direction in get_valid_next_moves(item.position, maze, visited):
            heappush(
                priority_queue,
                HeapQueueItem(
                    position,
                    direction,
                    item.price
                    + get_rotation_count(item.direction, direction) * PRICE_ROTATE
                    + PRICE_MOVE,
                ),
            )

    return lowest_price


def main() -> None:
    lines = sys.stdin.readlines()
    maze = parse_map(lines)

    print(find_cheapest_path(maze))


if __name__ == "__main__":
    main()
