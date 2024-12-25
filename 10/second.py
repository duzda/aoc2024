#!/usr/bin/env python3

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
    def get_score_util(position: Position, visited: set[Position]) -> int:
        visited.add(position)

        score = 0

        if current_map[position[1]][position[0]] == 9:
            score += 1

        for new_position in get_new_positions(position, current_map):
            x, y = new_position

            if new_position in visited:
                continue

            if current_map[position[1]][position[0]] + 1 != current_map[y][x]:
                continue

            score += get_score_util(new_position, visited.copy())

        return score

    visited: set[Position] = set()
    return get_score_util(trailhead, visited.copy())


def count_all_scores(current_map: Map) -> int:
    trailheads = find_trailheads(current_map)
    return sum(get_score(trailhead, current_map) for trailhead in trailheads)


def main() -> None:
    current_map = parse_input()

    print(count_all_scores(current_map))


if __name__ == "__main__":
    main()
