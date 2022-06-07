import openpyxl
import matplotlib
import matplotlib.pyplot as plot
import numpy as np
import copy
import os

matplotlib.rc('font', family='arial')
matplotlib.rcParams['hatch.linewidth'] = 2

read_book = openpyxl.load_workbook("Benchmark/Benchmark.xlsx")
EMULATOR_NAMES = ["DAOW", "Bluestacks", "GAE", "VMware", "Native PC", "Trinity", "WSA", "QEMU-KVM"]
TOTAL_WIDTH = 1.4
SPACE = 2.0
COLORS = [(229 / 256, 161 / 256, 36 / 256), (0 / 256, 158 / 256, 115 / 256), (128 / 256, 69 / 256, 156 / 256)]
HATCHES = ['\\\\\\', '...', '///']

def get_data_from_sheet_by_rows(sheet, rows, data, offset, num_data):
    for idx, emulator_name in enumerate(EMULATOR_NAMES):
        data[emulator_name] = list()
        cur_rows = copy.deepcopy(rows)
        for i in range(num_data):
            data[emulator_name].append([])
            for row in cur_rows:
                data[emulator_name][i].append(float(sheet.cell(row, idx + 2).value or 0))
            cur_rows = [row + offset for row in cur_rows]


def read_data(benchmark_type):
    data = dict()
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

    return row_names, data


def draw_bar_graph(benchmark_type, fig_format="pdf"):
    emulator_order = [4, 5, 0, 1, 2, 3, 6, 7]
    row_names, data = read_data(benchmark_type)
    num_bars = len(data[EMULATOR_NAMES[0]][0])
    width = TOTAL_WIDTH / num_bars
    offset = (SPACE - TOTAL_WIDTH) / 2

    fig = plot.figure(figsize=(11.6, 6.5))

    plot.rcParams['xtick.direction'] = 'in'
    plot.rcParams['ytick.direction'] = 'in'
    plot.rcParams['pdf.fonttype'] = 42
    plot.rcParams['ps.fonttype'] = 42
    font_size = 24

    plot.minorticks_off()
    max_y = 0
    for i in range(num_bars):
        x = [x_ * SPACE + width * (i + 0.5) + offset for x_ in range(len(EMULATOR_NAMES))]
        y = [np.average([datum[i] for datum in data[EMULATOR_NAMES[id]]]) for id in emulator_order]
        std = [np.std([datum[i] for datum in data[EMULATOR_NAMES[id]]]) for id in emulator_order]
        if max_y < max(y):
            max_y = max(y)
        plot.bar(x, y, width, yerr=std, label=row_names[i], color='none', edgecolor=COLORS[i], lw=2, hatch=HATCHES[i], error_kw=dict(ecolor='black', lw=1.5, capthick=1.5, capsize=3.5))

    ax = plot.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)

    plot.xlim(0, SPACE * (len(EMULATOR_NAMES)))
    plot.xticks([i * SPACE + SPACE / 2 for i in range(len(EMULATOR_NAMES))],
                [EMULATOR_NAMES[id] for id in emulator_order], fontsize=20)
    plot.tick_params(labelsize=20, width=2)
    if benchmark_type == 'Internal':
        plot.yticks([0, 10, 20, 30, 40, 50, 60, 70], fontsize=20)
    else:
        pass

    plot.ylabel("Frames Per Second", fontsize=28)
    legend = plot.legend(fontsize=font_size, loc='upper right', edgecolor=(0.5, 0.5, 0.5), borderpad=0, borderaxespad=1)
    legend.get_frame().set_linewidth(1)
    legend.get_frame().set_boxstyle('Square')

    fig.tight_layout()

    file_name = "Benchmark_" + benchmark_type + "." + fig_format
    file_name = os.path.join(os.curdir, "Benchmark/fig", file_name)
    plot.savefig(file_name)
    plot.show()


if __name__ == "__main__":
    draw_bar_graph("Internal", "pdf")
    draw_bar_graph("External", "pdf")
