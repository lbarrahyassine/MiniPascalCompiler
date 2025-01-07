from Semantic_analyzer import *

class CodeGenerator:
    def __init__(self, ast, symbol_table, output_file="output.txt"):
        self.ast = ast
        self.symbol_table = symbol_table
        self.instructions = []
        self.output_file = output_file
        self.current_label = 0

    def new_label(self):
        """Generate a new unique label."""
        self.current_label += 1
        return f"L{self.current_label}"

    def format_address(self, address):
        """Format the address as `$0000`, `$0001`, etc."""
        return f"${address:04X}"

    def generate_code(self, node):
        if node.type == "ProgramName":
            # Add a comment with the program name
            self.instructions.append(f"; Program: {node.value}\n")

        elif node.type == "Program":
            for child in node.children:
                self.generate_code(child)

        elif node.type == "Declarations":
            # Variable declarations (not needed for assembly code generation)
            pass

        elif node.type == "Block":
            # Generate code for statements in the block
            for child in node.children:
                self.generate_code(child)

        elif node.type == "Statements":
            # Generate code for each statement
            for child in node.children:
                self.generate_code(child)

        elif node.type == "Assignment":
            # Generate code for assignment
            var_name = node.value
            expression_code = self.generate_expression(node.children[0])
            self.instructions.extend(expression_code)
            variable_address = self.format_address(self.symbol_table[var_name]["address"])
            self.instructions.append(f"MOV {variable_address}, AX\n")

        elif node.type == "Write":
            # Generate code for write (output)
            expr_node = node.children[0]
            expr_type = self.symbol_table[expr_node.value]["type"] if expr_node.type == "Variable" else self.get_node_type(expr_node)

            if expr_type == "integer":
                # Handle integer output
                expr_code = self.generate_expression(expr_node)
                self.instructions.extend(expr_code)
                self.instructions.append("OUT AX\n")
            elif expr_type == "string":
                # Handle string output
                if expr_node.type == "Variable":
                    variable_address = self.format_address(self.symbol_table[expr_node.value]["address"])
                    self.instructions.append(f"OUT_STR {variable_address}\n")
                elif expr_node.type == "String":
                    self.instructions.append(f'OUT_STR "{expr_node.value}"\n')

    def generate_expression(self, node):
        """Generate assembly code for an expression."""
        if node.type == "Number":
            return [f"MOV AX, {node.value}\n"]

        elif node.type == "String":
            # Load string literal into a specific register or memory
            return [f'MOV AX, "{node.value}"\n']

        elif node.type == "Variable":
            variable_address = self.format_address(self.symbol_table[node.value]["address"])
            return [f"MOV AX, {variable_address}\n"]

        elif node.type == "BinaryOperation":
            left_code = self.generate_expression(node.children[0])
            right_code = self.generate_expression(node.children[1])
            operator = node.value

            if operator == "+":
                # Handle string concatenation or integer addition
                left_type = self.get_node_type(node.children[0])
                right_type = self.get_node_type(node.children[1])
                if left_type == "string" and right_type == "string":
                    # String concatenation
                    code = left_code
                    code.append("PUSH AX\n")  # Save left string
                    code.extend(right_code)
                    code.append("POP BX\n")  # Retrieve left string
                    code.append("CONCAT AX, BX\n")  # Concatenate strings
                    return code
                elif left_type == "integer" and right_type == "integer":
                    # Integer addition
                    code = left_code
                    code.append("PUSH AX\n")  # Save left value
                    code.extend(right_code)
                    code.append("POP BX\n")  # Retrieve left value
                    code.append("ADD AX, BX\n")  # Add integers
                    return code
                else:
                    raise ValueError("Type mismatch in binary operation")

            elif operator == "*":
                # Handle integer multiplication
                code = left_code
                code.append("PUSH AX\n")  # Save left value
                code.extend(right_code)
                code.append("POP BX\n")  # Retrieve left value
                code.append("MUL AX, BX\n")  # Multiply integers
                return code

            else:
                raise ValueError(f"Unsupported operator: {operator}")

        else:
            raise ValueError(f"Unsupported node type for expression: {node.type}")

    def get_node_type(self, node):
        """Get the type of a node."""
        if node.type == "Number":
            return "integer"
        elif node.type == "String":
            return "string"
        elif node.type == "Variable":
            return self.symbol_table[node.value]["type"]
        elif node.type == "BinaryOperation":
            left_type = self.get_node_type(node.children[0])
            right_type = self.get_node_type(node.children[1])
            if left_type == right_type:
                return left_type
            else:
                raise ValueError(f"Type mismatch in binary operation: {left_type} vs {right_type}")

    def write_to_file(self):
        """Write the generated instructions to the output file."""
        with open(self.output_file, "w") as f:
            f.writelines(self.instructions)


