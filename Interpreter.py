from Code_generator import *

class Interpreter:
    def __init__(self, assembly_code, symbol_table):
        self.assembly_code = assembly_code
        self.symbol_table = symbol_table
        self.memory = [None] * len(symbol_table)  # Memory represented as a list, supporting both integers and strings
        self.registers = {"AX": None, "BX": None, "SP": []}  # Registers, allowing for mixed types
        self.program_counter = 0  # Simulate the program coungiter
        self.outputs = []

    def execute(self):
        while self.program_counter < len(self.assembly_code):
            instruction = self.assembly_code[self.program_counter].strip()
            self.program_counter += 1
            if not instruction or instruction.startswith(";"):  # Ignore comments or empty lines
                continue
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction):
        """Execute a single instruction."""
        parts = instruction.split()
        command = parts[0]

        if command == "MOV":
            dest, src = parts[1].rstrip(","), parts[2]
            self.mov(dest, src)

        elif command == "ADD":
            dest, src = parts[1].rstrip(","), parts[2]
            self.add(dest, src)

        elif command == "MUL":
            dest, src = parts[1].rstrip(","), parts[2]
            self.mul(dest, src)

        elif command == "SUB":
            dest, src = parts[1].rstrip(","), parts[2]
            print (src, dest)
            self.sub(dest, src)

        elif command == "DIV":
            dest, src = parts[1].rstrip(","), parts[2]
            self.div(dest, src)

        elif command == "PUSH":
            src = parts[1]
            self.push(src)

        elif command == "POP":
            dest = parts[1]
            self.pop(dest)

        elif command == "OUT":
            src = parts[1]
            self.out(src)

        elif command == "OUT_STR":
            src = " ".join(parts[1:])  # Handles string literals with spaces
            self.out_str(src)

        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    def mov(self, dest, src):
        value = self.get_value(src)
        if dest in self.registers:  # If the destination is a register
            self.registers[dest] = value
        elif dest.startswith("$"):  # If the destination is a memory address
            address = self.get_address(dest)
            self.memory[address] = value
        else:
            raise ValueError(f"Unknown destination: {dest}")

    def add(self, dest, src):
        value = self.get_value(src)
        if dest in self.registers:  # Addition only works in registers
            if isinstance(self.registers[dest], int) and isinstance(value, int):
                self.registers[dest] += value
            else:
                raise ValueError(f"ADD requires integer operands, got {self.registers[dest]} and {value}")
        else:
            raise ValueError(f"ADD requires a register destination, got: {dest}")

    def mul(self, dest, src):
        value = self.get_value(src)
        if dest in self.registers:
            if isinstance(self.registers[dest], int) and isinstance(value, int):
                self.registers[dest] *= value
            else:
                raise ValueError(f"MUL requires integer operands, got {self.registers[dest]} and {value}")
        else:
            raise ValueError(f"MUL requires a register destination, got: {dest}")

    def sub(self, dest, src):
        value = self.get_value(src)
        if dest in self.registers:  # Subtraction only works in registers
            if isinstance(self.registers[dest], int) and isinstance(value, int):
                self.registers[dest] = value- self.registers[dest]
            else:
                raise ValueError(f"SUB requires integer operands, got {self.registers[dest]} and {value}")
        else:
            raise ValueError(f"SUB requires a register destination, got: {dest}")

    def div(self, dest, src):
        value = self.get_value(src)
        if dest in self.registers:  # Division only works in registers
            if isinstance(self.registers[dest], int) and isinstance(value, int):
                if self.registers[dest] == 0:
                    raise ZeroDivisionError("interpreteur : Division by zero is not allowed.")
                self.registers[dest] = value //self.registers[dest]  # Perform integer division
            else:
                raise ValueError(f"DIV requires integer operands, got {self.registers[dest]} and {value}")
        else:
            raise ValueError(f"DIV requires a register destination, got: {dest}")

    def push(self, src):
        value = self.get_value(src)
        self.registers["SP"].append(value)

    def pop(self, dest):
        stack = self.registers.get("SP", [])
        if not stack:
            raise ValueError("Stack underflow")
        value = stack.pop()
        if dest in self.registers:
            self.registers[dest] = value
        else:
            raise ValueError(f"POP requires a register destination, got: {dest}")

    def out(self, src):
        value = self.get_value(src)
        self.outputs.append(value)

    def out_str(self, src):
        """Implementation of the OUT_STR instruction for strings."""
        if src.startswith('"') and src.endswith('"'):  # String literal
            self.outputs.append(src[1:-1])
        else:  # Variable
            value = self.get_value(src)
            if isinstance(value, str):
                self.outputs.append(value)
            else:
                raise ValueError(f"OUT_STR expects a string, got {value}")


    def get_value(self, operand):
        """Get the value of a register, memory address, or constant."""
        if operand in self.registers:  # If it's a register
            return self.registers[operand]
        elif operand.isdigit():  # If it's an immediate integer constant
            return int(operand)
        elif operand.startswith("$"):  # If it's a memory address (e.g., $0000)
            address = self.get_address(operand)
            return self.memory[address]
        elif operand in self.symbol_table:  # If it's a variable (e.g., variable name)
            address = self.symbol_table[operand]["address"]
            return self.memory[address]
        elif operand.startswith('"') and operand.endswith('"'):
            return operand[1:-1]
        else:
            raise ValueError(f"Unknown operand: {operand}")

    def get_address(self, operand):
        """Convert a hexadecimal address (e.g., $0000) to an integer."""
        if operand.startswith("$"):
            return int(operand[1:], 16)  # Convert the hexadecimal address to an integer
        else:
            raise ValueError(f"Invalid address format: {operand}")

