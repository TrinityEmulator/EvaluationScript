import os
import matplotlib
import matplotlib.pyplot as plot
import pandas as pd
import numpy as np

matplotlib.rc('font', family='arial')
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Breakdown"))
LINE_STYLES = ["-",":","--","-."]
COLORS = ['b', 'k', (128/255, 0/255, 128/255), (0/255, 128/255, 128/255)]
LABELS = ['Trinity', 'w/o Flow Control', 'w/o Projection Space', 'w/o Teleporting']

def draw_cdf(data_table,limited_60 = False):
    plot.figure(figsize=(5.2, 4.3))
    plot.rcParams['figure.subplot.top'] = 0.99
    plot.rcParams['figure.subplot.bottom'] = 0.20
    plot.rcParams['figure.subplot.left'] = 0.05
    plot.rcParams['figure.subplot.right'] = 0.99
    plot.rcParams['xtick.direction'] = 'in'
    plot.rcParams['ytick.direction'] = 'in'
    plot.rcParams['pdf.fonttype'] = 42
    plot.rcParams['ps.fonttype'] = 42
    column_names = ['Trinity', 'w/o Flow Control', 'w/o Projection Space', 'w/o Teleporting']
    if not limited_60:
        column_names = [column_name+' Unlimited' for column_name in column_names]

    for id,columns in enumerate(column_names):
        avg_fps = np.sort(data_table[columns].to_list())
        game_id = np.arange(len(data_table[columns].to_list()))/float(len(data_table[columns].to_list()))
        plot.plot(game_id, avg_fps,label = LABELS[id], color = COLORS[id], linestyle=LINE_STYLES[id], linewidth=2)
    plot.tick_params(labelsize=16)
    plot.ylabel("Frames Per Second", fontsize=18)
    plot.xlabel("Apps by Increasing FPS", fontsize=18)

    plot.xlim([0, 0.99])
    plot.ylim([0, max(data_table['Trinity'])+3])
    plot.xticks([0, 0.09, 0.19, 0.29, 0.39, 0.49, 0.59, 0.69, 0.79, 0.89, 0.99],['1','10','20','30','40','50','60','70','80','90','100'])
    plot.yticks([0,10,20,30,40,50,60]) if limited_60 else plot.yticks([0,50,100,150,200])
    plot.legend(loc='upper center', edgecolor=(0.5, 0.5, 0.5),
                ncol=2, fontsize=14, bbox_to_anchor=(0.5, 1.25), handletextpad=0.2, handlelength=1, columnspacing=1)
    plot.tight_layout()
    fig_name = './breakdown-CDF_limited60.pdf' if limited_60 else './breakdown-CDF.pdf'
    plot.subplots_adjust(top=0.85)
    plot.savefig(os.path.join(os.curdir, "fig", fig_name))
    plot.show()

if __name__ == "__main__":
    data_table = pd.read_csv("BreakDownData.csv", encoding='utf8')
    draw_cdf(data_table)
    draw_cdf(data_table,True)