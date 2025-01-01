from Syntax_analyzer import *
class Semantic_analyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}
        self.memory = {}

    def evaluate(self, node):
        if node.type == "ProgramName":
            # Handle the ProgramName node
            print(f"Processing program name: {node.value}")

        elif node.type == "Program":
            for child in node.children:
                self.evaluate(child)

        elif node.type == "Block":
            for child in node.children:
                self.evaluate(child)

        elif node.type == "Statements":
            for child in node.children:
                self.evaluate(child)
        elif node.type == "Declarations":
            adr = 0
            for declaration in node.children:
                var_type = None
                var_list=[]

                for child in declaration.children:

                    if child.type == "Variable":
                        var_list.append(child.value)
                    elif child.type == "Type":
                        var_type=child.value
                        for variable in var_list:

                            self.symbol_table[variable] = {"type": var_type, "address": adr,"value": None}
                            adr+=1
                        var_list = []

                        var_type = None
                    elif var_type is None:
                        raise ValueError(f"Type not declared for variable {var_list}")


        elif node.type == "Assignment":
            var_name = node.value
            if var_name not in self.symbol_table:
                raise ValueError(f"Variable {var_name} is not declared")

            expected_type = self.symbol_table[var_name]["type"]
            assigned_value = self.evaluate(node.children[0])
            assigned_type = type(assigned_value).__name__

            # Type check
            if expected_type == "integer" and not isinstance(assigned_value, int):
                raise TypeError(f"Type error: Cannot assign {assigned_type} to {expected_type} variable {var_name}")
            elif expected_type == "string" and not isinstance(assigned_value, str):
                raise TypeError(f"Type error: Cannot assign {assigned_type} to {expected_type} variable {var_name}")

            # Update symbol table
            self.symbol_table[var_name]["value"] = assigned_value

        elif node.type == "BinaryOperation":
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])
            operator = node.value

            # Type check
            if not isinstance(left, int) or not isinstance(right, int):
                raise TypeError(f"Type error: Cannot apply operator {operator} to non-integer operands")

            # Perform operation
            if operator == "+":
                return left + right
            elif operator == "*":
                return left * right
            else:
                raise ValueError(f"Unknown operator {operator}")

        elif node.type == "Number":
            return int(node.value)

        elif node.type == "Variable":
            if node.value not in self.symbol_table:
                raise ValueError(f"Variable {node.value} is not declared")
            return self.symbol_table[node.value]["value"]

        else:
            raise ValueError(f"Unknown node type: {node.type}")



interpreter = Semantic_analyzer(ast)
interpreter.evaluate(ast)
print(interpreter.symbol_table)
