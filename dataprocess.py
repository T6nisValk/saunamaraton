import json

data_list = []
with open("sime_result.txt") as f:
    lines = f.readlines()

for line in lines:
    data = [item for item in line.strip("\n").split(";") if item not in ["", "?"]]
    data_dict = {
        "Rinnanumber": data[0],
        "SI-Pulga nr": data[1],
        "Eesnimi": data[2],
        "Perenimi": data[3],
        "Tiimi nimi": data[4],
        "Klass": data[5],
        "Raja aeg": data[6],
        "Mingi t2ht": data[7],
        "V6etud punktid": data[8],
        "Stardiaeg": data[9],
        "L6puaeg": data[-1],
        "Punktid ja ajad": data[10:-1],
    }
    data_list.append(data_dict)
json_data = json.dumps(data_list, indent=2)
with open("output.json", "w") as f:
    f.write(json_data)
print(json_data)
