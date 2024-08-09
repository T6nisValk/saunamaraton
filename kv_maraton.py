from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import customtkinter as ctk


class kvMarathon:
    def __init__(self):
        self.kv_punktid = [
            "11",
            "12",
            "21",
            "22",
            "31",
            "32",
            "41",
            "42",
            "51",
            "52",
            "61",
            "62",
            "71",
            "72",
            "81",
            "82",
            "91",
            "92",
            "101",
            "102",
            "111",
            "112",
            "121",
            "122",
            "131",
            "142",
        ]

        self.combobox_items = []

        self.root = ctk.CTk()
        self.root.geometry("800x700")
        self.root.title("kvmaraton")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.create_widgets()

    def create_widgets(self):
        self.create_browse_frame()
        self.create_data_frame()

    def create_browse_frame(self):
        self.browse_entry_text = tk.StringVar()
        self.browse_frame = ctk.CTkFrame(self.root)
        self.browse_frame.pack(pady=5)

        self.browse_label = ctk.CTkLabel(self.browse_frame, text="Faili asukoht: ")
        self.browse_label.grid(row=0, column=0, padx=5)

        self.browse_entry = ctk.CTkEntry(self.browse_frame, textvariable=self.browse_entry_text)
        self.browse_entry.grid(row=0, column=1, pady=5)

        self.browse_button = ctk.CTkButton(
            self.browse_frame, text="Browse", width=1, command=lambda: self.browse_file()
        )
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.confirm_button = ctk.CTkButton(
            self.browse_frame, text="Run", width=1, command=lambda: self.process_data(self.browse_entry.get())
        )
        self.confirm_button.grid(row=0, column=3)

        self.table_button = ctk.CTkButton(self.browse_frame, text="Table", width=1, command=lambda: self.table())
        self.table_button.grid(row=0, column=4, padx=5)

        self.individual_label = ctk.CTkLabel(self.browse_frame, text="Meeskonna algandmed: ")
        self.individual_label.grid(row=0, column=5)

        self.combobox = ctk.CTkComboBox(self.browse_frame, values=self.combobox_items)
        self.combobox.set("Vali meeskond")
        self.combobox.grid(row=0, column=6, pady=5)

        self.combobox_button = ctk.CTkButton(
            self.browse_frame, text="Run", width=1, command=lambda: self.individual_team()
        )
        self.combobox_button.grid(row=0, column=7, padx=5)

    def create_data_frame(self):
        self.data_frame = ctk.CTkFrame(self.root)
        self.data_frame.pack(pady=5)

        self.main_label = ctk.CTkLabel(self.data_frame, text="TULEMUSED (Failipõhiselt järjekorras)")
        self.main_label.pack(pady=5)

        self.text_box = ctk.CTkTextbox(self.data_frame, height=800, width=400)
        self.text_box.pack(side=tk.LEFT)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        self.browse_entry_text.set(file_path)

    def calculate_time_difference(self, start_time, end_time):
        format_str = "%H:%M:%S"
        start_datetime = datetime.strptime(start_time, format_str)
        end_datetime = datetime.strptime(end_time, format_str)
        time_difference = end_datetime - start_datetime
        return time_difference

    def calculate_specific_kv_punktid_time_difference(self, kv_punktid_dict):
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
            ("131", "142"),
        ]

        time_difference_dict = {}
        points_not_done = []
        for start_point, end_point in pairs_to_calculate:
            start_times = [time for point, time in kv_punktid_dict.items() if point == start_point]
            end_times = [time for point, time in kv_punktid_dict.items() if point == end_point]
            if start_times and end_times:
                start_time = start_times[0]
                end_time = end_times[-1]
                if start_time > end_time:
                    points_not_done.append(f"\n\t\t{start_point}-{end_point}")
                    continue
                else:
                    time_difference = self.calculate_time_difference(start_time, end_time)
                    time_difference_dict[f"{start_point}-{end_point}"] = str(time_difference)
            else:
                points_not_done.append(f"\n\t\t{start_point}-{end_point}")
        return time_difference_dict, points_not_done

    def str_to_timedelta(self, time_str):
        h, m, s = map(int, time_str.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def sum_time_strings(self, *time_strs):
        total_timedelta = timedelta()
        for time_str in time_strs:
            total_timedelta += self.str_to_timedelta(time_str)
        return total_timedelta

    def div_times(self, one, two):
        total_timedelta = self.str_to_timedelta(one) - self.str_to_timedelta(two)
        total_timedelta = self.timedelta_to_str(total_timedelta)
        return total_timedelta

    def timedelta_to_str(self, td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def process_data(self, file_path):
        self.data_list = []
        try:
            with open(file_path, encoding="utf-8") as f:
                self.lines = f.readlines()
            self.text_box.delete(1.0, tk.END)
            for index, line in enumerate(self.lines):
                data = [item for item in line.strip("\n").split(";") if item not in ["", "?"]]

                punktid_ajad = data[10:-1]

                punktid_ajad_dict = {}
                for i in range(0, len(punktid_ajad), 2):
                    point = punktid_ajad[i]
                    time = punktid_ajad[i + 1]
                    if point.endswith("1"):
                        if point not in punktid_ajad_dict:
                            punktid_ajad_dict[point] = time
                    else:
                        punktid_ajad_dict[point] = time
                self.boonused = {
                    punktid_ajad[i]: punktid_ajad[i + 1]
                    for i in range(0, len(punktid_ajad), 2)
                    if punktid_ajad[i] not in self.kv_punktid
                }
                kv_punktid_time_difference, points_not_done = self.calculate_specific_kv_punktid_time_difference(
                    punktid_ajad_dict
                )

                time_difference_output = []
                kv_time_fine_total_minutes = 0
                kv_times = []
                for key, value in kv_punktid_time_difference.items():
                    kv_times.append(value)
                    time_difference_output.append(f"\n\t\t{key}: {value}")
                    value = datetime.strptime(value, "%H:%M:%S")
                    time_to_compare = datetime.strptime("00:03:00", "%H:%M:%S")
                    if value < time_to_compare:
                        kv_time_fine_total_minutes += 15
                total_timedelta = self.sum_time_strings(*kv_times)
                total_time_str = self.timedelta_to_str(total_timedelta)
                kulunud_aeg_miinus_kv_ajad = self.div_times(data[6], total_time_str)
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
                    "Võetud punktid": data[8],
                    "Võetud kv punktid": str(len(punktid_ajad_dict.keys())),
                    "kv punktid": [punktid_ajad_dict],
                    "kv ajad": kv_punktid_time_difference,
                    "Tegemata punktid": points_not_done,
                    "kv ajad kokku": total_time_str,
                    "Kulunud aeg miinus kv ajad": kulunud_aeg_miinus_kv_ajad,
                    "Tegemata punktide kogus": len(points_not_done),
                }
                
                self.data_list.append(data_dict)
                self.combobox_items.append(f"{index+1}.{data[4]}")
                self.combobox.configure(values=self.combobox_items)

                data_to_insert = (
                    f"{index+1}.{data[4]}({data[2]} {data[3]} - {data[1]})"
                    f"\n\n\tVõetud kv punktid: {str(len(punktid_ajad_dict.keys()))}"
                    f"\n\tKõik punktid: {data[8]}"
                    f"\n\tAlguse aeg: {data[9]}"
                    f"\n\tLõppaeg: {data[-1]}"
                    f"\n\tKogu aeg: {data[6]}"
                    f"\n\tkv ajad: {total_time_str}"
                    f"\n\tKulunud aeg miinus kv ajad: {kulunud_aeg_miinus_kv_ajad}"
                    f"\n\tkv ajad: \n{''.join(time_difference_output)}\n"
                    f"\n\tKäimata kvde kogus: {len(points_not_done)}"
                    f"\n\tKäimata kvd: \n{''.join(points_not_done if points_not_done else "\n\t\t-")}\n\n\n"
                )

                self.text_box.insert(tk.END, data_to_insert)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found.")

    def individual_team(self):
        try:
            index = self.combobox.get().split(".")[0]
            data = self.data_list[int(index) - 1]
            team_data = tk.Tk()
            team_data.geometry("700x550")
            team_data.title(f"{data["Tiimi nimi"]}")
            data_frame = tk.Frame(team_data)
            data_frame.pack(padx=5, pady=5)
            text_box = tk.Text(team_data, height=35, width=80)
            text_box.pack(side=tk.LEFT, padx=5)
            scrollbar = tk.Scrollbar(team_data, command=text_box.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_box.config(yscrollcommand=scrollbar.set)
            tehtud_punktid = [f"\n\t{key}: {value}" for key, value in data["kv punktid"][0].items()]
            tegemata_punktid = [punkt for punkt in data["Tegemata punktid"]]
            data_to_insert = f"Rinnanumber: {data['Rinnanumber']} \
                    \nSI-Pulga nr: {data['SI-Pulga nr']} \
                    \nEesnimi: {data['Eesnimi']} \
                    \nPerenimi: {data['Perenimi']} \
                    \nTiimi nimi: {data['Tiimi nimi']} \
                    \nKlass: {data['Klass']} \
                    \nStardiaeg: {data['Stardiaeg']} \
                    \nLõpuaeg: {data['Lõpuaeg']} \
                    \nKogu aeg: {data['Kogu aeg']}\
                    \nkv ajad: {data["kv ajad kokku"]}\
                    \nKulunud aeg miinus kv ajad: {data["Kulunud aeg miinus kv ajad"]}\
                    \nVõetud punktid: {data['Võetud punktid']} \
                    \nTehtud punktid: \n{''.join(tehtud_punktid)}\n \
                    \nTegemata punktide kogus: {data["Tegemata punktide kogus"]}\
                    \nTegemata punktid: \n{''.join(tegemata_punktid)}\n"

            text_box.insert(tk.END, data_to_insert)
            team_data.mainloop()
        except ValueError:
            messagebox.showinfo(title="Info", message="No data.")

    def table(self):
        def copy_from_table(table, event=None):
            data = table.selection()
            values = ""
            for item in data:
                value = table.item(item, "values")
                values += "\t".join(map(str, value)) + "\n"
            self.root.clipboard_clear()
            self.root.clipboard_append(values)
            self.root.update()

        table_root = tk.Tk()
        table_root.title("Data table")
        table_root.geometry("1275x500")
        table = ttk.Treeview(
            table_root,
            height=100,
            columns=(
                "ID",
                "Tiim",
                "Nimi",
                "Alguse aeg",
                "Lõpu aeg",
                "Kulunud aeg",
                "Kogu kv aeg",
                "Lõppaeg",
                "Tegemata kvd",
            ),
            show="headings",
        )

        table.heading("ID", text="Koht")
        table.heading("Tiim", text="Tiim")
        table.heading("Nimi", text="Nimi")
        table.heading("Alguse aeg", text="Alguse aeg")
        table.heading("Lõpu aeg", text="Lõpu aeg")
        table.heading("Kulunud aeg", text="Kulunud aeg")
        table.heading("Kogu kv aeg", text="Kogu kv aeg")
        table.heading("Lõppaeg", text="Lõppaeg")
        table.heading("Tegemata kvd", text="Tegemata kvd")
        table.column("ID", width=50)
        table.column("Alguse aeg", width=100, anchor="center")
        table.column("Lõpu aeg", width=100, anchor="center")
        table.column("Kulunud aeg", width=100, anchor="center")
        table.column("Kogu kv aeg", width=100, anchor="center")
        table.column("Lõppaeg", width=100, anchor="center")
        table.column("Tegemata kvd", width=100, anchor="center")
        table.pack(pady=5, padx=5, side=tk.LEFT, fill="both", expand="yes")
        scrollbar = tk.Scrollbar(table_root, command=table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        table.config(yscrollcommand=scrollbar.set)
        table.bind("<Control-Key-c>", lambda x: copy_from_table(table, x))
        if self.data_list:
            sorted_data_list = sorted(self.data_list, key=lambda x: x["Kulunud aeg miinus kv ajad"])
            for index, line in enumerate(sorted_data_list):
                table.insert(
                    "",
                    "end",
                    values=(
                        f"{index+1}.",
                        line["Tiimi nimi"],
                        f"{line["Eesnimi"]} {line["Perenimi"]}",
                        line["Stardiaeg"],
                        line["Lõpuaeg"],
                        line["Kogu aeg"],
                        line["kv ajad kokku"],
                        line["Kulunud aeg miinus kv ajad"],
                        line["Tegemata punktide kogus"],
                    ),
                )

        else:
            table_root.destroy()
            messagebox.showinfo(title="Info", message="No data.")
        table_root.mainloop()

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":
    kv_marathon = kvMarathon()
    kv_marathon.run()
