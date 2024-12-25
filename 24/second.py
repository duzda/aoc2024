#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

type Registers = dict[str, bool]


class Operand(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

    def perform_operand(self, a: bool, b: bool) -> bool:
        """Performs operand on a and b

        :param a: First value
        :type a: bool
        :param b: Second value
        :type b: bool
        :raises ValueError: When operand is not of a valid Operand type
        :return: Operand of the two values
        :rtype: bool
        """
        if self is Operand.AND:
            return a and b
        if self is Operand.OR:
            return a or b
        if self is Operand.XOR:
            return a ^ b

        raise ValueError(f"Invalid operand ${self}")


class Circuit:
    registers: Registers
    instructions: list[Instruction]

    def __init__(self, lines: list[str]):
        index = lines.index("\n")
        self.__parse_registers(lines[:index])
        self.__parse_instructions(lines[index + 1 :])

    def __parse_registers(self, lines: Iterable[str]) -> None:
        self.registers = {}
        for line in lines:
            name, value = line.split(":")
            self.registers[name.strip()] = bool(int(value.strip()))

    def __parse_instructions(self, lines: Iterable[str]) -> None:
        self.instructions = []
        for line in lines:
            self.__register_instruction(line)

    def __register_instruction(self, line: str) -> None:
        a, operand, b, _, result = line.strip().split(" ")
        self.instructions.append(Circuit.Instruction(a, b, Operand(operand), result))

    def find_wrong(self) -> set[str]:
        # https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3kt1je
        highest_z = max(
            (filter(lambda i: i.result.startswith("z"), self.instructions)),
            key=lambda i: int(i.result[1:]),
        ).result

        wrong: set[str] = set()
        xyz: set[str] = {"x", "y", "z"}
        for ins in self.instructions:
            if (
                ins.result.startswith("z")
                and ins.operand != Operand.XOR
                and ins.result != highest_z
            ):
                wrong.add(ins.result)

            if (
                ins.operand == Operand.XOR
                and ins.result[0] not in xyz
                and ins.a[0] not in xyz
                and ins.b[0] not in xyz
            ):
                wrong.add(ins.result)

            if ins.operand == Operand.AND and "x00" not in {ins.a, ins.b}:
                for sub_ins in self.instructions:
                    if (
                        ins.result == sub_ins.a or ins.result == sub_ins.b
                    ) and sub_ins.operand != Operand.OR:
                        wrong.add(ins.result)

            if ins.operand == Operand.XOR:
                for sub_ins in self.instructions:
                    if (
                        ins.result == sub_ins.a or ins.result == sub_ins.b
                    ) and sub_ins.operand == Operand.OR:
                        wrong.add(ins.result)

        return wrong

    @dataclass
    class Instruction:
        a: str
        b: str
        operand: Operand
        result: str


if __name__ == "__main__":
    circuit = Circuit(sys.stdin.readlines())

    print(",".join(sorted(circuit.find_wrong())))
