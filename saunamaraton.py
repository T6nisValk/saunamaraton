from datetime import datetime, timedelta
import json
import tkinter as tk
from tkinter import messagebox, ttk

sauna_punktid = [
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
    "132",
    "141",
    "142",
    "151",
    "152",
    "161",
    "162",
    "171",
    "172",
    "181",
    "182",
]
max_sauna_punktid = len(sauna_punktid)

data_list = []


def calculate_time_difference(start_time, end_time):
    format_str = "%H:%M:%S"
    start_datetime = datetime.strptime(start_time, format_str)
    end_datetime = datetime.strptime(end_time, format_str)
    time_difference = end_datetime - start_datetime
    return time_difference

def calculate_specific_sauna_punktid_time_difference(sauna_punktid_dict):
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
            start_time = start_times[0]  # First occurrence of start point
            end_time = end_times[-1]  # Last occurrence of end point
            time_difference = calculate_time_difference(start_time, end_time)
            time_difference_dict[f"{start_point}-{end_point}"] = str(time_difference)
        else:
            points_not_done.append(f"{start_point}-{end_point}")

    return time_difference_dict, points_not_done


def data_process():
    with open("sime_result.txt", encoding="utf-8") as f:
        lines = f.readlines()

    for index, line in enumerate(lines):
        data = [item for item in line.strip("\n").split(";") if item not in ["", "?"]]
        punktid_ajad = data[10:-1]
        punktid_ajad_dict = {
            punktid_ajad[i]: punktid_ajad[i + 1]
            for i in range(0, len(punktid_ajad), 2)
            if punktid_ajad[i] in sauna_punktid
        }
        boonused = {
            punktid_ajad[i]: punktid_ajad[i + 1]
            for i in range(0, len(punktid_ajad), 2)
            if punktid_ajad[i] not in sauna_punktid
        }
        sauna_punktid_time_difference, points_not_done = calculate_specific_sauna_punktid_time_difference(
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
            "L6puaeg": data[-1],
            "Kogu aeg": data[6],
            "Kogu aeg pluss trahv": kogu_aeg_plus_fine_str,
            "V6etud punktid": data[8],
            "V6etud sauna punktid": str(len(punktid_ajad_dict.keys())),
            "Sauna punktid": [punktid_ajad_dict],
            "Sauna ajad": sauna_punktid_time_difference,
            "Points not done": points_not_done,
            "Total fine": total_fine_str,
            "V6etud boonuse punktid": str(len(boonused.keys())),
            "Boonused": [boonused],
        }
        data_list.append(data_dict)

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

        text_box.insert(tk.END, data_to_insert)


def saun(index):
    sauna_info = data_list[index]["Sauna punktid"][0]
    output = [f"{(key, sauna_info.get(key))}\n" for key in data_list[index]["Sauna punktid"][0].keys()]
    sauna_info_str = "".join(map(str, output))
    messagebox.showinfo("Sauna punktid", sauna_info_str)


def boonus(index):
    boonuse_info = data_list[index]["Boonused"][0]
    output = [f"{(key, boonuse_info.get(key))}\n" for key in data_list[index]["Sauna punktid"][0].keys()]
    boonuse_info_str = "".join(map(str, output))
    messagebox.showinfo("Sauna punktid", boonuse_info_str)


root = tk.Tk()
root.geometry("1580x700")

main_label = tk.Label(root, text="TULEMUSED", font="Bold")
main_label.pack(pady=5)
data_frame = tk.Frame(root)
data_frame.pack()
text_box = tk.Text(data_frame, height=35, width=195)
text_box.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(data_frame, command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.config(yscrollcommand=scrollbar.set)

data_process()
json_data = json.dumps(data_list, indent=2)


root.mainloop()
