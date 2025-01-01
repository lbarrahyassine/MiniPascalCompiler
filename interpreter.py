from Code_generator import *
class Interpreter:
    def __init__(self, assembly_code, symbol_table):
        self.assembly_code = assembly_code
        self.symbol_table = symbol_table
        self.memory = [0] * len(symbol_table)  # Memory as a list, one slot per variable
        self.registers = {"AX": 0, "BX": 0}  # Simulate CPU registers
        self.program_counter = 0  # Simulate the program counter

    def execute(self):
        """Main execution loop."""
        while self.program_counter < len(self.assembly_code):
            instruction = self.assembly_code[self.program_counter].strip()
            print(f"Executing: {instruction}")
            self.program_counter += 1
            if not instruction or instruction.startswith(";"):  # Skip comments or empty lines
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

        elif command == "PUSH":
            src = parts[1]
            self.push(src)

        elif command == "POP":
            dest = parts[1]
            self.pop(dest)

        elif command == "OUT":
            src = parts[1]
            self.out(src)

        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    def mov(self, dest, src):
        """MOV instruction implementation."""
        value = self.get_value(src)
        if dest in self.registers:  # Register destination
            self.registers[dest] = value
        elif dest in self.symbol_table:  # Memory destination
            address = self.symbol_table[dest]["address"]
            self.memory[address] = value
        else:
            raise ValueError(f"Unknown destination: {dest}")

    def add(self, dest, src):
        """ADD instruction implementation."""
        value = self.get_value(src)
        if dest in self.registers:
            self.registers[dest] += value
        else:
            raise ValueError(f"ADD requires a register destination, got: {dest}")

    def mul(self, dest, src):
        """MUL instruction implementation."""
        value = self.get_value(src)
        if dest in self.registers:
            self.registers[dest] *= value
        else:
            raise ValueError(f"MUL requires a register destination, got: {dest}")

    def push(self, src):
        """PUSH instruction implementation."""
        value = self.get_value(src)
        self.registers["SP"] = self.registers.get("SP", [])  # Initialize stack pointer
        self.registers["SP"].append(value)

    def pop(self, dest):
        """POP instruction implementation."""
        stack = self.registers.get("SP", [])
        if not stack:
            raise ValueError("Stack underflow")
        value = stack.pop()
        if dest in self.registers:
            self.registers[dest] = value
        else:
            raise ValueError(f"POP requires a register destination, got: {dest}")

    def out(self, src):
        """OUT instruction implementation."""
        value = self.get_value(src)
        print(f"OUTPUT: {value}")

    def get_value(self, operand):
        """Get the value of a register, memory location, or constant."""
        if operand in self.registers:  # Register
            return self.registers[operand]
        elif operand in self.symbol_table:  # Memory
            address = self.symbol_table[operand]["address"]
            return self.memory[address]
        elif operand.isdigit():  # Immediate constant
            return int(operand)
        else:
            raise ValueError(f"Unknown operand: {operand}")


assembly_code=generator.instructions

interpreter = Interpreter(assembly_code, symbol_table)
interpreter.execute()

# Print Final Memory State
print("\nMemory State:")
print(interpreter.memory)
