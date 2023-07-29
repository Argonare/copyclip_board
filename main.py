from copy_board import Ui_MainWindow
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import tool

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("./static/style/main.css", "r") as f:
        app.setStyleSheet(f.read())

    ui = Ui_MainWindow()
    ui.setup()
    tool.check_init(ui)

    sys.exit(app.exec())
