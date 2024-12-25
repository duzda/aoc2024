#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterable
from dataclasses import dataclass

type Position = Vector

# Just to know, how the tree looks like
"""
###############################
#.............................#
#.............................#
#.............................#
#.............................#
#..............#..............#
#.............###.............#
#............#####............#
#...........#######...........#
#..........#########..........#
#............#####............#
#...........#######...........#
#..........#########..........#
#.........###########.........#
#........#############........#
#..........#########..........#
#.........###########.........#
#........#############........#
#.......###############.......#
#......#################......#
#........#############........#
#.......###############.......#
#......#################......#
#.....###################.....#
#....#####################....#
#.............###.............#
#.............###.............#
#.............###.............#
#.............................#
#.............................#
#.............................#
#.............................#
###############################
"""


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other) -> Vector:
        if isinstance(other, self.__class__):
            return Vector(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for *: '{self.__class__}' and '{type(other)}'"
            )

    def __mod__(self, other: Vector) -> Vector:
        return Vector(self.x % other.x, self.y % other.y)

    def sum(self) -> int:
        return self.x + self.y

    def dot(self, other: Vector) -> int:
        return self.x * other.x + self.y * other.y


@dataclass
class Robot:
    position: Position
    velocity: Vector

    def update_position(self, wrap: Vector) -> None:
        self.position = (self.position + self.velocity) % wrap


def parse_line(line: str) -> Robot:
    p, v = line.split(" ")

    _, position_value = p.split("=")
    x_position, y_position = position_value.split(",")

    _, velocity_value = v.split("=")
    x_velocity, y_velocity = velocity_value.split(",")

    return Robot(
        Vector(int(x_position), int(y_position)),
        Vector(int(x_velocity), int(y_velocity)),
    )


def parse_input(lines: Iterable[str]) -> list[Robot]:
    return [parse_line(line) for line in lines]


def render_map(robots: list[Robot], size: Vector) -> str:
    robot_positions: set[Position] = {robot.position for robot in robots}

    string = ""
    for i in range(size.y):
        for j in range(size.x):
            string += "#" if Vector(j, i) in robot_positions else "."
        string += "\n"

    return string


def main() -> None:
    lines = sys.stdin.readlines()
    robots = parse_input(lines)

    size = Vector(101, 103)

    # https://www.reddit.com/r/adventofcode/comments/1hdw5op/comment/m1zfbgv
    for i in range(size.x * size.y):
        for robot in robots:
            robot.update_position(size)

        # The tree will definitely be on a step c_1 + 101x_1 or c_2 + 103x_2
        # if i % 103 == 32 or i % 101 == 83:
        string = render_map(robots, size)
        for line in string.split("\n"):
            if line.find("###############################") != -1:
                print(i + 1)
                return


if __name__ == "__main__":
    main()
