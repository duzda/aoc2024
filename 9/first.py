#!/usr/bin/env python3

import sys


def compute_checksum(disk_data: list[str]) -> int:
    checksum = 0
    for i, id in enumerate(disk_data):
        if id == ".":
            continue

        checksum += i * int(id)

    return checksum


def shift_data(disk_data: list[str]) -> list[str]:
    shifted_data = disk_data.copy()

    front = 0
    back = len(shifted_data) - 1

    while back > front and front != len(shifted_data):
        while shifted_data[back] == ".":
            back -= 1

        if shifted_data[front] == ".":
            shifted_data[front] = shifted_data[back]
            shifted_data[back] = "."

        front += 1

    return shifted_data


def generate_disk_from_map(disk_map: str) -> list[str]:
    disk_data: list[str] = []
    for i, count in enumerate(disk_map):
        if i % 2 == 1:
            disk_data.extend(["." for _ in range(int(count))])
        else:
            disk_data.extend([str(i // 2) for _ in range(int(count))])

    return disk_data


def main() -> None:
    input_disk_map = sys.stdin.read().strip()
    expanded_disk_data = generate_disk_from_map(input_disk_map)
    shifted_data = shift_data(expanded_disk_data)

    print(compute_checksum(shifted_data))


if __name__ == "__main__":
    main()
