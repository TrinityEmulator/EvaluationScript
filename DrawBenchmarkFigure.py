import openpyxl
import matplotlib.pyplot as plot
import numpy as np
import copy
import os

read_book = openpyxl.load_workbook("Benchmark/Benchmark.xlsx")
emulator_names = ["DAOW", "BlueStacks", "LDPLAYER", "Google", "VMWare", "Native PC", "Trinity", "WSA", "QEMU"]
TOTAL_WIDTH = 1.4
SPACE = 2.0
COLORS = ["#ffffff", "#e0e0e0", "#9e9e9e", "#424242", "#000000"]


def get_data_from_sheet_by_rows(sheet, rows, data, offset, num_data):
    for idx, emulator_name in enumerate(emulator_names):
        data[emulator_name] = list()
        cur_rows = copy.deepcopy(rows)
        for i in range(num_data):
            data[emulator_name].append([])
            for row in cur_rows:
                data[emulator_name][i].append(float(sheet.cell(row, idx + 2).value or 0))
            cur_rows = [row + offset for row in cur_rows]


def read_data(benchmark_name, benchmark_type):
    data = dict()
    if benchmark_name == "all":
        rows = [4, 5]
        row_names = ["Slingshot Unlimited Test 1 (3DMark)", "Slingshot Unlimited Test 2 (3DMark)",
                     "Manhattan Offscreen 1080p (GFXBench)"]
        data_3dmark = dict()
        sheet = read_book["3DMark_" + benchmark_type]
        get_data_from_sheet_by_rows(sheet, rows, data_3dmark, 9, 5)
        rows = [3]
        data_GFX = dict()
        sheet = read_book["GFXBench_" + benchmark_type]
        get_data_from_sheet_by_rows(sheet, rows, data_GFX, 5, 5)
        for key in data_3dmark:
            data[key] = [data_3dmark[key][i] + data_GFX[key][i] for i in range(0, 5)]
    elif benchmark_name == "3DMark":
        sheet = read_book[benchmark_name + "_" + benchmark_type]
        rows = [4, 5]
        row_names = ["Graphics Test 1", "Graphics Test 2"]
        get_data_from_sheet_by_rows(sheet, rows, data, 9, 5)
        print(data)
    elif benchmark_name == "GFXBench":
        sheet = read_book[benchmark_name + "_" + benchmark_type]
        rows = [3, 5]
        row_names = ["Manhattan", "TRex"]
        get_data_from_sheet_by_rows(sheet, rows, data, 5, 5)
        print(data)
    elif benchmark_name == "3D Graphic Benchmark":
        sheet = read_book[benchmark_name + "_" + benchmark_type]
        rows = [2, 4, 3]
        row_names = ["Max FPS", "Avg. FPS", "Min FPS"]
        get_data_from_sheet_by_rows(sheet, rows, data, 0, 1)
    elif benchmark_name == "GPU Benchmark 3D":
        sheet = read_book[benchmark_name + "_" + benchmark_type]
        rows = [2, 5, 6, 4]
        row_names = ["Total Score", "Max FPS", "Avg. FPS", "Min FPS"]
        get_data_from_sheet_by_rows(sheet, rows, data, 0, 1)
    elif benchmark_name == "Madagascar 3D Benchmark":
        sheet = read_book[benchmark_name + "_" + benchmark_type]
        rows = [2, 3, 4, 5]
        row_names = ["Total Score", "Water", "Animation", "Effects"]
        get_data_from_sheet_by_rows(sheet, rows, data, 0, 1)
    else:
        raise Exception("Invalid Sheet Name")

    return row_names, data


def draw_bar_graph(benchmark_name, benchmark_type, fig_format="pdf"):
    emulator_order = [5, 6, 0, 1, 2, 3, 4, 7, 8]
    row_names, data = read_data(benchmark_name, benchmark_type)
    num_bars = len(data[emulator_names[0]][0])
    width = TOTAL_WIDTH / num_bars
    offset = (SPACE - TOTAL_WIDTH) / 2

    fig = plot.figure(figsize=(12, 7))
    plot.minorticks_off()
    Trinity = np.array([np.mean([row[0] for row in data["Trinity"]]), np.mean([row[1] for row in data["Trinity"]]),
                        np.mean([row[2] for row in data["Trinity"]])])
    DAOW = np.array([np.mean([row[0] for row in data["DAOW"]]), np.mean([row[1] for row in data["DAOW"]]), 1])
    nativePC = np.array([np.mean([row[0] for row in data["Native PC"]]), np.mean([row[1] for row in data["Native PC"]]),
                         np.mean([row[2] for row in data["Native PC"]])])
    print("Trinity/DAOW: foreach benchmark: {}% On average: {}".format(Trinity[:2] / DAOW[:2],
                                                                       np.mean(Trinity[:2]) / np.mean(DAOW[:2])))
    print("Trinity/nativePC: foreach benchmark: {}% On average: {}".format(Trinity / nativePC,
                                                                           np.mean(Trinity) / np.mean(nativePC)))
    max_y = 0
    for i in range(num_bars):
        x = [x_ * SPACE + width * (i + 0.5) + offset for x_ in range(len(emulator_names) - 1)]
        y = [np.average([datum[i] for datum in data[emulator_names[id]]]) for id in emulator_order if id != 2]
        std = [np.std([datum[i] for datum in data[emulator_names[id]]]) for id in emulator_order if id != 2]
        if max_y < max(y):
            max_y = max(y)
        # print("{} Avg. FPS: {}, FPS STD {}".format(row_names[i], y, std))
        plot.bar(x, y, width, yerr=std, label=row_names[i], color=COLORS[i], edgecolor="black", capsize=4)

    emulator_names[8] = "QEMU-KVM"
    emulator_names[3] = "GAE"
    emulator_names[1] = "Bluestacks"
    plot.xlim(0, SPACE * (len(emulator_names) - 1))
    plot.xticks([i * SPACE + SPACE / 2 for i in range(len(emulator_names) - 1)],
                [emulator_names[id] for id in emulator_order if id != 2])
    plot.tick_params(labelsize=18)
    plot.ylim(0, max_y * 1.2)

    plot.ylabel("Frames Per Second", fontsize=35)
    # fixed legend pos
    legend = plot.legend(fontsize=23, loc='upper right')
    legend.get_frame().set_edgecolor("black")
    legend.get_frame().set_linewidth(1)

    fig.tight_layout()

    file_name = "Benchmark_" + benchmark_type + "." + fig_format
    file_name = os.path.join(os.curdir, "Benchmark/fig", file_name)
    plot.savefig(file_name, dpi=500)
    plot.show()


if __name__ == "__main__":
    draw_bar_graph("all", "Internal", "pdf")
    draw_bar_graph("all", "External", "pdf")
