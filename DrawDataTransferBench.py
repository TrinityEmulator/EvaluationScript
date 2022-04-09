import numpy as np
import matplotlib.pyplot as plt
import os

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
    plt.figure(figsize=(9, 7))
    ax = plt.gca()
    plt.xlabel("Data Chunk Size", fontsize=35)
    plt.ylabel("Throughput (GB/s)", fontsize=35)

    plt.yticks(fontsize=font_size)
    markers = ["s", "d"]
    for thread_id in num_threads:
        plt.ylim(0, 22)
        chunk_size = sorted(data[thread_id])
        x = np.array([str(int(i / 1024 / 1024)) + " MB" if int(i / 1024)
                                                           >= 1024 else str(int(i / 1024)) + " KB" for i in chunk_size])
        teleporting_x = sorted(our_data[thread_id])
        teleporting_y = np.array([our_data[thread_id][data_size][1]
                                  for data_size in teleporting_x])
        plt.plot(x, teleporting_y, marker=markers[thread_id % 2], color=COLOR_LIST[thread_id],
                 label="Data Teleporting " + str(
                     thread_id + 1) + (" threads" if thread_id > 0 else " thread"), zorder=1, linewidth=2.5,
                 markersize=10)

        if compare_target == "Exhaustion":
            y = np.array([data[thread_id][data_size][1] for data_size in chunk_size])
            if thread_id <= 1:
                plt.ylim(4, 20)
            else:
                plt.ylim(8.5, 20)
            plt.plot(x, y, marker=markers[thread_id % 2], color=COLOR_LIST[thread_id], linestyle='--',
                     label="Strategy Exhaustion " + str(
                         thread_id + 1) + (" threads" if thread_id > 0 else " thread"), zorder=1, linewidth=2.5,
                     markersize=10)
        if compare_target == "goldfish":
            google_x = sorted(google_data[thread_id])
            google_y = np.array([google_data[thread_id][data_size][1]
                                 for data_size in google_x])
            plt.plot(x, google_y, marker=markers[thread_id % 2], linestyle='--', color=COLOR_LIST[thread_id],
                     label="goldfish-pipe " + str(thread_id + 1) + (" threads" if thread_id > 0 else " thread"),
                     zorder=1, linewidth=2.5, markersize=10)
        plt.xticks(x, fontsize=font_size, rotation=45)

    plt.tight_layout()
    plt.legend(loc='upper left', fontsize=22)
    plt.savefig(f"fig/{fig_name}.{save_type}", dpi=OUTPUT_DPI, bbox_inches='tight')
    plt.show()


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
