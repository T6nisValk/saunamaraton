import sys
import os
from datetime import datetime, timedelta

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTreeWidgetItem
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import Qt, QTime

from helpers import resourcePath
from gui.ui_main import Ui_MainWindow
from assets.saunas import sauna_pairs
from gui.border import CustomDelegate


class SaunaMaraton(Ui_MainWindow):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.setupUi(self.window)
        self.path = None
        self.window.setWindowIcon(QIcon(resourcePath("app/assets/icons/sauna.ico")))
        self.result_list.setItemDelegate(CustomDelegate())

        self.team_names = []
        self.teams = []
        self.team_sauna_data = {}

        self.browse_btn.clicked.connect(self.browse_file)
        self.run_btn.clicked.connect(self.run_file)
        self.team_data_btn.clicked.connect(self.show_team_data)
        self.export_btn.clicked.connect(self.export_to_text)

    def export_to_text(self):
        if self.result_list.topLevelItemCount() == 0:
            QMessageBox.warning(self.window, "Export Error", "No data to export.")
            return

        destination_dir = QFileDialog.getExistingDirectory(self.window, "Save to")
        if not destination_dir:
            return

        export_path = os.path.join(destination_dir, "result_list.txt")

        # Check if file exists and prompt for overwrite
        if os.path.exists(export_path):
            reply = QMessageBox.question(
                self.window,
                "File Exists",
                "The file 'result_list.txt' already exists.\nDo you want to overwrite it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return

        result_list = []

        # Extract headers
        column_count = self.result_list.columnCount()
        headers = [self.result_list.headerItem().text(col) for col in range(column_count)]
        result_list.append("\t".join(headers))

        # Extract data rows
        for i in range(self.result_list.topLevelItemCount()):
            item = self.result_list.topLevelItem(i)
            item_data = [item.text(col) for col in range(column_count)]
            result_list.append("\t".join(item_data))

        # Write to file
        with open(export_path, "w", encoding="utf-8") as f:
            for line in result_list:
                f.write(line + "\n")

        QMessageBox.information(self.window, "Export Successful", f"Data saved to:\n{export_path}")

    def show_team_data(self):
        current_selection = self.result_list.currentItem()
        if current_selection:
            team_name = current_selection.text(4)
            team_sauna_data = self.team_sauna_data[team_name]
            self.info_lbl.setText(f"{team_name}\n{team_sauna_data}")

        else:
            QMessageBox.warning(self.window, "Error", "No team selected")

    def read_file(self, path):
        with open(path, "r") as f:
            for line in f.readlines():
                self.teams.append(line)

    def save_sauna_times(self, team_name, team):
        sauna_times = team.split(";")[10:-1]
        sauna_times = sauna_times[:-1]
        sauna_times = [item for item in sauna_times if item != "?"]
        self.team_sauna_data[team_name] = sauna_times

    def get_headers(self):
        headers = [
            "Rinnanumber",
            "SI-Number",
            "Eesnimi",
            "Perenimi",
            "Tiimi nimi",
            "Mõõdetud raja aeg",
            "Punktid",
            "Stardi aeg",
            "Lõpu aeg",
            "Aeg+trahv-boonus",
        ]
        for sauna in sauna_pairs:
            headers.append(f"{sauna[0]}-{sauna[1]}")
        return headers

    def calculate_time_difference(self, start_time, end_time):
        if not start_time or not end_time:
            return None

        time_format = "%H:%M:%S"
        t1 = datetime.strptime(start_time, time_format)
        t2 = datetime.strptime(end_time, time_format)
        if t1 > t2:
            return None
        return t2 - t1

    def insert_sauna_times_to_tree(self, team_name):
        if team_name not in self.team_sauna_data:
            return

        sauna_times = self.team_sauna_data[team_name]
        sauna_results = {}
        unpaired_saunas = []
        bonus_saunas = {}

        for sauna_in, sauna_out in sauna_pairs:
            first_in_time = None
            last_out_time = None

            for i in range(0, len(sauna_times), 2):
                sauna_id = sauna_times[i]
                time_value = sauna_times[i + 1]

                if sauna_id == sauna_in and first_in_time is None:
                    first_in_time = time_value

                if sauna_id == sauna_out:
                    last_out_time = time_value

            duration = self.calculate_time_difference(first_in_time, last_out_time)
            if duration is None:
                sauna_results[f"{sauna_in}-{sauna_out}"] = "N/A"
            else:
                sauna_results[f"{sauna_in}-{sauna_out}"] = duration

        for i in range(0, len(sauna_times), 2):
            sauna_id = sauna_times[i]
            if sauna_id not in [s for pair in sauna_pairs for s in pair]:
                unpaired_saunas.append(sauna_id)
                bonus_saunas[sauna_id] = sauna_times[i + 1]

        headers = self.get_headers()

        for sauna_id in bonus_saunas.keys():
            bonus_header = f"{sauna_id}"
            if bonus_header not in headers:
                headers.append(bonus_header)

        self.result_list.setHeaderLabels(headers)

        for i in range(self.result_list.topLevelItemCount()):
            item = self.result_list.topLevelItem(i)
            if item.text(4) == team_name:
                for sauna_pair, duration in sauna_results.items():
                    col_index = headers.index(sauna_pair)
                    if duration == "N/A":
                        item.setForeground(col_index, QColor("red"))
                        item.setText(col_index, "N/A")
                    else:
                        item.setForeground(col_index, QColor("green"))
                        duration_str = str(duration)
                        item.setText(col_index, duration_str)

                for sauna_id, time in bonus_saunas.items():
                    bonus_column = f"{sauna_id}"
                    col_index = headers.index(bonus_column)
                    item.setText(col_index, time)
                    item.setForeground(col_index, QColor("yellow"))

    def insert_team_data_to_treeview(self):
        column_count = 9
        self.result_list.setColumnCount(column_count)

        headers = self.get_headers()

        bonus_saunas = set()
        for team in self.teams:
            team_info = team.split(";")[:10]
            final_time = team.split(";")[:-1][-1]
            del team_info[7]
            del team_info[5]
            team_info.append(final_time)
            item = QTreeWidgetItem(team_info)
            self.result_list.addTopLevelItem(item)

            team_name = team_info[4]
            self.save_sauna_times(team_name, team)

            self.insert_sauna_times_to_tree(team_name)

            sauna_times = self.team_sauna_data[team_name]
            for i in range(0, len(sauna_times), 2):
                sauna_id = sauna_times[i]
                if sauna_id not in [s for pair in sauna_pairs for s in pair]:
                    if sauna_id not in bonus_saunas:
                        headers.append(f"Bonus {sauna_id}")
                        bonus_saunas.add(sauna_id)

        self.result_list.setHeaderLabels(headers)

    def apply_bonuses_penalties(self):
        for i in range(self.result_list.topLevelItemCount()):
            item = self.result_list.topLevelItem(i)
            penalty_time = timedelta(seconds=0)

            for col in range(10, self.result_list.columnCount()):
                if item.foreground(col) == QColor("red"):
                    penalty_time += timedelta(minutes=15)
                elif item.foreground(col) == QColor("yellow"):
                    penalty_time -= timedelta(minutes=10)

            initial_time = item.text(5)
            initial_time = datetime.strptime(initial_time, "%H:%M:%S") - datetime(1900, 1, 1)
            end_time = initial_time + penalty_time

            # Convert timedelta to QTime
            end_qtime = QTime(end_time.seconds // 3600, (end_time.seconds % 3600) // 60, end_time.seconds % 60)

            # Store both text and QTime for proper sorting
            item.setText(9, end_qtime.toString("HH:mm:ss"))
            item.setData(9, Qt.UserRole, end_qtime)  # Store QTime for sorting

    def run_file(self):
        if self.path:
            try:
                self.result_list.clear()
                self.read_file(self.path)
                self.insert_team_data_to_treeview()
                self.apply_bonuses_penalties()
                for col in range(self.result_list.columnCount()):
                    self.result_list.resizeColumnToContents(col)
                self.result_list.setSortingEnabled(True)
                self.result_list.sortByColumn(9, Qt.AscendingOrder)
            except Exception as e:
                QMessageBox.warning(self.window, "Error", str(e))
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
