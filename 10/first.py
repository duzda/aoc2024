#!/usr/bin/env python3

from collections import deque

type Map = list[list[int]]
type Position = tuple[int, int]


def parse_input() -> Map:
    current_map: Map = []

    try:
        while (line := input()) is not None:
            current_map.append([int(el) for el in line])
    except EOFError:
        pass

    return current_map


def find_trailheads(current_map: Map) -> list[Position]:
    trailheads: list[Position] = []
    for y, line in enumerate(current_map):
        for x, c in enumerate(line):
            if c == 0:
                trailheads.append((x, y))

    return trailheads


def get_new_positions(position: Position, current_map: Map) -> list[Position]:
    positions: list[Position] = []
    x, y = position

    for new_position in [
        (x, y - 1),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
    ]:
        new_x, new_y = new_position
        if (
            new_x >= 0
            and new_x < len(current_map[0])
            and new_y >= 0
            and new_y < len(current_map)
        ):
            positions.append(new_position)

    return positions


def get_score(trailhead: Position, current_map: Map) -> int:
    visited = [False] * len(current_map) * len(current_map[0])

    queue: deque[Position] = deque()
    queue.append(trailhead)
    visited[trailhead[0] + len(current_map[0]) * trailhead[1]] = True

    score = 0

    while queue:
        trailhead = queue.pop()

        if current_map[trailhead[1]][trailhead[0]] == 9:
            score += 1

        for position in get_new_positions(trailhead, current_map):
            x, y = position

            if visited[x + len(current_map[0]) * y]:
                continue

            if current_map[trailhead[1]][trailhead[0]] + 1 != current_map[y][x]:
                continue

            queue.append(position)
            visited[x + len(current_map[0]) * y] = True

    return score


def count_all_scores(current_map: Map) -> int:
    trailheads = find_trailheads(current_map)
    return sum(get_score(trailhead, current_map) for trailhead in trailheads)


def main() -> None:
    current_map = parse_input()

    print(count_all_scores(current_map))


if __name__ == "__main__":
    main()
