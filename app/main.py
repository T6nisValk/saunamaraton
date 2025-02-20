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
        self.team_sauna_data = {}

        # Signals
        self.browse_btn.clicked.connect(self.browse_file)
        self.run_btn.clicked.connect(self.run_file)
        self.team_data_btn.clicked.connect(self.show_team_data)

    def show_team_data(self):
        current_selection = self.result_list.currentItem()
        if current_selection:
            team_name = current_selection.text(4)
            print(team_name, self.team_sauna_data[team_name])
            sys.stdout.flush()

        else:
            QMessageBox.warning(self.window, "Error", "No team selected")

    def read_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                self.teams.append(line)

    def save_sauna_times(self, team_name, team):
        sauna_times = team.split(";")[10:-1]  # Get only sauna times
        sauna_times = sauna_times[:-1]  # Remove final time
        sauna_times = [item for item in sauna_times if item != "?"]  # Remove ?
        self.team_sauna_data[team_name] = sauna_times

    def insert_team_data_to_treeview(self):
        column_count = 9
        self.result_list.setColumnCount(column_count)
        self.result_list.setHeaderLabels(
            [
                "Rinnanumber",
                "SI-Number",
                "Eesnimi",
                "Perenimi",
                "Tiimi nimi",
                "Raja aeg",
                "Punktid",
                "Stardi aeg",
                "Lõpu aeg",
            ]
        )
        for team in self.teams:
            team_info = team.split(";")[:10]  # Remove sauna times
            final_time = team.split(";")[:-1][-1]  # Get final time
            del team_info[7]  # Remove C column
            del team_info[5]  # Remove VALIK
            team_info.append(final_time)  # Add final time to team info
            item = QTreeWidgetItem(team_info)
            self.result_list.addTopLevelItem(item)
            team_name = team_info[4]
            self.save_sauna_times(team_name, team)

        # Resize columns & sort
        self.result_list.setSortingEnabled(True)
        for col in range(column_count):
            self.result_list.resizeColumnToContents(col)

    def run_file(self):
        if self.path:
            try:
                self.read_file(self.path)
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
