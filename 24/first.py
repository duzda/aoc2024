#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import Enum

type Registers = dict[str, bool]


class IncompleteCircuitException(Exception):
    pass


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

    def perform_instructions(self) -> None:
        for instruction in self.instructions:
            if not instruction.performed:
                instruction.perform()

    def get_values(self, starts_with: str) -> Iterator[tuple[str, bool]]:
        for register in self.registers:
            if register.startswith(starts_with):
                yield register, self.registers[register]

    def __register_instruction(self, line: str) -> None:
        a, operand, b, _, result = line.strip().split(" ")

        self.instructions.append(
            Circuit.Instruction(a, b, Operand(operand), result, self)
        )

    @dataclass
    class Instruction:
        a: str
        b: str
        operand: Operand
        result: str
        circuit: Circuit
        performed: bool = False

        def __find_predecessor(self, wanted: str) -> Circuit.Instruction:
            """Find predecessor for current Instruction

            :param wanted: Current Instruction
            :type wanted: str
            :raises IncompleteCircuitException: If unable to find wanted, this probably means, the circuit is incomplete
            :return: Predeceasing instruction
            :rtype: Circuit.Instruction
            """
            for instruction in self.circuit.instructions:
                if instruction.result == wanted:
                    return instruction

            raise IncompleteCircuitException

        def perform(self) -> None:
            if self.a not in self.circuit.registers:
                predecessor = self.__find_predecessor(self.a)
                predecessor.perform()

            if self.b not in self.circuit.registers:
                predecessor = self.__find_predecessor(self.b)
                predecessor.perform()

            self.circuit.registers[self.result] = self.operand.perform_operand(
                self.circuit.registers[self.a], self.circuit.registers[self.b]
            )


def values_to_decimal(values: list[tuple[str, bool]]) -> int:
    sorted_values: list[tuple[str, bool]] = sorted(
        values, key=lambda i: int(i[0][1:]), reverse=True
    )
    return int("".join(str(int(v[1])) for v in sorted_values), 2)


def main() -> None:
    lines = sys.stdin.readlines()
    circuit = Circuit(lines)

    circuit.perform_instructions()

    values: list[tuple[str, bool]] = list(circuit.get_values("z"))
    print(values_to_decimal(values))


if __name__ == "__main__":
    main()
