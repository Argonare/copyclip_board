from copy_board import Ui_MainWindow
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import tool

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setup()
    tool.check_init(ui)

    sys.exit(app.exec())
