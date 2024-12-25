#!/usr/bin/env python3

from __future__ import annotations

import sys
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


def parse_map(lines: Iterable[str]) -> Map:
    pass


def main() -> None:
    lines = sys.stdin.readlines()
    parse_map(lines)

    print(lines)


if __name__ == "__main__":
    main()
