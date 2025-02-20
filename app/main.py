# Other imports
import sys
import os

# Pyside imports
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

# My imports
from gui.ui_main import Ui_MainWindow


class SaunaMaraton(Ui_MainWindow):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.setupUi(self.window)
        self.path = None

        # Signals
        self.browse_btn.clicked.connect(self.browse_file)
        self.run_btn.clicked.connect(self.run_file)

    def run_file(self):
        if self.path:
            with open(self.path, "r") as f:
                for line in f.readlines():
                    print(line)
        else:
            QMessageBox.warning(self.window, "Error", "File not found")

    def browse_file(self):
        self.path_lbl.clear()
        self.path, _ = QFileDialog.getOpenFileName(self.window, "Open File", "", "Text Files (*.txt);;All Files(*)")
        self.path_lbl.setText(os.path.basename(self.path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    sauna_app = SaunaMaraton(window)
    window.show()
    sys.exit(app.exec())
