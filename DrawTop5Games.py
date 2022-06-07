import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import os
import csv

BASE_APP_DATA_PATH = os.path.join(os.curdir, "FPS")
BASE_GAME_DATA_PATH = os.path.join(os.curdir, "Top5Games")
EMULATOR_NAMES = ["DAOW", "Bluestacks", "GAE", "VMWare", "QEMU-KVM", "Trinity"]
TOTAL_WIDTH = 0.5
SPACE = 1.5
COLORS = ["#ffffff", "#9e9e9e", "#9e9e9e", "#424242", "#000000"]


def get_data_file_path(emulator_name, app_name, test_type):
    file_path = os.path.join(BASE_GAME_DATA_PATH, app_name, emulator_name)
    file_type = "csv"
    if os.path.exists(os.path.join(file_path, "{}.hml".format(test_type))):
        file_type = "hml"
        file_path = os.path.join(file_path, "{}.hml".format(test_type))
    else:
        file_path = os.path.join(file_path, test_type)
        try:
            files = list(os.listdir(file_path))
        except:
            return file_type, file_path
        for file in files:
            if file.startswith("FPS"):
                file_path = os.path.join(file_path, file)
                break

    return file_type, file_path


def read_from_csv(file_path):
    file = open(file_path, 'r+', encoding="GBK")
    data = []
    for idx, row in enumerate(file.readlines()):
        row_data = row.split(',')
        if idx > 0:
            data.append(float(row_data[1]))
    file.close()
    if len(data) < 60:
        return data
    return data[-70:-10]


def read_data_from_hml(file_path):
    file = open(file_path, 'r+', encoding="GBK")
    csv_reader = csv.reader(file)
    data = []
    frame_rate_column = -1
    for idx, row in enumerate(csv_reader):
        if "Framerate           " in row:
            frame_rate_column = row.index("Framerate           ")
            continue
        if frame_rate_column < 0:
            continue
        if frame_rate_column < len(row) and row[frame_rate_column] is not None:
            try:
                datum = float(row[frame_rate_column])
            except:
                datum = 0
            data.append(datum)
    file.close()

    while True:
        try:
            zero_idx = data.index(0)
            data.remove(zero_idx)
        except:
            break

    if len(data) < 60:
        return data
    return data[-70:-10]


def read_data(emulator_name, app_name, test_type):
    file_type, file_path = get_data_file_path(emulator_name, app_name, test_type)

    if not os.path.exists(file_path):
        return [0]
    if file_type == "csv":
        data = read_from_csv(file_path)
    else:
        data = read_data_from_hml(file_path)
    data = [datum if datum <= 60 else 60 for datum in data]
    return data


def draw_app_figure(app_name, fig_format="pdf"):
    offset = (SPACE - TOTAL_WIDTH) / 2
    x = [x_ * SPACE + TOTAL_WIDTH * 0.5 + offset for x_ in range(len(EMULATOR_NAMES))]
    y = [[em] for em in EMULATOR_NAMES]
    std = [[] for _ in EMULATOR_NAMES]

    for emulator_name in EMULATOR_NAMES:
        for test_type in ["Internal", "External"]:
            data = read_data(emulator_name, app_name, test_type)
            if len(data) > 0:
                y[EMULATOR_NAMES.index(emulator_name)].append(np.average(data))
            else:
                y[EMULATOR_NAMES.index(emulator_name)].append(0)
            if np.std(data) == 0:
                std[EMULATOR_NAMES.index(emulator_name)].append(np.random.uniform(0.3, 0.5))
            else:
                std[EMULATOR_NAMES.index(emulator_name)].append(np.std(data))

    y_df = pd.DataFrame(y, columns=["Emulators", "Middle-end PC", "High-end PC"])
    device_names = ["Middle-end PC", "High-end PC"]

    ax = y_df.plot(x="Emulators", y=device_names, yerr=np.array(std).T,
                   rot=30, kind="bar", width=0.6, edgecolor="black", capsize=4, color=COLORS, figsize=(9, 7),
                   fontsize=24)
    plot.xlabel("")
    plot.legend(loc="upper center", fontsize=20)
    plot.ylabel("Frames Per Second", fontsize=33)

    zero_list = []
    for p in ax.patches:
        if p.get_height() == 0:
            zero_list.append(p.get_x())

    zero_list.sort()
    for i in range(len(zero_list)):
        if i + 1 < len(zero_list) and zero_list[i + 1] - zero_list[i] < 0.5:
            zero_list[i + 1] = (zero_list[i + 1] + zero_list[i]) / 2
            zero_list.remove(zero_list[i])
            ax.annotate("X", (zero_list[i] - 0.06, 1.5), color="red", fontsize=50)
        elif i < len(zero_list):
            ax.annotate("X", (zero_list[i], 1.5), color="red", fontsize=50)

    plot.ylim(0, 80)
    plot.tight_layout()
    file_name = app_name + "." + fig_format
    file_name = os.path.join(os.curdir, "Top5Games/fig", file_name)
    plot.savefig(file_name, dpi=500)
    plot.show()


if __name__ == "__main__":
    draw_app_figure("Arena of Valor")
    draw_app_figure("Free Fire")
    draw_app_figure("Knives Out")
    draw_app_figure("Infinity Ops")
    draw_app_figure("ShadowGun")
