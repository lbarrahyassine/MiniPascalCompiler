class ASTNode:
    """Classe représentant un nœud dans l'arbre syntaxique abstrait."""
    def __init__(self, node_type, value=None):
        self.node_type = node_type  # Type de nœud (Program, VarDeclaration, Statement, etc.)
        self.value = value  # Valeur associée au nœud
        self.children = []  # Liste des enfants

    def add_child(self, child):
        """Ajoute un enfant au nœud."""
        self.children.append(child)

    def display(self, level=0):
        """Affiche l'arbre syntaxique abstrait de manière hiérarchique."""
        indent = "  " * level
        print(f"{indent}{self.node_type}: {self.value}")
        for child in self.children:
            child.display(level + 1)


class Parser:
    """Analyseur syntaxique pour un mini-compilateur Pascal."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        """Récupère le jeton actuel."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self, expected_type):
        """Consomme un jeton si son type correspond au type attendu."""
        token = self.current_token()
        if token and token["type"] == expected_type:
            self.position += 1
            return token
        raise ValueError(f"Erreur syntaxique : attendu {expected_type}, obtenu {token}")

    def parse_program(self):
        """Analyse un programme Pascal complet et retourne l'AST."""
        program_node = ASTNode("Program")
        self.consume("KEYWORD")  # 'program'
        program_name = self.consume("IDENTIFIER")  # Nom du programme
        program_node.value = program_name["value"]
        self.consume("DELIMITER")  # ';'

        # Analyse des déclarations de variables
        if self.current_token() and self.current_token()["value"] == "var":
            program_node.add_child(self.parse_vars())

        # Analyse du bloc principal
        program_node.add_child(self.parse_block())

        # Consomme le point final '.'
        self.consume("DELIMITER")

        return program_node

    def parse_vars(self):
        """Analyse la section des variables."""
        vars_node = ASTNode("Declarations")
        self.consume("KEYWORD")  # 'var'

        while self.current_token() and self.current_token()["type"] == "IDENTIFIER":
            var_declaration = ASTNode("VarDeclaration")
            while self.current_token() and self.current_token()["type"] == "IDENTIFIER":
                var_name = self.consume("IDENTIFIER")
                var_declaration.add_child(ASTNode("Variable", var_name["value"]))
                if self.current_token() and self.current_token()["value"] == ",":
                    self.consume("DELIMITER")  # Consomme ','
            self.consume("DELIMITER")  # Consomme ':'
            var_type = self.consume("KEYWORD")  # Type de la variable (integer, real, etc.)
            var_declaration.add_child(ASTNode("Type", var_type["value"]))
            self.consume("DELIMITER")  # Consomme ';'
            vars_node.add_child(var_declaration)

        return vars_node

    def parse_block(self):
        """Analyse un bloc BEGIN ... END."""
        block_node = ASTNode("Block")
        self.consume("KEYWORD")  # 'begin'
        block_node.add_child(self.parse_statements())
        self.consume("KEYWORD")  # 'end'
        return block_node

    def parse_statements(self):
        """Analyse une ou plusieurs instructions."""
        statements_node = ASTNode("Statements")

        while self.current_token() and self.current_token()["type"] != "KEYWORD":
            statements_node.add_child(self.parse_statement())

        return statements_node

    def parse_statement(self):
        """Analyse une instruction individuelle."""
        token = self.current_token()

        if token["type"] == "IDENTIFIER":  # Instruction d'affectation
            var_name = self.consume("IDENTIFIER")
            self.consume("OPERATOR")  # ':='
            expression = self.parse_expression()
            self.consume("DELIMITER")  # ';'
            assignment_node = ASTNode("Assignment", var_name["value"])
            assignment_node.add_child(expression)
            return assignment_node

        elif token["type"] == "KEYWORD" and token["value"] == "write":  # Instruction WRITE
            self.consume("KEYWORD")  # 'write'
            self.consume("DELIMITER")  # '('
            argument = self.consume("IDENTIFIER")  # Argument de write()
            self.consume("DELIMITER")  # ')'
            self.consume("DELIMITER")  # ';'
            return ASTNode("ProcedureCall", f"write({argument['value']})")

        else:
            raise ValueError(f"Instruction inconnue : {token}")

    def parse_expression(self):
        """Analyse une expression simple (nombre ou identifiant)."""
        token = self.current_token()
        if token["type"] == "NUMBER":
            return ASTNode("Value", self.consume("NUMBER")["value"])
        elif token["type"] == "IDENTIFIER":
            return ASTNode("Value", self.consume("IDENTIFIER")["value"])
        else:
            raise ValueError(f"Expression invalide : {token}")


# Exemple d'utilisation avec des jetons
source_code = """
program Example;
var x, y: integer;
begin
    x := 10;
    y := x + 20;
    write(y);
end.
"""

# Jetons générés par l'analyse lexicale
tokens = lexical_analyser(source_code)

# Analyse syntaxique
try:
    parser = Parser(tokens)
    ast = parser.parse_program()
    print("Analyse syntaxique réussie !")
    print("\nArbre syntaxique abstrait (AST) :")
    ast.display()
except ValueError as e:
    print(e)
