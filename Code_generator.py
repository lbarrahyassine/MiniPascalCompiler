from Semantic_analyzer import *
class CodeGenerator:
    def __init__(self, ast, symbol_table, output_file="output.txt"):
        self.ast = ast
        self.symbol_table = symbol_table
        self.instructions = []
        self.output_file = output_file
        self.current_label = 0

    def new_label(self):
        """Génère une nouvelle étiquette unique."""
        self.current_label += 1
        return f"L{self.current_label}"

    def generate_code(self, node):
        if node.type == "ProgramName":
            # Ajouter un commentaire avec le nom du programme
            '''self.instructions.append(f"; ProgramNAME: {node.value}\n")'''
            pass

        elif node.type == "Program":
            '''self.instructions.append(f"; Program: {node.value}\n")'''
            for child in node.children:
                self.generate_code(child)


        elif node.type == "Declarations":
            # Ajouter les déclarations de variables
            '''for declaration in node.children:
                variable = declaration.children[0]
                self.instructions.append(f"{variable.value} DW 0\n")'''
            pass

        elif node.type == "Block":
            # Générer le code pour les instructions dans le bloc
            for child in node.children:
                self.generate_code(child)

        elif node.type == "Statements":
            # Générer le code pour chaque instruction
            for child in node.children:
                self.generate_code(child)

        elif node.type == "Assignment":
            # Générer une affectation
            var_name = node.value
            expression_code = self.generate_expression(node.children[0])
            self.instructions.extend(expression_code)
            self.instructions.append(f"MOV {var_name}, AX\n")

        elif node.type == "Write":
            # Générer un affichage (simulé pour l'instant)
            var_name = node.children[0].value
            self.instructions.append(f"MOV AX, {var_name}\n")
            self.instructions.append(f"OUT AX\n")

    def generate_expression(self, node):
        """Génère le code assembleur pour une expression."""
        if node.type == "Number":
            return [f"MOV AX, {node.value}\n"]

        elif node.type == "Variable":
            return [f"MOV AX, {node.value}\n"]

        elif node.type == "BinaryOperation":
            left_code = self.generate_expression(node.children[0])
            right_code = self.generate_expression(node.children[1])
            operator = node.value

            operation_map = {
                "+": "ADD",
                "*": "MUL",
            }
            operation = operation_map.get(operator)
            if not operation:
                raise ValueError(f"Unknown operator: {operator}")

            code = left_code
            code.append("PUSH AX\n")  # Sauvegarde la valeur gauche
            code.extend(right_code)
            code.append("POP BX\n")  # Récupère la valeur gauche dans BX
            code.append(f"{operation} AX, BX\n")  # Effectue l'opération
            return code

        else:
            raise ValueError(f"Unsupported node type for expression: {node.type}")

    def write_to_file(self):
        """Écrit les instructions générées dans un fichier."""
        with open(self.output_file, "w") as f:
            f.writelines(self.instructions)

print("------------------------------------------------------------------")
generator = CodeGenerator(ast, symbol_table)
generator.generate_code(ast)

#ast.display()
#print(symbol_table)
print(generator.instructions)
generator.write_to_file()