# Other imports
import sys
import os
from datetime import datetime, timedelta

# Pyside imports
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTreeWidgetItem
from PySide6.QtGui import QIcon, QColor

# My imports
from helpers import resourcePath
from gui.ui_main import Ui_MainWindow
from assets.saunas import sauna_pairs


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
        """Convert times to timedelta, compute difference, return timedelta or None."""
        if not start_time or not end_time:
            return None  # If missing times, return None

        time_format = "%H:%M:%S"
        t1 = datetime.strptime(start_time, time_format)
        t2 = datetime.strptime(end_time, time_format)
        return t2 - t1  # Returns timedelta

    def insert_sauna_times_to_tree(self, team_name):
        if team_name not in self.team_sauna_data:
            return

        sauna_times = self.team_sauna_data[team_name]
        sauna_results = {}  # Store sauna times
        penalty_time = timedelta(seconds=0)  # Track penalty time
        penalty_threshold = timedelta(minutes=2, seconds=55)

        for sauna_in, sauna_out in sauna_pairs:
            first_in_time = None
            last_out_time = None

            for i in range(0, len(sauna_times), 2):
                sauna_id = sauna_times[i]
                time_value = sauna_times[i + 1]

                if sauna_id == sauna_in and first_in_time is None:
                    first_in_time = time_value  # First entry

                if sauna_id == sauna_out:
                    last_out_time = time_value  # Last exit

            duration = self.calculate_time_difference(first_in_time, last_out_time)
            if duration:
                sauna_results[f"{sauna_in}-{sauna_out}"] = duration

                # Apply 15s penalty if time is under 2:55
                if duration < penalty_threshold:
                    penalty_time += timedelta(seconds=15)

        # Find the row for this team
        for i in range(self.result_list.topLevelItemCount()):
            item = self.result_list.topLevelItem(i)
            if item.text(4) == team_name:  # Column 4 is team name
                headers = self.get_headers()
                for sauna_pair, duration in sauna_results.items():
                    col_index = headers.index(sauna_pair)
                    duration_str = str(duration)
                    item.setText(col_index, duration_str)

                    # Set text color to red if under 2:55
                    if duration < penalty_threshold:
                        item.setForeground(col_index, QColor("red"))

                # Update "Mõõdetud raja aeg" with penalty
                measured_time = item.text(5)  # "Mõõdetud raja aeg" column
                if measured_time:
                    original_time = datetime.strptime(measured_time, "%H:%M:%S")
                    new_time = original_time + penalty_time
                    item.setText(9, new_time.strftime("%H:%M:%S"))  # "Aeg+trahv-boonus"

    def insert_team_data_to_treeview(self):
        column_count = 9
        self.result_list.setColumnCount(column_count)

        headers = self.get_headers()
        self.result_list.setHeaderLabels(headers)

        for team in self.teams:
            team_info = team.split(";")[:10]  # Remove sauna times
            final_time = team.split(";")[:-1][-1]  # Get final time
            del team_info[7]  # Remove C column
            del team_info[5]  # Remove VALIK
            team_info.append(final_time)  # Add final time to team info
            item = QTreeWidgetItem(team_info)
            self.result_list.addTopLevelItem(item)

            # Save times to dict
            team_name = team_info[4]
            self.save_sauna_times(team_name, team)

            # Sort times and calculate difference then add to tree
            self.insert_sauna_times_to_tree(team_name)

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
