import sys
from Interpreter import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QHBoxLayout,
    QSplitter,
)
from PyQt5.QtCore import Qt

class CompilerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set the main window properties
        self.setWindowTitle("Compiler Interface")
        self.setGeometry(100, 100, 800, 600)

        # Create the main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layouts
        layout = QVBoxLayout(main_widget)

        # Text editor for source code
        self.source_code_editor = QTextEdit()
        self.source_code_editor.setPlaceholderText("Write your source code here...")
        self.source_code_editor.setStyleSheet("font: 12pt Courier;")

        # Output display area
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("font: 10pt Courier; background-color: #f5f5f5;")

        # Run button
        run_button = QPushButton("Run")
        run_button.setStyleSheet("font: 12pt; padding: 10px;")
        run_button.clicked.connect(self.run_program)

        # Add widgets to layout
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.source_code_editor)
        splitter.addWidget(self.output_display)

        layout.addWidget(splitter)
        layout.addWidget(run_button)

    def run_program(self):
        # Get the source code from the editor
        source_code = self.source_code_editor.toPlainText()

        # Simulate compiler backend call
        try:
            output = self.compiler_backend(source_code)  # Replace with your backend function
            self.output_display.setPlainText(output)
        except Exception as e:
            self.output_display.setPlainText(f"Error: {str(e)}")

    def compiler_backend(self, source_code):
        if not source_code.strip():
            return "No source code to compile."
        analyser1 = LexicalAnalyser()
        tokens1 = analyser1.analyse(source_code)
        parser1 = Parser(tokens1)
        ast1 = parser1.parse_program()
        ast_verif1 = Semantic_analyzer(ast1)
        ast_verif1.evaluate(ast1)
        symbol_table1 = ast_verif1.symbol_table
        generator1 = CodeGenerator(ast1, symbol_table1)
        generator1.generate_code(ast1)
        assembly_code1=generator1.instructions
        interpreter1 = Interpreter(assembly_code1, symbol_table1)
        interpreter1.execute()
        outs=interpreter1.outputs
        output_text=''
        for item in outs:
            output_text+=str(item)+'\n'


        return f"Compiled Output:\n{output_text}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompilerInterface()
    window.show()
    sys.exit(app.exec_())
