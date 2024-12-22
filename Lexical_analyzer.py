class ASTNode:
    def __init__(self, type, value=None, children=None, position=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []
        self.position = position

    def add_child(self, child):
        self.children.append(child)

    def display(self, level=0):
        indent = "  " * level
        position_info = f" (position: {self.position})" if self.position is not None else ""
        print(f"{indent}{self.type}: {self.value}{position_info}")
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

    def consume(self, expected_type):
        token = self.current_token()
        if token and token["type"] == expected_type:
            self.position += 1
            return token
        raise ValueError(f"Syntax Error: Expected {expected_type}, got {token}")

    def parse_program(self):
        program_node = ASTNode("Program")
        token = self.consume("KEYWORD")  # 'program'
        program_node.value = token["value"]
        program_node.position = token["position"]
        name_token = self.consume("IDENTIFIER")
        program_node.add_child(ASTNode("ProgramName", name_token["value"], position=name_token["position"]))
        self.consume("DELIMITER")  # ';'

        if self.current_token() and self.current_token()["value"] == "var":
            program_node.add_child(self.parse_vars())

        program_node.add_child(self.parse_block())
        self.consume("DELIMITER")  # '.'
        return program_node

    def parse_vars(self):
        vars_node = ASTNode("Declarations")
        self.consume("KEYWORD")  # 'var'

        while self.current_token() and self.current_token()["type"] == "IDENTIFIER":
            var_decl_node = ASTNode("VarDeclaration")
            while self.current_token() and self.current_token()["type"] == "IDENTIFIER":
                var_token = self.consume("IDENTIFIER")
                var_decl_node.add_child(ASTNode("Variable", var_token["value"], position=var_token["position"]))
                if self.current_token() and self.current_token()["value"] == ",":
                    self.consume("DELIMITER")
                else:
                    break
            self.consume("DELIMITER")  # ':'
            type_token = self.consume("KEYWORD")
            var_decl_node.add_child(ASTNode("Type", type_token["value"], position=type_token["position"]))
            self.consume("DELIMITER")  # ';'
            vars_node.add_child(var_decl_node)

        return vars_node

    def parse_block(self):
        block_node = ASTNode("Block")
        self.consume("KEYWORD")  # 'begin'
        block_node.add_child(self.parse_statements())
        self.consume("KEYWORD")  # 'end'
        return block_node

    def parse_statements(self):
        statements_node = ASTNode("Statements")
        while self.current_token() and self.current_token()["type"] != "KEYWORD":
            statements_node.add_child(self.parse_statement())
        return statements_node

    def parse_statement(self):
        token = self.current_token()

        if token["type"] == "IDENTIFIER":
            var_token = self.consume("IDENTIFIER")
            self.consume("OPERATOR")  # ':='
            expr_node = self.parse_expression()
            self.consume("DELIMITER")  # ';'
            return ASTNode("Assignment", var_token["value"], [expr_node], position=var_token["position"])

        elif token["type"] == "KEYWORD" and token["value"] == "write":
            write_token = self.consume("KEYWORD")
            self.consume("DELIMITER")  # '('
            var_token = self.consume("IDENTIFIER")
            self.consume("DELIMITER")  # ')'
            self.consume("DELIMITER")  # ';'
            return ASTNode("ProcedureCall", f"write({var_token['value']})", position=write_token["position"])

        else:
            raise ValueError(f"Unknown statement: {token}")

    def parse_expression(self):
        token = self.current_token()

        if token["type"] == "NUMBER":
            number_token = self.consume("NUMBER")
            return ASTNode("Number", number_token["value"], position=number_token["position"])

        elif token["type"] == "IDENTIFIER":
            var_token = self.consume("IDENTIFIER")
            return ASTNode("Variable", var_token["value"], position=var_token["position"])

        else:
            raise ValueError(f"Invalid expression: {token}")

# Example usage
source_code = """
program Example;
var x, y: integer;
begin
    x := 10;
    y := x + 20;
    write(y);
end.
"""

def lexical_analyser(code):
    # Placeholder for the actual lexical analyser implementation
    return [
        {"type": "KEYWORD", "value": "program", "position": 0},
        {"type": "IDENTIFIER", "value": "Example", "position": 8},
        {"type": "DELIMITER", "value": ";", "position": 15},
        {"type": "KEYWORD", "value": "var", "position": 17},
        {"type": "IDENTIFIER", "value": "x", "position": 21},
        {"type": "DELIMITER", "value": ",", "position": 22},
        {"type": "IDENTIFIER", "value": "y", "position": 24},
        {"type": "DELIMITER", "value": ":", "position": 25},
        {"type": "KEYWORD", "value": "integer", "position": 27},
        {"type": "DELIMITER", "value": ";", "position": 34},
        {"type": "KEYWORD", "value": "begin", "position": 36},
        {"type": "IDENTIFIER", "value": "x", "position": 42},
        {"type": "OPERATOR", "value": ":=", "position": 44},
        {"type": "NUMBER", "value": "10", "position": 47},
        {"type": "DELIMITER", "value": ";", "position": 49},
        {"type": "IDENTIFIER", "value": "y", "position": 51},
        {"type": "OPERATOR", "value": ":=", "position": 53},
        {"type": "IDENTIFIER", "value": "x", "position": 56},
        {"type": "DELIMITER", "value": ";", "position": 57},
        {"type": "KEYWORD", "value": "write", "position": 59},
        {"type": "DELIMITER", "value": "(", "position": 64},
        {"type": "IDENTIFIER", "value": "y", "position": 65},
        {"type": "DELIMITER", "value": ")", "position": 66},
        {"type": "DELIMITER", "value": ";", "position": 67},
        {"type": "KEYWORD", "value": "end", "position": 69},
        {"type": "DELIMITER", "value": ".", "position": 72}
    ]

# Perform lexical analysis
tokens = lexical_analyser(source_code)

# Parse and generate the AST
parser = Parser(tokens)
ast = parser.parse_program()
ast.display()