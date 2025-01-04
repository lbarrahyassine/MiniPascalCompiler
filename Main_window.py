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
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class CompilerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_output = ""
        self.current_symbol_table = ""
        self.ast_root = None  # For storing the AST

    def init_ui(self):
        # Set the main window properties
        self.setWindowTitle("Compiler Interface")
        self.setGeometry(100, 100, 800, 600)

        # Create the main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layouts
        main_layout = QVBoxLayout(main_widget)

        # Text editor for source code
        self.source_code_editor = QTextEdit()
        self.source_code_editor.setPlaceholderText("Write your source code here...")
        self.source_code_editor.setStyleSheet("font: 12pt Courier;")

        # Output display area
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("font: 10pt Courier; background-color: #f5f5f5;")

        # Tree widget for AST display
        self.tree_display = QTreeWidget()
        self.tree_display.setHeaderLabel("Abstract Syntax Tree")
        self.tree_display.setVisible(False)  # Initially hidden

        # Graphical tree display
        self.graphical_tree_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        self.graphical_tree_canvas.setVisible(False)

        # Menu buttons for toggling views
        menu_layout = QHBoxLayout()
        self.output_button = QPushButton("Output")
        self.output_button.setCheckable(True)
        self.output_button.setChecked(True)  # Default selection
        self.output_button.clicked.connect(self.show_output)

        self.symbol_table_button = QPushButton("Symbol Table")
        self.symbol_table_button.setCheckable(True)
        self.symbol_table_button.clicked.connect(self.show_symbol_table)

        self.tree_button = QPushButton("Tree")
        self.tree_button.setCheckable(True)
        self.tree_button.clicked.connect(self.show_tree)

        self.graphical_tree_button = QPushButton("Graphical Tree")
        self.graphical_tree_button.setCheckable(True)
        self.graphical_tree_button.clicked.connect(self.show_graphical_tree)

        # Group buttons and ensure only one is selected at a time
        menu_layout.addWidget(self.output_button)
        menu_layout.addWidget(self.symbol_table_button)
        menu_layout.addWidget(self.tree_button)
        menu_layout.addWidget(self.graphical_tree_button)

        # Run button
        run_button = QPushButton("Run")
        run_button.setStyleSheet("font: 12pt; padding: 10px;")
        run_button.clicked.connect(self.run_program)

        # Add widgets to layout
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.source_code_editor)
        splitter.addWidget(self.output_display)
        splitter.addWidget(self.tree_display)
        splitter.addWidget(self.graphical_tree_canvas)

        main_layout.addWidget(splitter)
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(run_button)

    def run_program(self):
        # Get the source code from the editor
        source_code = self.source_code_editor.toPlainText()

        # Simulate compiler backend call
        try:
            output, symbol_table, ast_root = self.compiler_backend(source_code)
            self.current_output = output
            self.current_symbol_table = symbol_table
            self.ast_root = ast_root
            self.show_output()  # Show the output by default
        except Exception as e:
            self.output_display.setPlainText(f"Error: {str(e)}")

    def show_output(self):
        # Display the compiled output
        self.output_button.setChecked(True)
        self.symbol_table_button.setChecked(False)
        self.tree_button.setChecked(False)
        self.graphical_tree_button.setChecked(False)
        self.output_display.setVisible(True)
        self.tree_display.setVisible(False)
        self.graphical_tree_canvas.setVisible(False)
        self.output_display.setPlainText(self.current_output)

    def show_symbol_table(self):
        # Display the symbol table
        self.symbol_table_button.setChecked(True)
        self.output_button.setChecked(False)
        self.tree_button.setChecked(False)
        self.graphical_tree_button.setChecked(False)
        self.output_display.setVisible(True)
        self.tree_display.setVisible(False)
        self.graphical_tree_canvas.setVisible(False)
        self.output_display.setPlainText(self.current_symbol_table)

    def show_tree(self):
        # Display the AST as a tree
        self.tree_button.setChecked(True)
        self.output_button.setChecked(False)
        self.symbol_table_button.setChecked(False)
        self.graphical_tree_button.setChecked(False)
        self.output_display.setVisible(False)
        self.tree_display.setVisible(True)
        self.graphical_tree_canvas.setVisible(False)
        self.populate_tree(self.ast_root)

    def populate_tree(self, node, parent_item=None):
        if node is None:
            return

        # Create a QTreeWidgetItem for the current node
        item = QTreeWidgetItem([f"{node.type}: {node.value or ''}"])
        if parent_item is None:
            self.tree_display.clear()
            self.tree_display.addTopLevelItem(item)
        else:
            parent_item.addChild(item)

        # Recursively add children
        for child in node.children:
            self.populate_tree(child, item)

    def show_graphical_tree(self):
        # Display the AST graphically
        self.graphical_tree_button.setChecked(True)
        self.output_button.setChecked(False)
        self.symbol_table_button.setChecked(False)
        self.tree_button.setChecked(False)
        self.output_display.setVisible(False)
        self.tree_display.setVisible(False)
        self.graphical_tree_canvas.setVisible(True)
        self.render_graphical_tree(self.ast_root)

    def render_graphical_tree(self, node, x=0, y=0, level=1, ax=None, dx=10):
        if node is None:
            return

        if ax is None:
            ax = self.graphical_tree_canvas.figure.add_subplot(111)
            ax.clear()
            ax.axis("off")

        # Draw the current node
        ax.text(
            x, y, node.type,
            ha="center", va="center",
            fontsize=8,
            bbox=dict(boxstyle="circle", facecolor="lightblue", edgecolor="black")
        )

        # Calculate positions for children
        num_children = len(node.children)
        if num_children > 0:
            child_dx = dx / num_children
            child_y = y - 2  # Distance between levels

            for i, child in enumerate(node.children):
                child_x = x - (dx / 2) + (i + 0.5) * child_dx
                # Draw connecting line
                ax.plot([x, child_x], [y - 0.5, child_y + 0.5], "k-", lw=1)
                # Recursively render child nodes
                self.render_graphical_tree(child, child_x, child_y, level + 1, ax, dx / 2)

        self.graphical_tree_canvas.draw()

    def compiler_backend(self, source_code):
        if not source_code.strip():
            return "No source code to compile.", "", None

        analyser = LexicalAnalyser()
        tokens = analyser.analyse(source_code)
        parser = Parser(tokens)
        ast_root = parser.parse_program()
        semantic_analyzer = Semantic_analyzer(ast_root)
        semantic_analyzer.evaluate(ast_root)
        symbol_table = semantic_analyzer.symbol_table
        code_generator = CodeGenerator(ast_root, symbol_table)
        code_generator.generate_code(ast_root)
        assembly_code = code_generator.instructions
        interpreter = Interpreter(assembly_code, symbol_table)
        interpreter.execute()
        output = interpreter.outputs

        # Format outputs
        output_text = "\n".join(str(item) for item in output)
        symbol_table_text = "\n".join(f"{key}: {value}" for key, value in symbol_table.items())

        return output_text, symbol_table_text, ast_root


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompilerInterface()
    window.show()
    sys.exit(app.exec_())
