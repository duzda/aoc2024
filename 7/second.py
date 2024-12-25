#!/usr/bin/env python3

type Equation = tuple[int, list[int]]


def parse_line(line: str) -> Equation:
    splitted = line.split(":")
    return int(splitted[0]), [
        int(expression) for expression in splitted[1].strip().split(" ")
    ]


def parse_input() -> list[Equation]:
    equations: list[Equation] = []

    try:
        while (line := input()) is not None:
            equations.append(parse_line(line))
    except EOFError:
        pass

    return equations


def has_solution_recursive(
    expected_result: int,
    numbers: list[int],
    current_result: int,
    i: int = 1,
):
    if i == len(numbers) or current_result > expected_result:
        return current_result == expected_result

    def curried_solution(current_result: int):
        return has_solution_recursive(expected_result, numbers, current_result, i + 1)

    return (
        curried_solution(current_result + numbers[i])
        or curried_solution(current_result * numbers[i])
        or curried_solution(int(str(current_result) + str(numbers[i])))
    )


def has_solution(equation: Equation) -> bool:
    expected_result, numbers = equation
    return has_solution_recursive(expected_result, numbers, numbers[0])


def count_equations(equations: list[Equation]) -> int:
    equation_sum = 0
    for equation in equations:
        if has_solution(equation):
            equation_sum += equation[0]

    return equation_sum


def main() -> None:
    equations = parse_input()

    print(count_equations(equations))


if __name__ == "__main__":
    main()
