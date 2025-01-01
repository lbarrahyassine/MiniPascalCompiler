from Code_generator import *

class Interpreter:
    def __init__(self, assembly_code, symbol_table):
        self.assembly_code = assembly_code
        self.symbol_table = symbol_table
        self.memory = [0] * len(symbol_table)  # Mémoire représentée comme une liste
        self.registers = {"AX": 0, "BX": 0, "SP": []}  # Simuler les registres du CPU, incluant le pointeur de pile
        self.program_counter = 0  # Simuler le compteur de programme

    def execute(self):
        """Boucle principale d'exécution."""
        while self.program_counter < len(self.assembly_code):
            instruction = self.assembly_code[self.program_counter].strip()
            self.program_counter += 1
            if not instruction or instruction.startswith(";"):  # Ignorer les commentaires ou lignes vides
                continue
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction):
        """Exécuter une seule instruction."""
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
        """Implémentation de l'instruction MOV."""
        value = self.get_value(src)
        if dest in self.registers:  # Si la destination est un registre
            self.registers[dest] = value
        elif dest.startswith("$"):  # Si la destination est une adresse mémoire
            address = self.get_address(dest)
            self.memory[address] = value
        else:
            raise ValueError(f"Unknown destination: {dest}")

    def add(self, dest, src):
        """Implémentation de l'instruction ADD."""
        value = self.get_value(src)
        if dest in self.registers:  # L'addition ne peut être que dans un registre
            self.registers[dest] += value
        else:
            raise ValueError(f"ADD requires a register destination, got: {dest}")

    def mul(self, dest, src):
        """Implémentation de l'instruction MUL."""
        value = self.get_value(src)
        if dest in self.registers:
            self.registers[dest] *= value
        else:
            raise ValueError(f"MUL requires a register destination, got: {dest}")

    def push(self, src):
        """Implémentation de l'instruction PUSH."""
        value = self.get_value(src)
        self.registers["SP"].append(value)

    def pop(self, dest):
        """Implémentation de l'instruction POP."""
        stack = self.registers.get("SP", [])
        if not stack:
            raise ValueError("Stack underflow")
        value = stack.pop()
        if dest in self.registers:
            self.registers[dest] = value
        else:
            raise ValueError(f"POP requires a register destination, got: {dest}")

    def out(self, src):
        """Implémentation de l'instruction OUT."""
        value = self.get_value(src)
        print(f"OUTPUT: {value}")  # Afficher l'output de la commande OUT

    def get_value(self, operand):
        """Obtenir la valeur d'un registre, une adresse mémoire, ou une constante."""
        if operand in self.registers:  # Si c'est un registre
            return self.registers[operand]
        elif operand.isdigit():  # Si c'est une constante immédiate
            return int(operand)
        elif operand.startswith("$"):  # Si c'est une adresse mémoire (ex: $0000)
            address = self.get_address(operand)
            return self.memory[address]
        elif operand in self.symbol_table:  # Si c'est une variable (nom de la variable)
            address = self.symbol_table[operand]["address"]
            return self.memory[address]
        else:
            raise ValueError(f"Unknown operand: {operand}")

    def get_address(self, operand):
        """Convertir une adresse en notation hexadécimale (ex: $0000) en un entier."""
        # S'assurer que l'adresse commence par "$" et est au format hexadécimal
        if operand.startswith("$"):
            return int(operand[1:], 16)  # Convertir l'adresse hexadécimale en entier
        else:
            raise ValueError(f"Invalid address format: {operand}")


# Exemple d'utilisation avec le code assembleur généré
assembly_code = generator.instructions
print("------------------------------------------------------------------")
interpreter = Interpreter(assembly_code, symbol_table)
interpreter.execute()

# Afficher l'état final de la mémoire
print("\nMemory State:")
print(interpreter.memory)
