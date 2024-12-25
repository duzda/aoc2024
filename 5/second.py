#!/usr/bin/env python3

import sys
from collections import defaultdict
from functools import cmp_to_key

type Rules = dict[str, list[str]]
type Page = list[str]


def parse_rules(text: list[str]) -> Rules:
    rules: Rules = defaultdict(list)

    for line in text:
        rule = line.split("|")
        rules[rule[0]].append(rule[1])

    return rules


def parse_pages(text: list[str]) -> list[Page]:
    pages: list[Page] = []

    for line in text:
        pages.append(line.split(","))

    return pages


def parse_input(text: str) -> tuple[Rules, list[Page]]:
    lines = text.splitlines()
    empty_line_index = lines.index("")

    return parse_rules(lines[:empty_line_index]), parse_pages(
        lines[empty_line_index + 1 :]
    )


def is_valid_page_order(rules: Rules, page_order: Page) -> bool:
    for i, page in enumerate(page_order):
        if page not in rules.keys():
            continue

        for before_page in page_order[:i]:
            if before_page in rules[page]:
                return False

    return True


def get_sorted_page_order(rules: Rules, page_order: Page) -> list[str]:
    # https://www.reddit.com/r/adventofcode/comments/1h71eyz/comment/m0hz57r
    def cmp(a: str, b: str) -> int:
        if a in rules.keys() and b in rules[a]:
            return 1
        if b in rules.keys() and a in rules[b]:
            return -1
        return 0

    sorted_page_order: list[str] = sorted(page_order, key=cmp_to_key(cmp))

    return sorted_page_order


def count_fixed_pages(rules: Rules, pages: list[Page]) -> int:
    final_sum = 0
    for page_order in pages:
        if not is_valid_page_order(rules, page_order):
            fixed_page_order = get_sorted_page_order(rules, page_order)
            final_sum += int(fixed_page_order[(len(fixed_page_order) - 1) // 2])

    return final_sum


def main() -> None:
    input_text = sys.stdin.read()
    rules, pages = parse_input(input_text)
    valid_sum = count_fixed_pages(rules, pages)

    print(valid_sum)


if __name__ == "__main__":
    main()
