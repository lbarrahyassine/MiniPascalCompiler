class LexicalAnalyser:
    def __init__(self):
        # List of Pascal keywords
        self.KEYWORDS = ["program", "var", "integer", "string", "real", "begin", "end", "if", "then", "else",
                         "while", "do", "for", "to", "write", "read"]

        # List of operators and delimiters
        self.OPERATORS = [":=", "+", "-", "*", "/", "=", "<", ">", "<=", ">="]
        self.DELIMITERS = [";", ",", ".", "(", ")", ":"]

    def is_whitespace(self, char):
        """Checks if a character is a space, tab, or newline."""
        return char in " \t\n\r"

    def is_letter(self, char):
        """Checks if a character is a letter."""
        return char.isalpha()

    def is_digit(self, char):
        """Checks if a character is a digit."""
        return char.isdigit()

    def analyse(self, code):
        """Performs lexical analysis on the source code."""
        tokens = []
        i = 0
        length = len(code)

        while i < length:
            char = code[i]

            # Ignore whitespace
            if self.is_whitespace(char):
                i += 1
                continue

            # Identify keywords or identifiers
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

            # Identify numbers
            if self.is_digit(char):
                start = i
                while i < length and self.is_digit(code[i]):
                    i += 1
                number = code[start:i]
                tokens.append({"type": "NUMBER", "value": number, "position": i})
                continue

            # Identify strings
            if char in ['"', "'"]:
                quote_type = char
                start = i
                i += 1
                while i < length and code[i] != quote_type:
                    i += 1
                if i < length and code[i] == quote_type:
                    i += 1
                    string_value = code[start + 1:i - 1]
                    tokens.append({"type": "STRING", "value": string_value, "position": i})
                else:
                    raise ValueError(f"Error: Unclosed string at position {start}")
                continue

            # Identify operators
            if any(code[i:i + len(op)] == op for op in self.OPERATORS):
                for op in self.OPERATORS:
                    if code[i:i + len(op)] == op:
                        tokens.append({"type": "OPERATOR", "value": op, "position": i})
                        i += len(op)
                        break
                continue

            # Identify delimiters
            if char in self.DELIMITERS:
                tokens.append({"type": "DELIMITER", "value": char, "position": i})
                i += 1
                continue

            # Identify comments (ignore them)
            if char == "{":
                i += 1
                while i < length and code[i] != "}":
                    i += 1
                if i < length and code[i] == "}":
                    i += 1
                else:
                    raise ValueError(f"Error: Unclosed comment at position {i}")
                continue

            # If the character is not recognized
            raise ValueError(f"Lexical error: Invalid character '{char}' at position {i}")

        return tokens


source_code="""program programme1;
    var x,y: integer;
        a:string;
    begin
        x:=1;
    end.

"""

analyser = LexicalAnalyser()
tokens = analyser.analyse(source_code)
for item in tokens:
    print(item)