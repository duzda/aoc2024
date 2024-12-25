#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import cache

type Position = Vector

NUMERIC_KEYPAD: str = """
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

DIRECTIONAL_KEYPAD: str = """
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""


def movement_vector_to_char(vector: Vector) -> str:
    mapping = {
        Vector(0, -1): "^",
        Vector(1, 0): ">",
        Vector(0, 1): "v",
        Vector(-1, 0): "<",
    }
    return mapping[vector]


@dataclass
class SequenceNode:
    visited: set[Position] = field(default_factory=set)
    sequence: list[str] = field(default_factory=list)
    movements: str = ""

    def is_visited(self, position: Position) -> bool:
        return position in self.visited

    @staticmethod
    def create_from(
        sequence_node: SequenceNode,
        mapping: dict[Position, str],
        new_position: Position,
        movement: str,
    ) -> SequenceNode:
        visited = {*sequence_node.visited, new_position}
        sequence = [*sequence_node.sequence, mapping[new_position]]
        movements = sequence_node.movements + movement
        return SequenceNode(visited, sequence, movements)


class Keypad:
    mappings: dict[Position, str]
    reverse_map: dict[str, Position]
    size: Vector

    def __init__(self, keypad: str) -> None:
        self.mappings = {}
        for y, line in enumerate(keypad.splitlines()[2::2]):
            for x, c in enumerate(line[2::4]):
                if c == " ":
                    continue

                self.mappings[Vector(x, y)] = c

        self.reverse_map = {v: k for k, v in self.mappings.items()}
        self.size = Vector(x + 1, y + 1)

    @cache
    def __get_valid_next_positions(self, position: Position) -> list[Position]:
        return list(
            filter(
                lambda p: p.x >= 0
                and p.x < self.size.x
                and p.y >= 0
                and p.y < self.size.y,
                (
                    position + v
                    for v in [Vector(0, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0)]
                ),
            )
        )

    @cache
    def get_sequences(self, a: str, b: str) -> list[str]:
        movement_sequences: list[str] = []

        sequences: deque[SequenceNode] = deque()
        sequences.append(SequenceNode({self.reverse_map[a]}, [a]))

        minimum_length = sys.maxsize

        while len(sequences) != 0:
            node = sequences.popleft()
            last = node.sequence[-1]

            if last == b and len(node.sequence) <= minimum_length:
                minimum_length = len(node.sequence)
                movement_sequences.append(node.movements + "A")
                continue

            for position in self.__get_valid_next_positions(self.reverse_map[last]):
                if position not in self.mappings:
                    continue

                if not node.is_visited(position):
                    sequences.append(
                        SequenceNode.create_from(
                            node,
                            self.mappings,
                            position,
                            movement_vector_to_char(position - self.reverse_map[last]),
                        )
                    )

        return movement_sequences


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)


def parse_input(lines: Iterable[str]) -> list[str]:
    return [line.strip() for line in lines]


@cache
def get_shortest_complex_path_length(
    sequence: str, current_keypad: Keypad, next_keypad: Keypad, depth: int
) -> int:
    if depth == 0:
        return len(sequence)

    sequence = "A" + sequence

    length = 0
    for i in range(len(sequence) - 1):
        length += min(
            [
                get_shortest_complex_path_length(
                    seq,
                    next_keypad,
                    next_keypad,
                    depth - 1,
                )
                for seq in current_keypad.get_sequences(sequence[i], sequence[i + 1])
            ]
        )

    return length


def extract_numeric(sequence: str) -> int:
    return int("".join(list(filter(lambda c: c >= "0" and c <= "9", list(sequence)))))


def get_score(sequence: str, numeric: Keypad, directional: Keypad) -> int:
    return get_shortest_complex_path_length(
        sequence, numeric, directional, 26
    ) * extract_numeric(sequence)


def get_scores(sequences: list[str], numeric: Keypad, directional: Keypad) -> int:
    return sum(get_score(sequence, numeric, directional) for sequence in sequences)


def main() -> None:
    lines = sys.stdin.readlines()
    sequences = parse_input(lines)
    numeric = Keypad(NUMERIC_KEYPAD)
    directional = Keypad(DIRECTIONAL_KEYPAD)

    print(get_scores(sequences, numeric, directional))


if __name__ == "__main__":
    main()
