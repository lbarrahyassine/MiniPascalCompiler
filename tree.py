class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def display(self, level=0):
        indent = "  " * level
        if self.value is not None:
            print(f"{indent}{self.node_type}: {self.value}")
        else:
            print(f"{indent}{self.node_type}")
        for child in self.children:
            child.display(level + 1)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self, expected_type=None):
        token = self.current_token()
        if token is None:
            raise ValueError("Unexpected end of input")

        if expected_type and token["type"] != expected_type:
            raise ValueError(f"Expected {expected_type}, but got {token}")

        self.position += 1
        return token

    def parse_program(self):
        program_node = ASTNode("Program", self.consume("KEYWORD")["value"])
        program_name = self.consume("IDENTIFIER")["value"]
        program_node.add_child(ASTNode("ProgramName", program_name))
        self.consume("DELIMITER")

        if self.current_token() and self.current_token()["value"] == "var":
            program_node.add_child(self.parse_declarations())

        program_node.add_child(self.parse_block())
        self.consume("DELIMITER")
        return program_node

    def parse_declarations(self):
        declarations_node = ASTNode("Declarations")
        self.consume("KEYWORD")  # 'var'
        while self.current_token() and self.current_token()["type"] == "IDENTIFIER":
            var_decl_node = ASTNode("VarDeclaration")
            var_name = self.consume("IDENTIFIER")["value"]
            var_decl_node.add_child(ASTNode("Variable", var_name))
            self.consume("DELIMITER")  # ':'
            var_type = self.consume("KEYWORD")["value"]
            var_decl_node.add_child(ASTNode("Type", var_type))
            self.consume("DELIMITER")  # ';'
            declarations_node.add_child(var_decl_node)
        return declarations_node

    def parse_block(self):
        block_node = ASTNode("Block")
        self.consume("KEYWORD")  # 'begin'
        while self.current_token() and self.current_token()["value"] != "end":
            block_node.add_child(self.parse_statement())
        self.consume("KEYWORD")  # 'end'
        return block_node

    def parse_statement(self):
        token = self.current_token()
        if token["type"] == "IDENTIFIER":
            return self.parse_assignment()
        elif token["type"] == "KEYWORD" and token["value"] == "write":
            return self.parse_procedure_call()
        else:
            raise ValueError(f"Unknown statement: {token}")

    def parse_assignment(self):
        assign_node = ASTNode("Assignment", self.consume("IDENTIFIER")["value"])
        self.consume("OPERATOR")  # ':='
        assign_node.add_child(self.parse_expression())
        self.consume("DELIMITER")  # ';'
        return assign_node

    def parse_procedure_call(self):
        proc_call_node = ASTNode("ProcedureCall", self.consume("KEYWORD")["value"])
        self.consume("DELIMITER")  # '('
        argument = self.consume("IDENTIFIER")["value"]
        arguments_node = ASTNode("Arguments")
        arguments_node.add_child(ASTNode("Variable", argument))
        proc_call_node.add_child(arguments_node)
        self.consume("DELIMITER")  # ')'
        self.consume("DELIMITER")  # ';'
        return proc_call_node

    def parse_expression(self):
        token = self.current_token()
        if token["type"] == "NUMBER":
            return ASTNode("Literal", self.consume("NUMBER")["value"])
        elif token["type"] == "IDENTIFIER":
            left_operand = ASTNode("Variable", self.consume("IDENTIFIER")["value"])
            if self.current_token() and self.current_token()["type"] == "OPERATOR":
                operator_node = ASTNode("BinaryOperation")
                operator_node.add_child(ASTNode("Operator", self.consume("OPERATOR")["value"]))
                operator_node.add_child(left_operand)
                operator_node.add_child(self.parse_expression())
                return operator_node
            return left_operand
        else:
            raise ValueError(f"Invalid expression: {token}")

# Example tokens from a lexical analyzer
tokens = [
    {"type": "KEYWORD", "value": "program"},
    {"type": "IDENTIFIER", "value": "Example"},
    {"type": "DELIMITER", "value": ";"},
    {"type": "KEYWORD", "value": "var"},
    {"type": "IDENTIFIER", "value": "x"},
    {"type": "DELIMITER", "value": ":"},
    {"type": "KEYWORD", "value": "integer"},
    {"type": "DELIMITER", "value": ";"},
    {"type": "IDENTIFIER", "value": "y"},
    {"type": "DELIMITER", "value": ":"},
    {"type": "KEYWORD", "value": "integer"},
    {"type": "DELIMITER", "value": ";"},
    {"type": "KEYWORD", "value": "begin"},
    {"type": "IDENTIFIER", "value": "x"},
    {"type": "OPERATOR", "value": ":="},
    {"type": "NUMBER", "value": "10"},
    {"type": "DELIMITER", "value": ";"},
    {"type": "IDENTIFIER", "value": "y"},
    {"type": "OPERATOR", "value": ":="},
    {"type": "IDENTIFIER", "value": "x"},
    {"type": "OPERATOR", "value": "+"},
    {"type": "NUMBER", "value": "20"},
    {"type": "DELIMITER", "value": ";"},
    {"type": "KEYWORD", "value": "write"},
    {"type": "DELIMITER", "value": "("},
    {"type": "IDENTIFIER", "value": "y"},
    {"type": "DELIMITER", "value": ")"},
    {"type": "DELIMITER", "value": ";"},
    {"type": "KEYWORD", "value": "end"},
    {"type": "DELIMITER", "value": "."},
]

# Parse and display the AST
try:
    parser = Parser(tokens)
    ast = parser.parse_program()
    ast.display()
except ValueError as e:
    print(e)
