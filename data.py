import tkinter as tk
from tkinter import filedialog


def browse():
    file_path = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    entry_var.set(file_path)


def run():
    path = entry_field.get()
    output = {}
    with open(path) as f:
        for index, line in enumerate(f.readlines()):
            stripped_line = line.strip("\n")
            output[f"{index+1}, {stripped_line.split(";")[2]} {stripped_line.split(";")[3]}"] = \
                [stripped_line[:stripped_line.index("?")-3],
                 stripped_line[stripped_line.index("?")-3:]]

    for key in output.keys():
        output[key] = [
            [item for item in output[key][0].strip("").split(
                ";") if item not in ["", "?"]],
            [item for item in output[key][1].strip("").split(
                ";") if item not in ["", "?"]]
        ]
        print(f"{key} : {output[key]}\n")


root = tk.Tk()
root.geometry("200x100")

entry_var = tk.StringVar()
entry_field = tk.Entry(root, textvariable=entry_var,
                       borderwidth=3, width=30)
entry_field.pack(pady=5)

browse_button = tk.Button(
    root, text="Browse", borderwidth=3, command=lambda: browse())
browse_button.pack()

run_button = tk.Button(root, text="Run", borderwidth=3,
                       command=lambda: run())
run_button.pack(pady=5)

root.mainloop()
