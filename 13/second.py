#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def dot(self, other: Vector) -> int:
        return self.x * other.x + self.y * other.y


@dataclass(eq=False, match_args=False)
class Equation:
    a: Vector
    b: Vector
    result: Vector

    def solve(self, price: Vector) -> int:
        # https://www.geeksforgeeks.org/point-of-intersection-of-two-lines-formula/
        x = (self.b.x * -self.result.y - self.b.y * -self.result.x) / (
            self.a.x * self.b.y - self.a.y * self.b.x
        )
        y = (-self.result.x * self.a.y + self.result.y * self.a.x) / (
            self.a.x * self.b.y - self.a.y * self.b.x
        )

        if not (x == int(x) and y == int(y)):
            return 0

        return Vector(int(x), int(y)).dot(price)


def parse_button_line(line: str) -> Vector:
    _, eq = line.split(":")
    x, y = eq.split(",")
    _, x = x.split("+")
    _, y = y.split("+")
    return Vector(int(x), int(y))


def parse_prize_line(line: str) -> Vector:
    _, eq = line.split(":")
    x, y = eq.split(",")
    _, x = x.split("=")
    _, y = y.split("=")
    return Vector(int(x), int(y)) + Vector(10000000000000, 10000000000000)


def parse_input(lines: list[str]) -> list[Equation]:
    equations: list[Equation] = []

    for i in range(0, len(lines), 4):
        equations.append(
            Equation(
                parse_button_line(lines[i]),
                parse_button_line(lines[i + 1]),
                parse_prize_line(lines[i + 2]),
            )
        )

    return equations


def count_tokens(equations: Iterable[Equation]) -> int:
    price = Vector(3, 1)

    total_count = 0

    for equation in equations:
        if result := equation.solve(price):
            total_count += result

    return total_count


def main() -> None:
    lines = sys.stdin.readlines()
    equations = parse_input(lines)

    print(count_tokens(equations))


if __name__ == "__main__":
    main()
