import matplotlib
import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import os

matplotlib.rc('font', family='arial')
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),"100Games"))

EMULATOR_NAME = ["DAOW", "Bluestacks", "GAE", "WSA", "VMware", "QEMU-KVM", "Best", "Trinity"]
COLORS = [(220 / 255, 128 / 255, 0 / 255), 'g', '#e040fb', 'r',"#00acc1", "#5d4037", 'k', 'b']
LINE_STYLES = [":", "--", "-.", (0, (5, 1)), (0, (3, 1, 1, 1)), (0, (3, 1, 1, 1, 1, 1)), (0, (1, 1)), '-']

def draw100games_cdf(test_type):
    plot.rcParams['pdf.fonttype'] = 42
    plot.rcParams['ps.fonttype'] = 42
    plot.rcParams['xtick.direction'] = 'in'
    plot.rcParams['ytick.direction'] = 'in'
    figure_sz_large = (5.6, 4)
    plot.figure(figsize=figure_sz_large)

    data_table = pd.read_csv(f"AllGameAvgFPS_{test_type}.csv", encoding='utf8')
    for emu_id, emu_name in enumerate(EMULATOR_NAME):
        avg_fps = np.sort(data_table[emu_name].to_list())
        avg_fps = avg_fps[~np.isnan(avg_fps)]
        game_id = np.arange(len(avg_fps))/float(len(avg_fps))
        plot.plot(game_id, avg_fps, label=emu_name, color = COLORS[emu_id],linestyle = LINE_STYLES[emu_id])

    ax = plot.gca()
    plot.tick_params(labelsize=16)
    plot.ylabel("Frames Per Second", fontsize=16)
    plot.xlabel("Apps by Increasing FPS", fontsize=16)

    plot.xlim([0, 0.99])
    plot.ylim([0, 63])
    plot.xticks([0, 0.09, 0.19, 0.29, 0.39, 0.49, 0.59, 0.69, 0.79, 0.89, 0.99],['1','10','20','30','40','50','60','70','80','90','100'])
    ax.set_yticks([0,10,20,30,40,50,60])
    handles, labels = ax.get_legend_handles_labels()
    handles = [handles[6],handles[2],handles[7],handles[3],handles[0],handles[4],handles[1],handles[5]]
    labels = [labels[6],labels[2],labels[7],labels[3],labels[0],labels[4],labels[1],labels[5]]
    legend = plot.legend(handles, labels, loc='upper center', edgecolor=(0.5, 0.5, 0.5), borderpad=0, borderaxespad=0.5,
                         ncol=4, fontsize=13, bbox_to_anchor=(0.5, 1.25), handletextpad=0.1, handlelength=1.5,columnspacing=1)
    legend.get_frame().set_linewidth(1)
    legend.get_frame().set_boxstyle('Square')
    plot.tight_layout()
    plot.savefig(os.path.join("fig",f"Compare-{test_type}_CDF.pdf"))
    plot.show()

if __name__ == "__main__":
    draw100games_cdf('Internal')
    draw100games_cdf('External')
