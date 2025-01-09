from Syntax_analyzer import *

class Semantic_analyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}

    def evaluate(self, node):
        if node.type == "ProgramName":
            pass

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
                var_list = []

                for child in declaration.children:
                    if child.type == "Variable":
                        var_list.append(child.value)
                    elif child.type == "Type":
                        var_type = child.value
                        for variable in var_list:
                            self.symbol_table[variable] = {
                                "type": var_type,
                                "address": adr,
                                # "value": None
                            }
                            adr += 1
                        var_list = []
                        var_type = None
                    elif var_type is None:
                        raise ValueError(f"Type not declared for variable {var_list}")

        elif node.type == "Assignment":
            var_name = node.value
            if var_name not in self.symbol_table:
                raise ValueError(f"Variable {var_name} is not declared")

            expected_type = self.symbol_table[var_name]["type"]
            assigned_node = node.children[0]
            assigned_type = self.get_node_type(assigned_node)

            # Type check
            if expected_type != assigned_type:
                raise TypeError(
                    f"Type error: Cannot assign {assigned_type} to {expected_type} variable {var_name}"
                )
            for child in node.children:
                self.evaluate(child)

        elif node.type == "BinaryOperation":
            left_type = self.get_node_type(node.children[0])
            right_type = self.get_node_type(node.children[1])
            operator = node.value

            # Type check
            if operator in ("+", "-","*","/"):
                if left_type != "integer" or right_type != "integer":
                    raise TypeError(
                        f"Type error: Cannot apply operator {operator} to non-integer operands"
                    )
                if operator == "/":
                    if node.children[1].type =="Number":
                        if int(node.children[1].value) == 0:
                            raise ZeroDivisionError("Semantic error: Division by zero")

            elif operator == "+":
                # Allow string concatenation
                if left_type == "string" and right_type == "string":
                    return "string"
                else:
                    raise TypeError(
                        f"Type error: Operator '+' requires both operands to be strings or integers"
                    )



        elif node.type == "Number":
            return "integer"

        elif node.type == "String":
            return "string"

        elif node.type == "Variable":
            if node.value not in self.symbol_table:
                raise ValueError(f"Variable {node.value} is not declared")
            return self.symbol_table[node.value]["type"]

        elif node.type == "Write":
            # Ensure the argument type is either integer or string
            expr_type = self.get_node_type(node.children[0])
            if expr_type not in ("integer", "string"):
                raise TypeError(
                    f"Type error: write() only supports integer or string arguments, got {expr_type}"
                )

        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def get_node_type(self, node):
        if node.type == "Number":
            return "integer"
        elif node.type == "String":
            return "string"
        elif node.type == "Variable":
            if node.value not in self.symbol_table:
                raise ValueError(f"Variable {node.value} is not declared")
            return self.symbol_table[node.value]["type"]
        elif node.type == "BinaryOperation":
            left_type = self.get_node_type(node.children[0])
            right_type = self.get_node_type(node.children[1])

            if left_type == "integer" and right_type == "integer":
                return "integer"
            elif left_type == "string" and right_type == "string":
                return "string"
            else:
                raise TypeError(
                    f"Type error in binary operation with types {left_type} and {right_type}"
                )
        else:
            raise ValueError(f"Unsupported node type for type checking: {node.type}")


parser = Parser(tokens)
ast_root = parser.inspect_program()
semantic_analyzer = Semantic_analyzer(ast_root)
semantic_analyzer.evaluate(ast_root)
symbol_table = semantic_analyzer.symbol_table
print(symbol_table)