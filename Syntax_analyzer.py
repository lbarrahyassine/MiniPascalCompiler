from Lexical_analyzer import *

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

    def inspect_program(self):
        program_node = ASTNode("Program")
        token = self.consume("KEYWORD")  # 'program'
        program_node.value = token["value"]
        program_node.position = token["position"]
        name_token = self.consume("IDENTIFIER")
        program_node.add_child(ASTNode("ProgramName", name_token["value"], position=name_token["position"]))
        self.consume("DELIMITER")  # ';'

        if self.current_token() and self.current_token()["value"] == "var":
            program_node.add_child(self.inspect_vars())

        program_node.add_child(self.inspect_block())
        self.consume("DELIMITER")  # '.'
        return program_node

    def inspect_vars(self):
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

    def inspect_block(self):
        block_node = ASTNode("Block")
        self.consume("KEYWORD")  # 'begin'
        block_node.add_child(self.inspect_statements())
        self.consume("KEYWORD")  # 'end'
        return block_node

    def inspect_statements(self):
        statements_node = ASTNode("Statements")
        while self.current_token() and not (
                self.current_token()["type"] == "KEYWORD" and self.current_token()["value"] == "end"):
            statements_node.add_child(self.inspect_statement())
        return statements_node

    def inspect_statement(self):
        token = self.current_token()

        if token["type"] == "IDENTIFIER":  # Handle assignment
            var_token = self.consume("IDENTIFIER")
            self.consume("OPERATOR")  # ':='
            expr_node = self.inspect_expression()
            self.consume("DELIMITER")  # ';'
            return ASTNode("Assignment", var_token["value"], [expr_node], position=var_token["position"])

        elif token["type"] == "KEYWORD" and token["value"] == "write":  # Handle write()
            return self.inspect_write()

        else:
            raise ValueError(f"Syntax Error: Unexpected statement at {token}")

    def inspect_write(self):
        write_token = self.consume("KEYWORD")  # 'write'
        self.consume("DELIMITER")  # '('
        expr_node = self.inspect_expression()  # Parse the expression inside `write()`
        self.consume("DELIMITER")  # ')'
        self.consume("DELIMITER")  # ';'
        return ASTNode("Write", None, [expr_node], position=write_token["position"])

    def inspect_expression(self):
        left = self.inspect_term()

        while self.current_token() and self.current_token()["type"] == "OPERATOR" and self.current_token()["value"] in (
                "+", "-"):
            operator_token = self.consume("OPERATOR")
            right = self.inspect_term()
            left = ASTNode("BinaryOperation", operator_token["value"], [left, right],
                           position=operator_token["position"])

        return left

    def inspect_term(self):
        """inspects a term with multiplication and division."""
        left = self.inspect_factor()

        while self.current_token() and self.current_token()["type"] == "OPERATOR" and self.current_token()["value"] in (
                "*", "/"):
            operator_token = self.consume("OPERATOR")
            right = self.inspect_factor()
            left = ASTNode("BinaryOperation", operator_token["value"], [left, right],
                           position=operator_token["position"])

        return left

    def inspect_factor(self):
        """Parses a single factor: a number, a variable, a grouped expression, or a string."""
        token = self.current_token()

        if token["type"] == "NUMBER":
            number_token = self.consume("NUMBER")
            return ASTNode("Number", number_token["value"], position=number_token["position"])

        elif token["type"] == "STRING":
            string_token = self.consume("STRING")
            return ASTNode("String", string_token["value"], position=string_token["position"])

        elif token["type"] == "IDENTIFIER":
            var_token = self.consume("IDENTIFIER")
            return ASTNode("Variable", var_token["value"], position=var_token["position"])

        elif token["type"] == "DELIMITER" and token["value"] == "(":
            self.consume("DELIMITER")  # '('
            expr = self.inspect_expression()
            self.consume("DELIMITER")  # ')'
            return expr

        else:
            raise ValueError(f"Invalid factor: {token}")

# Perform lexical analysis
analyser = LexicalAnalyser()
tokens = analyser.analyse(source_code)

# Parse and generate the AST
parser = Parser(tokens)
ast = parser.inspect_program()
ast.display()