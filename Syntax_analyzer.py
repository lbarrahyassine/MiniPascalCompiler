class Parser:
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
        """Analyse un programme complet."""
        self.consume("KEYWORD")  # 'program'
        self.consume("IDENTIFIER")  # Nom du programme
        self.consume("DELIMITER")  # ';'
        self.parse_block()
        self.consume("DELIMITER")  # '.'

    def parse_block(self):
        """Analyse un bloc BEGIN ... END."""
        self.consume("KEYWORD")  # 'begin'
        self.parse_statements()
        self.consume("KEYWORD")  # 'end'

    def parse_statements(self):
        """Analyse une ou plusieurs instructions."""
        while self.current_token() and self.current_token()["type"] != "KEYWORD":
            self.parse_statement()

    def parse_statement(self):
        """Analyse une instruction individuelle."""
        token = self.current_token()
        if token["type"] == "IDENTIFIER":  # Instruction d'affectation
            self.consume("IDENTIFIER")
            self.consume("OPERATOR")  # ':='
            self.parse_expression()
            self.consume("DELIMITER")  # ';'
        elif token["type"] == "KEYWORD" and token["value"] == "write":  # Instruction WRITE
            self.consume("KEYWORD")  # 'write'
            self.consume("DELIMITER")  # '('
            self.consume("IDENTIFIER")  # Identifiant dans write()
            self.consume("DELIMITER")  # ')'
            self.consume("DELIMITER")  # ';'
        else:
            raise ValueError(f"Instruction inconnue : {token}")

    def parse_expression(self):
        """Analyse une expression simple (par exemple un nombre ou un identifiant)."""
        token = self.current_token()
        if token["type"] == "NUMBER":
            self.consume("NUMBER")
        elif token["type"] == "IDENTIFIER":
            self.consume("IDENTIFIER")
        else:
            raise ValueError(f"Expression invalide : {token}")

"""
# Jetons générés par l'analyse lexicale
tokens = lexical_analyser(source_code)

# Analyse syntaxique
try:
    parser = Parser(tokens)
    parser.parse_program()
    print("Analyse syntaxique réussie !")
except ValueError as e:
    print(e)
"""