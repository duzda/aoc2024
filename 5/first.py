#!/usr/bin/env python3

import sys
from collections import defaultdict

Rules = dict[str, list[str]]
Page = list[str]


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


def count_valid_pages(rules: Rules, pages: list[Page]) -> int:
    final_sum = 0
    for page_order in pages:
        if is_valid_page_order(rules, page_order):
            final_sum += int(page_order[(len(page_order) - 1) // 2])

    return final_sum


def main() -> None:
    input_text = sys.stdin.read()
    rules, pages = parse_input(input_text)
    valid_sum = count_valid_pages(rules, pages)

    print(valid_sum)


if __name__ == "__main__":
    main()
