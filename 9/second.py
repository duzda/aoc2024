#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass
class Block:
    empty_size: int
    size: int
    data: list[str]

    def __init__(self, new_data: list[str]) -> None:
        self.size = len(new_data)
        self.empty_size = new_data.count(".")
        self.data = new_data

    def emplace(self, other: Block) -> None:
        for value in other.data:
            self.data[self.size - self.empty_size] = value
            self.empty_size -= 1

    def clear(self) -> None:
        self.data = ["." for _ in range(self.size)]
        self.empty_size = self.size


def compute_checksum(disk_data: list[Block]) -> int:
    flattened = [x for block in disk_data for x in block.data]
    checksum = 0
    for i, id in enumerate(flattened):
        if id == ".":
            continue

        checksum += i * int(id)

    return checksum


def shift_data(disk_data: list[Block]) -> None:
    front = 0
    back = len(disk_data) - 1

    while back >= 0:
        while back > 0 and disk_data[back].empty_size != 0:
            back -= 1

        if front < back and disk_data[back].size <= disk_data[front].empty_size:
            disk_data[front].emplace(disk_data[back])
            disk_data[back].clear()
            back -= 1
            front = 0
        else:
            front += 1

        if front == len(disk_data):
            front = 0
            back -= 1


def generate_disk_from_map(disk_map: str) -> list[Block]:
    disk_data: list[Block] = []
    for i, count in enumerate(disk_map):
        if count == "0":
            continue

        if i % 2 == 1:
            disk_data.append(Block(["." for _ in range(int(count))]))
        else:
            disk_data.append(Block([str(i // 2) for _ in range(int(count))]))

    return disk_data


def main() -> None:
    input_disk_map = sys.stdin.read().strip()
    expanded_disk_data = generate_disk_from_map(input_disk_map)
    shift_data(expanded_disk_data)

    print(compute_checksum(expanded_disk_data))


if __name__ == "__main__":
    main()
