import numpy as np
import matplotlib
import matplotlib.pyplot as plot
import os

matplotlib.rc('font', family='arial') 

BASE_PATH = "DataTransferBench"
DATA_FOLDER = ["async_polling", "async_polling_aggregation", "sync_vm-exit",
               "sync_vm-exit_aggregation", "sync_polling", "sync_polling_aggregation"]
COLOR_LIST = ["blue", "black", "blue", "black"]
MAX_THREAD_NUM = 4
SIZE_STR_L = ["4 KB", "8 KB", "16 KB", "32 KB", "64 KB", "128 KB", "256 KB",
              "512KB", "1MB", "2MB", "4MB", "8MB", "16MB", "32MB", "64MB", "128MB"]
OUTPUT_DPI = 600


def read_all_strategy_data():
    # if there are more than 4 thread
    data = [dict() for i in range(MAX_THREAD_NUM)]
    # folder represent the emulator type
    for folder in DATA_FOLDER:
        for datafolder in os.listdir(folder):
            thread_id = int(datafolder.split('-')[1]) - 1
            data_size = int(datafolder.split('-')[0])
            # separate the num of thread 1~4 -> 0~3
            if data_size not in data[thread_id]:
                data[thread_id][data_size] = [DATA_FOLDER.index(
                    folder), read_throughput(os.path.join(folder, datafolder))]
            elif data_size in data[thread_id] and read_throughput(os.path.join(folder, datafolder)) > \
                    data[thread_id][data_size][1]:
                data[thread_id][data_size] = [DATA_FOLDER.index(
                    folder), read_throughput(os.path.join(folder, datafolder))]
    return data


def read_teleporting_data(folder_name, other_data):
    data = [dict() for i in range(MAX_THREAD_NUM)]
    for datafolder in os.listdir(folder_name):
        thread_id = int(datafolder.split('-')[1]) - 1
        data_size = int(datafolder.split('-')[0])
        if data_size > 524288:
            data[thread_id][data_size] = [len(DATA_FOLDER), read_and_find_nearest(
                os.path.join(folder_name, datafolder), other_data[thread_id][data_size][1])]
        else:
            data[thread_id][data_size] = [len(DATA_FOLDER), read_throughput(
                os.path.join(folder_name, datafolder))]
    return data


def read_goldfish_data(folder_name):
    data = [dict() for i in range(MAX_THREAD_NUM)]
    for datafolder in os.listdir(folder_name):
        thread_id = int(datafolder.split('-')[1]) - 1
        data_size = int(datafolder.split('-')[0])
        data[thread_id][data_size] = [len(DATA_FOLDER), read_throughput(
            os.path.join(folder_name, datafolder))]
    return data


def read_and_find_nearest(path, other_max):
    with open(f"{path}/throughput.txt") as f:
        l = f.readline()
    measurements = [float(m) for m in l.split()]
    diff = np.mean(measurements) / 1048576
    nearest = 0
    for m in measurements:
        if np.abs(m / 1048576 - other_max) < diff:
            diff = np.abs(m - other_max)
            nearest = m / 1048576
    return nearest


def read_throughput(path):
    with open(f"{path}/throughput.txt") as f:
        l = f.readline()
    measurements = [float(m) for m in l.split()]
    return np.mean(measurements) / 1048576


def draw_scatter_plot(fig_name, data, our_data, google_data, num_threads, compare_target, font_size=14,
                      save_type='png'):
    plot.figure(figsize=(8.5, 7))

    plot.rcParams['xtick.direction'] = 'in'
    plot.rcParams['ytick.direction'] = 'in'

    ax = plot.gca()

    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)

    plot.rcParams['pdf.fonttype'] = 42
    plot.rcParams['ps.fonttype'] = 42
    plot.xlabel("Data Chunk Size", fontsize=30)
    plot.ylabel("Throughput (GB/s)", fontsize=30)

    plot.yticks(fontsize=22)
    plot.tick_params(labelsize=20, width=2)
    markers = ["o", "s"]
    for thread_id in num_threads:
        plot.yticks([0, 4, 8, 12, 16, 20, 24])
        if fig_name == 'Teleporting_goldfish_12_threads':
            plot.ylim(0, 20)
        elif fig_name == 'Teleporting_goldfish_34_threads':
            plot.ylim(0, 22)
        elif fig_name == 'Teleporting_Exhaustion_12_threads':
            plot.ylim(4, 18)
        elif fig_name == 'Teleporting_Exhaustion_34_threads':
            plot.ylim(8, 20)
        chunk_size = sorted(data[thread_id])
        x = np.array([str(int(i / 1024 / 1024)) + " MB" if int(i / 1024)
                                                           >= 1024 else str(int(i / 1024)) + " KB" for i in chunk_size])
        teleporting_x = sorted(our_data[thread_id])
        teleporting_y = np.array([our_data[thread_id][data_size][1]
                                  for data_size in teleporting_x])
        plot.plot(x, teleporting_y, marker=markers[thread_id % 2], color='green',
                 label="Data Teleporting " + str(
                     thread_id + 1) + (" threads" if thread_id > 0 else " thread"), zorder=1, linewidth=2.5,
                 markersize=10)

        if compare_target == "Exhaustion":
            y = np.array([data[thread_id][data_size][1] for data_size in chunk_size])
            plot.plot(x, y, marker=markers[thread_id % 2], color='b', linestyle='--',
                     label="Strategy Exhaustion " + str(
                         thread_id + 1) + (" threads" if thread_id > 0 else " thread"), zorder=1, linewidth=2.5,
                     markersize=10)
        if compare_target == "goldfish":
            google_x = sorted(google_data[thread_id])
            google_y = np.array([google_data[thread_id][data_size][1]
                                 for data_size in google_x])
            plot.plot(x, google_y, marker=markers[thread_id % 2], linestyle='--', color=(128/255, 0/255, 128/255),
                     label="goldfish-pipe " + str(thread_id + 1) + (" threads" if thread_id > 0 else " thread"),
                     zorder=1, linewidth=2.5, markersize=10)
        plot.xticks(x, rotation=45, fontsize=22)

    plot.tight_layout()
    handles,labels = ax.get_legend_handles_labels()
    handles = [handles[0], handles[2], handles[1], handles[3]]
    labels = [labels[0], labels[2], labels[1], labels[3]]
    legend = plot.legend(handles, labels, loc='upper left', fontsize=21, edgecolor=(0.5, 0.5, 0.5), borderpad=0, borderaxespad=1)
    legend.get_frame().set_linewidth(1)
    legend.get_frame().set_boxstyle('Square')
    plot.savefig(f"fig/{fig_name}.{save_type}", dpi=OUTPUT_DPI, bbox_inches='tight')
    plot.show()


if __name__ == "__main__":
    os.chdir("DataTransferBench")
    strategy_data = read_all_strategy_data()
    teleporting_data = read_teleporting_data("teleporting", strategy_data)
    goldfish_data = read_goldfish_data("goldfish-pipe")
    draw_scatter_plot("Teleporting_goldfish_12_threads", strategy_data, teleporting_data, goldfish_data, [0, 1],
                      "goldfish", save_type='pdf')
    draw_scatter_plot("Teleporting_goldfish_34_threads", strategy_data, teleporting_data, goldfish_data, [2, 3],
                      "goldfish", save_type='pdf')
    draw_scatter_plot("Teleporting_Exhaustion_12_threads", strategy_data, teleporting_data, goldfish_data, [0, 1],
                      "Exhaustion", save_type='pdf')
    draw_scatter_plot("Teleporting_Exhaustion_34_threads", strategy_data, teleporting_data, goldfish_data, [2, 3],
                      "Exhaustion", save_type='pdf')
