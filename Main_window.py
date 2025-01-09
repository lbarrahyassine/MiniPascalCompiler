import sys
from Interpreter import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QHBoxLayout,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QStackedWidget,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt



class CompilerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_output = ""
        self.current_symbol_table = {}
        self.ast_root = None

    def init_ui(self):
        self.setWindowTitle("Pascal Compiler")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("logo.png"))


        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)


        self.source_code_editor = QTextEdit()
        self.source_code_editor.setPlaceholderText("Write your code here...")
        self.source_code_editor.setStyleSheet("font: 12pt Courier;")

        # Stacked widget to toggle views
        self.display_stack = QStackedWidget()

        # Output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("font: 10pt Courier; background-color: #f5f5f5;")
        self.display_stack.addWidget(self.output_display)

        # Symbol table display as a table
        self.symbol_table_widget = QTableWidget()
        self.symbol_table_widget.setColumnCount(3)  # Name, Type, Address
        self.symbol_table_widget.setHorizontalHeaderLabels(["Name", "Type", "Address"])
        self.display_stack.addWidget(self.symbol_table_widget)

        # Tree widget for AST
        self.tree_display = QTreeWidget()
        self.tree_display.setHeaderLabel("Abstract Syntax Tree")
        self.display_stack.addWidget(self.tree_display)


        # Menu buttons
        menu_layout = QHBoxLayout()
        self.output_button = QPushButton("Output")
        self.output_button.setCheckable(True)
        self.output_button.setChecked(True)
        self.output_button.clicked.connect(self.show_output)

        self.symbol_table_button = QPushButton("Symbol Table")
        self.symbol_table_button.setCheckable(True)
        self.symbol_table_button.clicked.connect(self.show_symbol_table)

        self.tree_button = QPushButton("Tree")
        self.tree_button.setCheckable(True)
        self.tree_button.clicked.connect(self.show_tree)

        # Group buttons
        menu_layout.addWidget(self.output_button)
        menu_layout.addWidget(self.symbol_table_button)
        menu_layout.addWidget(self.tree_button)

        run_button = QPushButton("Run")
        run_button.setStyleSheet("font: 12pt; padding: 10px;")
        run_button.clicked.connect(self.run_program)

        # Add widgets to layout
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.source_code_editor)
        splitter.addWidget(self.display_stack)
        main_layout.addWidget(splitter)
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(run_button)

    def run_program(self):
        source_code = self.source_code_editor.toPlainText()
        try:
            output, symbol_table, ast_root = self.compiler_backend(source_code)
            self.current_output = output
            self.current_symbol_table = symbol_table
            self.ast_root = ast_root
            self.show_output()
        except Exception as e:
            self.output_display.setPlainText(f"Error: {str(e)}")

    def show_output(self):
        self.output_button.setChecked(True)
        self.symbol_table_button.setChecked(False)
        self.tree_button.setChecked(False)
        #self.graphical_tree_button.setChecked(False)
        self.display_stack.setCurrentWidget(self.output_display)
        self.output_display.setPlainText(self.current_output)

    def show_symbol_table(self):
        self.symbol_table_button.setChecked(True)
        self.output_button.setChecked(False)
        self.tree_button.setChecked(False)
        #self.graphical_tree_button.setChecked(False)
        self.display_stack.setCurrentWidget(self.symbol_table_widget)
        self.populate_symbol_table(self.current_symbol_table)

    def populate_symbol_table(self, symbol_table):
        self.symbol_table_widget.clearContents()
        self.symbol_table_widget.setRowCount(len(symbol_table))
        for row, (name, details) in enumerate(symbol_table.items()):
            var_type = details.get("type", "Unknown")
            address = details.get("address", "N/A")
            self.symbol_table_widget.setItem(row, 0, QTableWidgetItem(name))
            self.symbol_table_widget.setItem(row, 1, QTableWidgetItem(var_type))
            self.symbol_table_widget.setItem(row, 2, QTableWidgetItem(str(address)))

    def show_tree(self):
        self.tree_button.setChecked(True)
        self.output_button.setChecked(False)
        self.symbol_table_button.setChecked(False)
        #self.graphical_tree_button.setChecked(False)
        self.display_stack.setCurrentWidget(self.tree_display)
        self.populate_tree(self.ast_root)

    def populate_tree(self, node, parent_item=None):
        if node is None:
            return
        item = QTreeWidgetItem([f"{node.type}: {node.value or ''}"])
        if parent_item is None:
            self.tree_display.clear()
            self.tree_display.addTopLevelItem(item)
        else:
            parent_item.addChild(item)
        for child in node.children:
            self.populate_tree(child, item)


    def compiler_backend(self, source_code):
        if not source_code.strip():
            return "No source code to compile.", {}, None
        analyser = LexicalAnalyser()
        tokens = analyser.analyse(source_code)
        parser = Parser(tokens)
        ast_root = parser.inspect_program()
        semantic_analyzer = Semantic_analyzer(ast_root)
        semantic_analyzer.evaluate(ast_root)
        symbol_table = semantic_analyzer.symbol_table
        code_generator = CodeGenerator(ast_root, symbol_table)
        code_generator.generate_code(ast_root)
        assembly_code = code_generator.instructions
        interpreter = Interpreter(assembly_code, symbol_table)
        interpreter.execute()
        output = interpreter.outputs
        output_text = "\n".join(str(item) for item in output)
        return output_text, symbol_table, ast_root


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompilerInterface()
    window.show()
    sys.exit(app.exec_())
