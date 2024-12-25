#!/usr/bin/env python3

import sys
from typing import Callable


class Program:
    A: int
    B: int
    C: int

    instructions: list[int]
    program_output: list[int]

    IP: int = 0

    def __init__(self, A: int, B: int, C: int, instructions: list[int]) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.instructions = instructions
        self.program_output = []

    def __get_operand(self, operand: int):
        # According to tests, combo 7 is literal 7
        operands = [0, 1, 2, 3, self.A, self.B, self.C]
        return operands[operand]

    def __adv(self, value: int) -> None:
        self.A = int(self.A / (2**value))

    def __bxl(self, value: int) -> None:
        self.B = self.B ^ value

    def __bst(self, value: int) -> None:
        self.B = value % 8

    def __jnz(self, value: int) -> None:
        if self.A != 0:
            self.IP = value - 2

    def __bxc(self, _: int) -> None:
        self.B = self.B ^ self.C

    def __out(self, value: int) -> None:
        self.program_output.append(value % 8)

    def __bdv(self, value: int) -> None:
        self.B = int(self.A / (2**value))

    def __cdv(self, value: int) -> None:
        self.C = int(self.A / (2**value))

    def __process_instruction(self) -> bool:
        """Processes next instruction and returns whether the program has halted.

        :return: Has program halted
        :rtype: bool
        """
        if self.IP < 0 or self.IP >= len(self.instructions):
            return True

        instruction = self.instructions[self.IP]
        combo_operand = self.__get_operand(self.instructions[self.IP + 1])

        instructions: list[Callable[[int], None]] = [
            self.__adv,
            self.__bxl,
            self.__bst,
            self.__jnz,
            self.__bxc,
            self.__out,
            self.__bdv,
            self.__cdv,
        ]

        instructions[instruction](combo_operand)
        self.IP += 2

        return False

    def process_program(self) -> None:
        while not self.__process_instruction():
            pass
        print(",".join(map(str, self.program_output)))


def parse_program_input(lines: list[str]) -> tuple[int, int, int, list[int]]:
    _, A = lines[0].split(":")
    _, B = lines[1].split(":")
    _, C = lines[2].split(":")

    _, instructions = lines[4].split(" ")
    parsed_instructions = [int(i) for i in instructions.split(",")]

    return int(A), int(B), int(C), parsed_instructions


def main() -> None:
    lines = sys.stdin.readlines()
    A, B, C, instructions = parse_program_input(lines)

    program = Program(A, B, C, instructions)
    program.process_program()


if __name__ == "__main__":
    main()
