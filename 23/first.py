#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import AbstractSet


@dataclass
class Node:
    value: str
    neighbors: list[Node]

    def __init__(self, value: str) -> None:
        self.value = value
        self.neighbors = []


@dataclass
class Graph:
    nodes: dict[str, Node]

    def __init__(self, edges: Iterable[tuple[str, str]]) -> None:
        self.nodes = {}
        for a, b in edges:
            self.add_edge(a, b)

    def add_edge(self, a: str, b: str) -> None:
        if a not in self.nodes:
            self.nodes[a] = Node(a)

        if b not in self.nodes:
            self.nodes[b] = Node(b)

        self.nodes[a].neighbors.append(self.nodes[b])
        self.nodes[b].neighbors.append(self.nodes[a])

    def find_cycles(self, length: int) -> set[AbstractSet[str]]:
        cycles: set[AbstractSet[str]] = set()

        def find_cycles_util(
            current: Node, length: int, visited: list[str] | None = None
        ) -> None:
            if visited is None:
                visited = [current.value]
            else:
                visited = [*visited, current.value]

                if current.value == visited[0]:
                    if len(visited) == length + 1:
                        cycles.add(frozenset(visited))
                    return

                if len(visited) > length:
                    return

            for neighbor in current.neighbors:
                find_cycles_util(neighbor, length, visited)

        for node in self.nodes.values():
            find_cycles_util(node, length)

        return cycles


def parse_edges(lines: Iterable[str]) -> Iterator[tuple[str, str]]:
    for line in lines:
        from_node, to_node = line.split("-")
        yield from_node.strip(), to_node.strip()


def filter_by_starting_name(
    cycles: Iterable[AbstractSet[str]], starts_with: str
) -> Iterator[AbstractSet[str]]:
    for cycle in cycles:
        if any(el.startswith(starts_with) for el in cycle):
            yield cycle


def main() -> None:
    lines = sys.stdin.readlines()
    edges = parse_edges(lines)

    graph = Graph(edges)

    cycles = graph.find_cycles(3)
    cycles_t = filter_by_starting_name(cycles, "t")

    print(len(list(cycles_t)))


if __name__ == "__main__":
    main()
