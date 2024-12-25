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

    def sum(self) -> int:
        return self.x + self.y

    def dot(self, other: Vector) -> int:
        return self.x * other.x + self.y * other.y


@dataclass(eq=False, match_args=False)
class Equation:
    a: Vector
    b: Vector
    result: Vector

    @staticmethod
    def __is_valid_price(
        to_be_validated: int,
        price: Vector,
        max_count: int,
    ) -> bool:
        return to_be_validated != (max_count + 1) * price.sum()

    def solve(self, price: Vector, max_count: int) -> int:
        lowest_price = (max_count + 1) * price.sum()
        for i in range(max_count):
            for j in range(max_count):
                if (
                    Vector(i, j).dot(Vector(self.a.x, self.b.x)) == self.result.x
                    and Vector(i, j).dot(Vector(self.a.y, self.b.y)) == self.result.y
                ):
                    lowest_price = min(lowest_price, Vector(i, j).dot(price))

        return (
            lowest_price
            if Equation.__is_valid_price(lowest_price, price, max_count)
            else 0
        )


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
    return Vector(int(x), int(y))


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
        if result := equation.solve(price, 100):
            total_count += result

    return total_count


def main() -> None:
    lines = sys.stdin.readlines()
    equations = parse_input(lines)

    print(count_tokens(equations))


if __name__ == "__main__":
    main()
