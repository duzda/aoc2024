#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

ROW_MULTIPLIER = 100

type Position = Vector

type Empty = Literal["."]
type Robot = Literal["@"]
type Box = Literal["O"]
type Wall = Literal["#"]
type Map = list[list[Empty | Robot | Box | Wall]]

type Up = Literal["^"]
type Right = Literal[">"]
type Down = Literal["v"]
type Left = Literal["<"]
type Direction = Up | Right | Down | Left


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)


def parse_map(lines: Iterable[str]) -> Map:
    return [list(line[:-1]) for line in lines]  # type: ignore[arg-type]


def parse_commands(lines: Iterable[str]) -> list[Direction]:
    commands: list[Direction] = []

    for line in lines:
        commands.extend(line[:-1])  # type: ignore[arg-type]

    return commands


def parse_input(lines: list[str]) -> tuple[Map, list[Direction]]:
    i = lines.index("\n")
    return parse_map(lines[:i]), parse_commands(lines[i + 1 :])


def find_robot(robot_map) -> Position:
    for i, row in enumerate(robot_map):
        for j, el in enumerate(row):
            if el == "@":
                return Vector(j, i)

    return Vector(-1, -1)


def direction_to_vector(command: Direction) -> Vector:
    if command == "^":
        return Vector(0, -1)
    if command == ">":
        return Vector(1, 0)
    if command == "v":
        return Vector(0, 1)
    if command == "<":
        return Vector(-1, 0)


def perform_command(robot_map: Map, command: Direction) -> None:
    robot_position = find_robot(robot_map)
    vector = direction_to_vector(command)

    while True:
        new_position = robot_position + vector
        c = robot_map[new_position.y][new_position.x]

        if c == ".":
            while c != "@":
                old_position = new_position - vector
                c = robot_map[old_position.y][old_position.x]
                robot_map[new_position.y][new_position.x] = c
                new_position = old_position

            robot_map[old_position.y][old_position.x] = "."
            break

        elif c == "#":
            break

        robot_position = new_position


def perform_commands(robot_map: Map, commands: list[Direction]) -> None:
    for command in commands:
        perform_command(robot_map, command)


def sum_boxes_coordinates(robot_map: Map) -> int:
    count = 0

    for i, row in enumerate(robot_map):
        for j, el in enumerate(row):
            if el == "O":
                count += i * 100 + j

    return count


def main() -> None:
    lines = sys.stdin.readlines()
    robot_map, commands = parse_input(lines)
    perform_commands(robot_map, commands)

    print(sum_boxes_coordinates(robot_map))


if __name__ == "__main__":
    main()
