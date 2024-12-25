#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

type Position = Vector

type Start = Literal["S"]
type End = Literal["E"]
type Empty = Literal["."]
type Wall = Literal["#"]
type Map = list[list[Start | End | Empty | Wall]]


class NotFoundException(Exception):
    pass


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)


class RaceMap:
    race_map: Map
    distance_map: dict[Position, int]

    def __init__(self, lines: Iterable[str]) -> None:
        self.__init_race_map(lines)
        self.__init_distance_map()

    def __init_race_map(self, lines: Iterable[str]) -> None:
        self.race_map = []
        for line in lines:
            self.race_map.append(list(line))  # type: ignore[arg-type]

    def __find_element(self, needle: Start | End) -> Position:
        """Finds the element in race_map

        :param needle: 'S' or 'E', anything else doesn't make sense
        :type needle: Start | End
        :raises NotFoundException: When needle can't be found
        :return: Position of the needle in the map
        :rtype: Position
        """
        for y, line in enumerate(self.race_map):
            for x, c in enumerate(line):
                if c == needle:
                    return Vector(x, y)

        raise NotFoundException

    def __get_valid_next_positions(self, position: Position) -> list[Position]:
        return list(
            filter(
                lambda p: p.x >= 0
                and p.x < self.__width
                and p.y >= 0
                and p.y < self.__height
                and self.race_map[p.y][p.x] != "#",
                (
                    position + v
                    for v in [Vector(0, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0)]
                ),
            )
        )

    def __init_distance_map(self) -> None:
        self.distance_map = {}

        to_be_visited: deque[tuple[Position, int]] = deque()
        to_be_visited.append((self.__find_element("S"), 0))

        while len(to_be_visited) != 0:
            position, distance = to_be_visited.popleft()
            self.distance_map[position] = distance

            for new_position in self.__get_valid_next_positions(position):
                if new_position not in self.distance_map.keys():
                    to_be_visited.append((new_position, distance + 1))

    def __count_cheats_position(self, minimum_time: int, position: Position) -> int:
        new_positions = (
            position + v
            for v in [
                Vector(0, -2),
                Vector(1, -1),
                Vector(2, 0),
                Vector(1, 1),
                Vector(0, 2),
                Vector(-1, 1),
                Vector(-2, 0),
                Vector(-1, -1),
            ]
        )

        count = 0
        for new_position in new_positions:
            if new_position in self.distance_map.keys():
                diff = self.distance_map[new_position] - self.distance_map[position]
                if diff >= minimum_time + 2:
                    count += 1

        return count

    def count_cheats(self, minimum_time: int) -> int:
        return sum(
            [
                self.__count_cheats_position(minimum_time, position)
                for position in self.distance_map.keys()
            ]
        )

    @property
    def __width(self) -> int:
        return len(self.race_map[0])

    @property
    def __height(self) -> int:
        return len(self.race_map)


def main() -> None:
    lines = sys.stdin.readlines()
    race_map = RaceMap(lines)

    print(race_map.count_cheats(100))


if __name__ == "__main__":
    main()
