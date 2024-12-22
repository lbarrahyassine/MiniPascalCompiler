class LexicalAnalyser:
    def __init__(self):
        # Liste des mots-clés de Pascal
        self.KEYWORDS = ["program", "var", "integer", "real", "begin", "end", "if", "then", "else",
                         "while", "do", "for", "to", "write", "read"]

        # Liste des opérateurs et délimiteurs
        self.OPERATORS = [":=", "+", "-", "*", "/", "=", "<", ">", "<=", ">="]
        self.DELIMITERS = [";", ",", ".", "(", ")", ":"]

    def is_whitespace(self, char):
        """Vérifie si un caractère est un espace, une tabulation ou une nouvelle ligne."""
        return char in " \t\n\r"

    def is_letter(self, char):
        """Vérifie si un caractère est une lettre."""
        return char.isalpha()

    def is_digit(self, char):
        """Vérifie si un caractère est un chiffre."""
        return char.isdigit()

    def analyse(self, code):
        """Analyse lexicale du code source."""
        tokens = []
        i = 0
        length = len(code)

        while i < length:
            char = code[i]

            # Ignorer les espaces blancs
            if self.is_whitespace(char):
                i += 1
                continue

            # Identifier les mots-clés ou identifiants
            if self.is_letter(char):
                start = i
                while i < length and (self.is_letter(code[i]) or self.is_digit(code[i])):
                    i += 1
                word = code[start:i]
                if word in self.KEYWORDS:
                    tokens.append({"type": "KEYWORD", "value": word, "position": i})
                else:
                    tokens.append({"type": "IDENTIFIER", "value": word, "position": i})
                continue

            # Identifier les nombres
            if self.is_digit(char):
                start = i
                while i < length and self.is_digit(code[i]):
                    i += 1
                number = code[start:i]
                tokens.append({"type": "NUMBER", "value": number, "position": i})
                continue

            # Identifier les opérateurs
            if any(code[i:i + len(op)] == op for op in self.OPERATORS):
                for op in self.OPERATORS:
                    if code[i:i + len(op)] == op:
                        tokens.append({"type": "OPERATOR", "value": op, "position": i})
                        i += len(op)
                        break
                continue

            # Identifier les délimiteurs
            if char in self.DELIMITERS:
                tokens.append({"type": "DELIMITER", "value": char, "position": i})
                i += 1
                continue

            # Identifier les commentaires
            if char == "{":
                start = i
                i += 1
                while i < length and code[i] != "}":
                    i += 1
                if i < length and code[i] == "}":
                    i += 1
                    tokens.append({"type": "COMMENT", "value": code[start:i], "position": i})
                else:
                    raise ValueError(f"Erreur : Commentaire non fermé à la position {start}")
                continue

            # Si le caractère n'est pas reconnu
            raise ValueError(f"Erreur lexicale : caractère non valide '{char}' à la position {i}")

        return tokens


# Exemple d'utilisation
if __name__ == "__main__":
    source_code = """
    program Example;
    var x, y: integer;
    begin
        x := 10;
        y := x + 20;
        write(y);
    end.
    """

    analyser = LexicalAnalyser()

    try:
        tokens = analyser.analyse(source_code)
        for token in tokens:
            print(token)
    except ValueError as e:
        print(e)
