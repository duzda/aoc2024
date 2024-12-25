#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass


@dataclass
class Graph:
    nodes: dict[str, set[str]]

    def __init__(self, edges: Iterable[tuple[str, str]]) -> None:
        self.nodes = defaultdict(set)
        for a, b in edges:
            self.nodes[a].add(b)
            self.nodes[b].add(a)

    def find_biggest_party(
        self,
        p: set[str],
        r: set[str] | None = None,
        x: set[str] | None = None,
    ) -> Iterator[set[str]]:
        # https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
        if r is None:
            r = set()

        if x is None:
            x = set()

        if len(p) == 0 and len(x) == 0:
            yield r
            return

        for v in p.copy():
            yield from self.find_biggest_party(
                {u for u in p if u in self.nodes[v]},
                r | {v},
                {u for u in x if u in self.nodes[v]},
            )

            p.remove(v)
            x = x | {v}


def get_password(permutation: Iterable[str]) -> str:
    return ",".join(sorted(permutation))


def parse_edges(lines: Iterable[str]) -> Iterator[tuple[str, str]]:
    for line in lines:
        from_node, to_node = line.split("-")
        yield from_node.strip(), to_node.strip()


def main() -> None:
    lines = sys.stdin.readlines()
    edges = parse_edges(lines)

    graph = Graph(edges)

    cliques: list[set[str]] = list(graph.find_biggest_party(set(graph.nodes.keys())))
    print(get_password(sorted(cliques, key=len)[-1]))


if __name__ == "__main__":
    main()
