from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


class SaunaMarathon:
    def __init__(self):
        self.sauna_punktid = [
            "11", "12", "21", "22", "31", "32", "41", "42", "51", "52", "61", "62", "71", "72",
            "81", "82", "91", "92", "101", "102", "111", "112", "121", "122", "131", "132",
            "141", "142", "151", "152", "161", "162", "171", "172", "181", "182",
        ]

        self.combobox_items = []

        self.root = tk.Tk()
        self.root.geometry("1275x600")
        self.root.title("Saunamaraton")

        self.create_widgets()
        # try:
        #     with open("fine.txt") as f:
        #         lines = f.readlines()
        #         for line in lines:
        #             if line.startswith("fine"):
        #                 fine = line.strip("\n").split("=")
        #                 self.fine_minute = int(fine[-1])
        #             elif line.startswith("bonus"):
        #                 bonus = line.strip("\n").split("=")
        #                 self.bonus_minute = int(bonus[-1])
        # except FileNotFoundError:
        #     enter_fine_minutes = tk.Tk()
        #     enter_fine_minutes.title("Sisesta trahv/boonus")
        #     fine_label = tk.Label(enter_fine_minutes, text="Trahv")
        #     fine_label.pack()
        #     self.fine_entry = tk.Entry(enter_fine_minutes)
        #     self.fine_entry.pack()
        #     bonus_label = tk.Label(enter_fine_minutes, text="Boonus")
        #     bonus_label.pack()
        #     self.bonus_entry = tk.Entry(enter_fine_minutes)
        #     self.bonus_entry.pack()
        #     ok_button = tk.Button(enter_fine_minutes, text="Ok", command=lambda: self.write())
        #     ok_button.pack()

        #     enter_fine_minutes.mainloop()

    def create_widgets(self):
        self.create_browse_frame()
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Testing")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)

    def about(self):
        messagebox.showinfo(title="About this", message="Random text goes here.")

    def create_browse_frame(self):
        self.browse_entry_text = tk.StringVar()
        self.browse_frame = tk.Frame(self.root)
        self.browse_frame.pack(pady=5)

        self.browse_label = tk.Label(self.browse_frame, text="Faili asukoht: ")
        self.browse_label.grid(row=0, column=0, padx=5)

        self.browse_entry = tk.Entry(self.browse_frame, width=40, textvariable=self.browse_entry_text)
        self.browse_entry.grid(row=0, column=1, pady=5)

        self.browse_button = tk.Button(self.browse_frame, text="Otsi",
                                       command=lambda: self.browse_file())
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.confirm_button = tk.Button(self.browse_frame, text="Näita",
                                        command=lambda: self.process_data(self.browse_entry.get()))
        self.confirm_button.grid(row=0, column=3)

        self.individual_label = tk.Label(self.browse_frame, text="Meeskonna algandmed: ")
        self.individual_label.grid(row=0, column=5)

        self.combobox = ttk.Combobox(self.browse_frame, values=self.combobox_items)
        self.combobox.set("Vali meeskond")
        self.combobox.grid(row=0, column=6, pady=5)

        self.combobox_button = tk.Button(
            self.browse_frame, text="Näita", command=lambda: self.individual_team())
        self.combobox_button.grid(row=0, column=7, padx=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"),
                       ("All files", "*.*")])
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
            ("181", "182"),]

        time_difference_dict = {}
        points_not_done = []
        for start_point, end_point in pairs_to_calculate:
            start_times = [time for point, time in sauna_punktid_dict.items() if point ==
                           start_point]
            end_times = [time for point, time in sauna_punktid_dict.items() if point == end_point]
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

    def process_data(self, file_path):
        self.data_list = []
        try:
            with open(file_path, encoding="utf-8") as f:
                self.lines = f.readlines()
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
                    if punktid_ajad[i] not in self.sauna_punktid}
                sauna_punktid_time_difference, points_not_done = self.calculate_specific_sauna_punktid_time_difference(
                    punktid_ajad_dict)
                käimata_saun_fine_minutes = len(points_not_done) * 15
                käimata_saun_fine_hours, remainder_minutes = divmod(käimata_saun_fine_minutes, 60)
                käimata_saun_fine_str = f"{käimata_saun_fine_hours:02}:{remainder_minutes:02}:00"
                boonuste_aeg_minutes = len(self.boonused) * 10
                boonuste_aeg_hours, remainder_minutes = divmod(boonuste_aeg_minutes, 60)
                boonuste_aeg_str = f"{boonuste_aeg_hours:02}:{remainder_minutes:02}:00"
                time_difference_output = []
                secret_sauna_times = []
                sauna_time_fine_total_minutes = 0
                for key, value in sauna_punktid_time_difference.items():
                    if key in ["111-112", "151-152"]:
                        secret_sauna_times.append(f"{key}:{value}")
                        continue
                    else:
                        time_difference_output.append(f"\n\t\t{key}: {value}")
                        value = datetime.strptime(value, "%H:%M:%S")
                        time_to_compare = datetime.strptime("00:03:00", "%H:%M:%S")
                        if value < time_to_compare:
                            sauna_time_fine_total_minutes += 15

                sauna_time_fine_total_hours, remainder_minutes = divmod(
                    sauna_time_fine_total_minutes, 60)
                sauna_time_fine_total_str = \
                    f"{sauna_time_fine_total_hours:02}:{remainder_minutes:02}:00"
                kogu_trahv_minutes = sauna_time_fine_total_minutes + käimata_saun_fine_minutes
                kogu_trahv_hours, remainder_minutes = divmod(kogu_trahv_minutes, 60)
                kogu_trahv_str = f"{kogu_trahv_hours:02}:{remainder_minutes:02}:00"
                kogu_aeg = datetime.strptime(data[6], "%H:%M:%S")
                kogu_trahv = datetime.strptime(kogu_trahv_str, "%H:%M:%S")
                kogu_aeg_pluss_trahv = kogu_aeg + timedelta(hours=kogu_trahv.hour,
                                                            minutes=kogu_trahv.minute,
                                                            seconds=kogu_trahv.second)
                boonuste_aeg = datetime.strptime(boonuste_aeg_str, "%H:%M:%S")
                lõpp_tulemus = kogu_aeg_pluss_trahv - timedelta(
                    hours=boonuste_aeg.hour, minutes=boonuste_aeg.minute,
                    seconds=boonuste_aeg.second)
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
                    "Käimata sauna trahv": käimata_saun_fine_str,
                    "Sauna aja trahv": sauna_time_fine_total_str,
                    "Kogu trahv": kogu_trahv_str,
                    "Salasaun": secret_sauna_times,
                    "Aeg trahviga": kogu_aeg_pluss_trahv.strftime("%H:%M:%S"),
                    "Boonuste aeg": boonuste_aeg_str,
                    "Lõppaeg": lõpp_tulemus.strftime("%H:%M:%S"),
                    "Võetud punktid": data[8],
                    "Võetud sauna punktid": str(len(punktid_ajad_dict.keys())),
                    "Sauna punktid": [punktid_ajad_dict],
                    "Sauna ajad": sauna_punktid_time_difference,
                    "Tegemata punktid": points_not_done,
                    "Võetud boonuse punktid": str(len(self.boonused.keys())),
                    "Boonused": [self.boonused],
                }
                self.data_list.append(data_dict)
                self.combobox_items.append(f"{index+1}.{data[4]}")
                self.combobox["values"] = self.combobox_items

            self.table()
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found.")

    def individual_team(self):
        try:
            index = self.combobox.get().split(".")[0]
            data = self.data_list[int(index)-1]
            team_data = tk.Tk()
            team_data.geometry("700x550")
            team_data.title(f"{data["Tiimi nimi"]}")
            data_frame = tk.Frame(team_data)
            data_frame.pack(padx=5, pady=5)
            self.ind_text_box = tk.Text(team_data, height=35, width=80)
            self.ind_text_box.pack(side=tk.LEFT, padx=5)
            scrollbar = tk.Scrollbar(team_data, command=self.ind_text_box.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.ind_text_box.config(yscrollcommand=scrollbar.set)
            tehtud_punktid = [f"\n\t{key}: {value}" for key,
                              value in data["Sauna punktid"][0].items()]
            tegemata_punktid = [punkt for punkt in data["Tegemata punktid"]]
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
                    \nTehtud punktid: \n{''.join(tehtud_punktid)}\n \
                    \nTegemata punktid: \n{''.join(tegemata_punktid)}\n \
                    \nBoonused: \n\n\t{"\n\t".join(data["Boonused"][0].keys())}\n\n\n"
            )
            self.ind_text_box.insert(tk.END, data_to_insert)
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

        table = ttk.Treeview(
            self.root, height=100,
            columns=("ID", "Tiim", "Nimi", "Alguse aeg", "Lõpu aeg", "Kulunud aeg", "Trahv", "111-112", "151-152",
                     "Boonus", "Lõppaeg"),
            show="headings")
        table_label = tk.Label(self.root, text="Järjestatud lõpuaja järgi.")
        table_label.pack()
        table.heading("ID", text="Koht")
        table.heading("Tiim", text="Tiim")
        table.heading("Nimi", text="Nimi")
        table.heading("Alguse aeg", text="Alguse aeg")
        table.heading("Lõpu aeg", text="Lõpu aeg")
        table.heading("Kulunud aeg", text="Kulunud aeg")
        table.heading("Trahv", text="Trahv")
        table.heading("111-112", text="111-112")
        table.heading("151-152", text="151-152")
        table.heading("Boonus", text="Boonus")
        table.heading("Lõppaeg", text="Lõppaeg")
        table.column("ID", width=50)
        table.column("Alguse aeg", width=100, anchor="center")
        table.column("Lõpu aeg", width=100, anchor="center")
        table.column("Kulunud aeg", width=100, anchor="center")
        table.column("Trahv", width=100, anchor="center")
        table.column("151-152", width=100, anchor="center")
        table.column("111-112", width=100, anchor="center")
        table.column("Boonus", width=100, anchor="center")
        table.column("Lõppaeg", width=100, anchor="center")
        table.pack(pady=5, padx=5, side=tk.LEFT, fill="both", expand="yes")
        scrollbar = tk.Scrollbar(self.root, command=table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        table.config(yscrollcommand=scrollbar.set)
        table.bind("<Control-Key-c>", lambda x: copy_from_table(table, x))
        if self.data_list:
            sorted_data_list = sorted(self.data_list, key=lambda x: x["Lõppaeg"])
            for index, line in enumerate(sorted_data_list):
                if line["Salasaun"]:
                    saun_111_112 = [saun for saun in line["Salasaun"] if saun.startswith("111")]
                    saun_151_152 = [saun for saun in line["Salasaun"] if saun.startswith("151")]
                table.insert("", "end", values=(f"{index+1}.",
                                                line["Tiimi nimi"],
                                                f"{line["Eesnimi"]} {line["Perenimi"]}",
                                                line["Stardiaeg"],
                                                line["Lõpuaeg"],
                                                line["Kogu aeg"],
                                                line["Kogu trahv"],
                                                saun_111_112[0].split(":", 1)[1] if saun_111_112 else "-",
                                                saun_151_152[0].split(":", 1)[1] if saun_151_152 else "-",
                                                line["Boonuste aeg"],
                                                line["Lõppaeg"]))

        else:
            messagebox.showinfo(title="Info", message="No data.")

    def write(self):
        with open("fine.txt", "w") as f:
            data = {"fine_minute": self.calculate_specific_sauna_punktid_time_differencefine_entry.get(),
                    "bonus_minute": self.bonus_entry.get()}
            for trahv, aeg in data.items():
                f.write(f"{trahv}={aeg}\n")

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":
    sauna_marathon = SaunaMarathon()
    sauna_marathon.run()
