from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox


class SaunaMarathon:
    def __init__(self):
        self.sauna_punktid = [
    "11","12","21","22","31","32","41","42","51","52","61","62","71","72",
    "81","82","91","92","101","102","111","112","121","122","131","132",
    "141","142","151","152","161","162","171","172","181","182",
]
        self.data_list = []

        self.combobox_items = []
        
        self.root = tk.Tk()
        self.root.geometry("800x700")
        self.root.title("Saunamaraton")

        self.frame_grid = tk.Frame(self.root)
        self.frame_grid.pack(pady=5)
        
        self.browse_entry_text = tk.StringVar()
        self.browse_frame = tk.Frame(self.frame_grid)
        self.browse_frame.grid(row=0, column=0)
        
        self.browse_label = tk.Label(self.browse_frame, text="Faili asukoht: ")
        self.browse_label.grid(row=0, column=0, padx=5)
        
        self.browse_entry = tk.Entry(self.browse_frame, textvariable=self.browse_entry_text)
        self.browse_entry.grid(row=0, column=1, pady=5)

        self.browse_button = tk.Button(self.browse_frame, text="Browse", command=lambda: self.browse_file())
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.confirm_button = tk.Button(self.browse_frame, text="Run", command=lambda: self.process_data(self.browse_entry.get()))
        self.confirm_button.grid(row=0, column=3)
        
        self.individual_data_frame = tk.Frame(self.frame_grid)
        self.individual_data_frame.grid(row=0, column=1)
        
        self.individual_label = tk.Label(self.individual_data_frame, text="Meeskonna andmed: ")
        self.individual_label.grid(row=1, column=0)
        
        self.combobox = ttk.Combobox(self.individual_data_frame, values=self.combobox_items)
        self.combobox.set("Vali meeskond")
        self.combobox.grid(row=1, column=1, pady=5)
        
        self.combobox_button = tk.Button(self.individual_data_frame, text="Run", command=lambda: self.individual_team())
        self.combobox_button.grid(row=1, column=2, padx=5)

        self.data_frame = tk.Frame(self.frame_grid)
        self.data_frame.grid(row=1, column=0, columnspan=2)
        
        self.main_label = tk.Label(self.data_frame, text="TULEMUSED", font="Bold")
        self.main_label.pack(pady=5)

        self.text_box = tk.Text(self.data_frame, height=35, width=80)
        self.text_box.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.data_frame, command=self.text_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_box.config(yscrollcommand=self.scrollbar.set)

    def individual_team(self):
        index = self.combobox.get().split(".")[0]
        data = self.data_list[int(index)-1]
        team_data = tk.Tk()
        team_data.geometry("700x550")
        team_data.title(f"{data["Tiimi nimi"]}")
        
        data_frame = tk.Frame(team_data)
        data_frame.pack(padx=5, pady=5)
        text_box = tk.Text(team_data, height=35, width=80)
        text_box.pack(side=tk.LEFT, padx=5)

        scrollbar = tk.Scrollbar(team_data, command=self.text_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_box.config(yscrollcommand=scrollbar.set)
        tehtud_punktid = [f"\n\t{key}: {value}" for key, value in data["Sauna punktid"][0].items()]
        data_to_insert = (
                f"Rinnanumber: {data['Rinnanumber']} \
                \nSI-Pulga nr: {data['SI-Pulga nr']} \
                \nEesnimi: {data['Eesnimi']} \
                \nPerenimi: {data['Perenimi']} \
                \nTiimi nimi: {data['Tiimi nimi']} \
                \nKlass: {data['Klass']} \
                \nStardiaeg: {data['Stardiaeg']} \
                \nLõpuaeg: {data['Lõpuaeg']} \
                \nKogu aeg: {data['Kogu aeg']}\
                \nVõetud punktid: {data['Võetud punktid']} \
                \nTehtud punktid: \n{''.join(tehtud_punktid)}\n\n\n"
            )
        text_box.insert(tk.END, data_to_insert)
        team_data.mainloop()
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        self.browse_entry_text.set(file_path)
        
    def calculate_time_difference(self, start_time, end_time):
        format_str = "%H:%M:%S"
        start_datetime = datetime.strptime(start_time, format_str)
        end_datetime = datetime.strptime(end_time, format_str)
        time_difference = end_datetime - start_datetime
        return time_difference

    def calculate_specific_sauna_punktid_time_difference(self, sauna_punktid_dict):
        pairs_to_calculate = [
            ("11", "12"),
            ("21", "22"),
            ("31", "32"),
            ("41", "42"),
            ("51", "52"),
            ("61", "62"),
            ("71", "72"),
            ("81", "82"),
            ("91", "92"),
            ("101", "102"),
            ("111", "112"),
            ("121", "122"),
            ("131", "132"),
            ("141", "142"),
            ("151", "152"),
            ("161", "162"),
            ("171", "172"),
            ("181", "182"),
        ]

        time_difference_dict = {}
        points_not_done = []

        for start_point, end_point in pairs_to_calculate:
            start_times = [time for point, time in sauna_punktid_dict.items() if point == start_point]
            end_times = [time for point, time in sauna_punktid_dict.items() if point == end_point]

            if start_times and end_times:
                start_time = start_times[0]
                end_time = end_times[-1]
                time_difference = self.calculate_time_difference(start_time, end_time)
                time_difference_dict[f"{start_point}-{end_point}"] = str(time_difference)
            else:
                points_not_done.append(f"{start_point}-{end_point}")

        return time_difference_dict, points_not_done

    def process_data(self, file_path):
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found.")
        self.text_box.delete(1.0, tk.END)
        for index, line in enumerate(lines):
            data = [item for item in line.strip("\n").split(";") if item not in ["", "?"]]
            punktid_ajad = data[10:-1]
            punktid_ajad_dict = {
                punktid_ajad[i]: punktid_ajad[i + 1]
                for i in range(0, len(punktid_ajad), 2)
                if punktid_ajad[i] in self.sauna_punktid
            }
            boonused = {
                punktid_ajad[i]: punktid_ajad[i + 1]
                for i in range(0, len(punktid_ajad), 2)
                if punktid_ajad[i] not in self.sauna_punktid
            }
            sauna_punktid_time_difference, points_not_done = self.calculate_specific_sauna_punktid_time_difference(
                punktid_ajad_dict
            )

            total_fine_minutes = len(points_not_done) * 30
            total_fine_hours, remainder_minutes = divmod(total_fine_minutes, 60)
            total_fine_str = f"{total_fine_hours:02}:{remainder_minutes:02}:00"

            kogu_aeg_str = data[6]
            kogu_aeg_obj = datetime.strptime(kogu_aeg_str, "%H:%M:%S")

            kogu_aeg_plus_fine_obj = kogu_aeg_obj + timedelta(minutes=total_fine_minutes)
            kogu_aeg_plus_fine_str = kogu_aeg_plus_fine_obj.strftime("%H:%M:%S")
            data_dict = {
                "Rinnanumber": data[0],
                "SI-Pulga nr": data[1],
                "Eesnimi": data[2],
                "Perenimi": data[3],
                "Tiimi nimi": data[4],
                "Klass": data[5],
                "Stardiaeg": data[9],
                "Lõpuaeg": data[-1],
                "Kogu aeg": data[6],
                "Kogu aeg pluss trahv": kogu_aeg_plus_fine_str,
                "Võetud punktid": data[8],
                "Võetud sauna punktid": str(len(punktid_ajad_dict.keys())),
                "Sauna punktid": [punktid_ajad_dict],
                "Sauna ajad": sauna_punktid_time_difference,
                "Tegemata punktid": points_not_done,
                "Kogu trahv": total_fine_str,
                "Võetud boonuse punktid": str(len(boonused.keys())),
                "Boonused": [boonused],
            }
            self.data_list.append(data_dict)
            self.combobox_items.append(f"{index+1}.{data[4]}")
            self.combobox["values"] = self.combobox_items
            time_difference_output = []
            sauna_fine_total = 0
            for key, value in sauna_punktid_time_difference.items():
                time_difference_output.append(f"\n\t\t{key}: {value}")

                time_difference = datetime.strptime(value, "%H:%M:%S") - datetime.strptime("00:00:00", "%H:%M:%S")

                if time_difference < timedelta(minutes=3):
                    sauna_fine_total += 30
            total_fine_minutes += sauna_fine_total
            total_fine_hours, remainder_minutes = divmod(total_fine_minutes, 60)
            total_fine_str = f"{total_fine_hours:02}:{remainder_minutes:02}:00"
            sauna_fine_hours, remainder_minutes = divmod(sauna_fine_total, 60)
            sauna_fine_str = f"{sauna_fine_hours:02}:{remainder_minutes:02}:00"
            points_not_done = [f"\n\t\t{points}" for points in points_not_done]
            data_to_insert = (
                f"{index+1}.{data[4]}({data[2]} {data[3]} - {data[1]})"
                f"\n\n\tVõetud sauna punktid: {str(len(punktid_ajad_dict.keys()))}"
                f"\n\tVõetud boonuse punktid: {str(len(boonused.keys()))}"
                f"\n\tKõik punktid: {data[8]}"
                f"\n\tAlguse aeg: {data[9]}"
                f"\n\tLõppaeg: {data[-1]}"
                f"\n\tKogu aeg: {data[6]}"
                f"\n\tSauna ajad: \n{''.join(time_difference_output)}\n"
                f"\n\tSauna aja trahv(<3min): {sauna_fine_str}"
                f"\n\tKäimata saunad: \n{''.join(points_not_done if points_not_done else "\n\t\t-")}\n"
                f"\n\tKäimata sauna trahvid: {total_fine_str}"
                f"\n\tKogu trahv: {total_fine_str}\n\n"
            )

            self.text_box.insert(tk.END, data_to_insert)
    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    sauna_marathon = SaunaMarathon()
    sauna_marathon.run()
