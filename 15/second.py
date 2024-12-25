#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
from typing import Literal

ROW_MULTIPLIER = 100

type Position = Vector

type Empty = Literal["."]
type Robot = Literal["@"]
type BoxLeft = Literal["["]
type BoxRight = Literal["]"]
type Wall = Literal["#"]
type Map = list[list[Empty | Robot | BoxLeft | BoxRight | Wall]]

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
    robot_map: Map = []

    for line in lines:
        robot_map.append([])
        for c in line:
            if c == "#":
                robot_map[-1].extend(["#", "#"])
            elif c == "O":
                robot_map[-1].extend(["[", "]"])
            elif c == "@":
                robot_map[-1].extend(["@", "."])
            elif c == ".":
                robot_map[-1].extend([".", "."])

    return robot_map  # type: ignore[arg-type]


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


def is_horizontal(movement: Vector) -> bool:
    return movement.y == 0 and movement.x != 0


def perform_horizontal(position: Position, robot_map: Map, direction: Vector) -> bool:
    c = robot_map[position.y][position.x]

    if c == "#":
        return False

    if c == ".":
        return True

    new_position = position + direction
    is_valid = perform_horizontal(new_position, robot_map, direction)
    if is_valid:
        robot_map[new_position.y][new_position.x] = c

    return is_valid


def validate_vertical(
    position: Position,
    robot_map: Map,
    direction: Vector,
    visited: set[Position],
) -> bool:
    c = robot_map[position.y][position.x]

    if c == "#":
        return False

    if c == ".":
        return True

    new_position = position + direction
    new_c = robot_map[new_position.y][new_position.x]
    visited.add(new_position)

    if c == "@" or c == "]":
        if new_c == "[":
            shifted_position = new_position + Vector(1, 0)
            visited.add(shifted_position)
            return validate_vertical(
                new_position, robot_map, direction, visited
            ) and validate_vertical(shifted_position, robot_map, direction, visited)

    if c == "@" or c == "[":
        if new_c == "]":
            shifted_position = new_position - Vector(1, 0)
            visited.add(shifted_position)
            return validate_vertical(
                new_position, robot_map, direction, visited
            ) and validate_vertical(shifted_position, robot_map, direction, visited)

    return validate_vertical(new_position, robot_map, direction, visited)


def perform_vertical(position: Position, robot_map: Map, direction: Vector) -> bool:
    old_map = deepcopy(robot_map)
    visited: set[Position] = {position}
    if is_valid := validate_vertical(position, robot_map, direction, visited):
        for node_position in visited:
            if (old_position := (node_position - direction)) in visited:
                character = old_map[old_position.y][old_position.x]
            else:
                character = "."

            robot_map[node_position.y][node_position.x] = character

    return is_valid


def perform_command_util(position: Position, robot_map: Map, direction: Vector) -> bool:
    if is_horizontal(direction):
        return perform_horizontal(position, robot_map, direction)
    else:
        return perform_vertical(position, robot_map, direction)


def perform_command(robot_map: Map, command: Direction) -> None:
    robot_position = find_robot(robot_map)
    direction_vector = direction_to_vector(command)

    if perform_command_util(robot_position, robot_map, direction_vector):
        robot_map[robot_position.y][robot_position.x] = "."


def perform_commands(robot_map: Map, commands: list[Direction]) -> None:
    for command in commands:
        perform_command(robot_map, command)


def sum_boxes_coordinates(robot_map: Map) -> int:
    count = 0

    for i, row in enumerate(robot_map):
        for j, el in enumerate(row):
            if el == "[":
                count += i * 100 + j

    return count


def main() -> None:
    lines = sys.stdin.readlines()
    robot_map, commands = parse_input(lines)

    perform_commands(robot_map, commands)

    print(sum_boxes_coordinates(robot_map))


if __name__ == "__main__":
    main()
