# Other imports
import sys
import os

# Pyside imports
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTreeWidgetItem
from PySide6.QtGui import QIcon

# My imports
from helpers import resourcePath
from gui.ui_main import Ui_MainWindow


class SaunaMaraton(Ui_MainWindow):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.setupUi(self.window)
        self.path = None
        self.window.setWindowIcon(QIcon(resourcePath("app/assets/icons/sauna.ico")))

        self.team_names = []
        self.teams = []

        # Signals
        self.browse_btn.clicked.connect(self.browse_file)
        self.run_btn.clicked.connect(self.run_file)
        self.team_data_btn.clicked.connect(self.show_team_data)

    def show_team_data(self):
        current_selection = self.team_list.currentText()
        if current_selection:
            for team in self.teams:
                if current_selection in team:
                    print(team)
                    break
        else:
            QMessageBox.warning(self.window, "Error", "No team selected")

    def read_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                self.teams.append(line)

    def get_team_names(self, data):
        for team in data:
            team_name = team.split(";")[4]
            self.team_names.append(team_name)

    def insert_team_names_to_combobox(self):
        self.team_list.addItems(self.team_names)

    def insert_team_data_to_treeview(self):
        max_columns = max(len(team.split(";")) for team in self.teams)
        self.result_list.setColumnCount(max_columns)
        self.result_list.setHeaderLabels([f"Col {i + 1}" for i in range(max_columns)])
        for team in self.teams:
            columns = team.split(";")
            item = QTreeWidgetItem(columns)
            self.result_list.addTopLevelItem(item)
        self.result_list.setSortingEnabled(True)
        for col in range(max_columns):
            self.result_list.resizeColumnToContents(col)

    def run_file(self):
        if self.path:
            try:
                self.read_file(self.path)
                self.get_team_names(self.teams)
                self.insert_team_names_to_combobox()
                self.insert_team_data_to_treeview()

            except Exception as e:
                QMessageBox.warning(self.window, "Error", str(e))
        else:
            QMessageBox.warning(self.window, "Error", "File not found")

    def browse_file(self):
        self.path_lbl.clear()
        self.path, _ = QFileDialog.getOpenFileName(
            self.window, "Open File", "", "Text Files (*.txt);;All Files(*)"
        )
        self.path_lbl.setText(os.path.basename(self.path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    sauna_app = SaunaMaraton(window)
    window.show()
    sys.exit(app.exec())
