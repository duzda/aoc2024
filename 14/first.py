#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterable
from dataclasses import dataclass

type Position = Vector


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

    def calculate_position_after_steps(self, steps: int, wrap: Vector) -> Position:
        new_position: Position = (self.position + self.velocity * steps) % wrap
        return new_position


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


def simulate_steps(n: int, robots: Iterable[Robot], map_size: Vector) -> list[Position]:
    return [robot.calculate_position_after_steps(n, map_size) for robot in robots]


def calculate_quadrants(
    positions: Iterable[Position], size: Vector
) -> tuple[int, int, int, int]:
    half_x = size.x // 2
    half_y = size.y // 2

    upper_left = 0
    upper_right = 0
    bottom_left = 0
    bottom_right = 0

    for position in positions:
        if position.y < half_y:
            if position.x < half_x:
                upper_left += 1
            elif position.x > half_x:
                upper_right += 1
        elif position.y > half_y:
            if position.x < half_x:
                bottom_left += 1
            elif position.x > half_x:
                bottom_right += 1

    return upper_left, upper_right, bottom_right, bottom_left


def calculate_safety_factor(positions: Iterable[Position], size: Vector) -> int:
    a, b, c, d = calculate_quadrants(positions, size)
    return a * b * c * d


def main() -> None:
    lines = sys.stdin.readlines()
    robots = parse_input(lines)

    size = Vector(101, 103)

    new_positions = simulate_steps(100, robots, size)

    print(calculate_safety_factor(new_positions, size))


if __name__ == "__main__":
    main()
