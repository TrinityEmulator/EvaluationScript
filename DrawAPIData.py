import matplotlib
import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import os

matplotlib.rc('font', family='arial')
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),"APIData"))

def draw_api_distribution_CDF():
    plot_table = pd.read_csv(f"API_Call_Type_Distribution.csv", encoding='utf8')
    type1 = np.sort(plot_table['Type 1'])
    type2 = np.sort(plot_table['Type 2'])
    type3 = np.sort(plot_table['Type 3'])
    y=np.arange(len(type1))/float(len(type1)-1)

    plot.rcParams['figure.subplot.top'] = 0.90
    plot.rcParams['figure.subplot.bottom'] = 0.16
    plot.rcParams['figure.subplot.left'] = 0.16
    plot.rcParams['figure.subplot.right'] = 0.95
    plot.rcParams['xtick.direction'] = 'in'
    plot.rcParams['ytick.direction'] = 'in'
    plot.rcParams['pdf.fonttype'] = 42
    plot.rcParams['ps.fonttype'] = 42

    plot.figure(figsize=(5.2, 4.2))
    ax = plot.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.tick_params(width=2)

    plot.xticks(fontsize=18)
    plot.yticks(ticks=[0.2, 0.4, 0.6, 0.8, 1], fontsize=20) 
    plot.xlim([0, 100])
    plot.ylim([0, 1])
    plot.xlabel("Percentage (%)", fontsize=20)
    plot.ylabel("CDF", fontsize=20)
    plot.plot(type1,y, color='k', linewidth=2.5, label='Type-1')
    plot.plot(type2,y, color='b', linestyle='--', linewidth=2.5, label='Type-2')
    plot.plot(type3,y, color=(128/255, 0/255, 128/255), linestyle='-.', linewidth=2.5, label='Type-3')

    # type 1 Box
    ax.text(65, 0.45,\
        f"Mean={np.average(type1):,.2f}\nMedian={np.median(type1):,.2f}\nMin={np.min(type1):,.2f}\nMax={np.max(type1):,.2f}",\
        bbox=dict(boxstyle='square', facecolor='none', edgecolor='k', linewidth=2),\
        fontsize=15)
    x_start = 67.4
    y_start = 0.728
    xy_scale = np.max(type1)
    xdelta = -6.5
    ydelta = -xdelta / xy_scale
    ax.annotate('', xy=(x_start + xdelta, y_start + ydelta), xytext=(x_start, y_start), arrowprops=dict(arrowstyle="->", lw=2, color='k'))

    # type 2 Box
    ax.text(54, 0.10,\
        f"Mean={np.average(type2):,.2f}\nMedian={np.median(type2):,.2f}\nMin={np.min(type2):,.2f}\nMax={np.max(type2):,.2f}",\
        bbox=dict(boxstyle='square', facecolor='none', edgecolor='b', linewidth=2),\
        fontsize=15, color='b')
    x_start = 57.4
    y_start = 0.38
    xy_scale = np.max(type1)
    xdelta = -13.2
    ydelta = -xdelta / xy_scale
    ax.annotate('', xy=(x_start + xdelta, y_start + ydelta), xytext=(x_start, y_start), arrowprops=dict(arrowstyle="->", lw=2, color='b'))

    # type 3 Box
    ax.text(14, 0.6,\
        f"Mean={np.average(type3):,.2f}\nMedian={np.median(type3):,.2f}\nMin={np.min(type3):,.2f}\nMax={np.max(type3):,.2f}",\
        bbox=dict(boxstyle='square', facecolor='none', edgecolor=(128/255, 0/255, 128/255), linewidth=2),\
        fontsize=15, color=(128/255, 0/255, 128/255))
    x_start = 19.3
    y_start = 0.88
    xy_scale = np.max(type1)
    xdelta = -6.75
    ydelta = -xdelta / xy_scale
    ax.annotate('', xy=(x_start + xdelta, y_start + ydelta), xytext=(x_start, y_start), arrowprops=dict(arrowstyle="->", lw=2, color=(128/255, 0/255, 128/255)))

    legend = plot.legend(loc='upper center', fontsize=15, edgecolor=(0.5, 0.5, 0.5), borderpad=0, borderaxespad=1, ncol=3, bbox_to_anchor=(0.5, 1.16),handletextpad=0.05)
    legend.get_frame().set_linewidth(1)
    legend.get_frame().set_boxstyle('Square')
    plot.savefig(os.path.join('fig','Context-Resource-CDF.pdf'))
    plot.show()

def draw_data_size_CDF():
    data = np.loadtxt('Graphics_Data_Size_Per_Sec.csv',delimiter = ",", encoding='utf8')
    sorted_data = np.sort(data)

    yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)

    plot.rcParams['figure.subplot.top'] = 0.95
    plot.rcParams['figure.subplot.bottom'] = 0.16
    plot.rcParams['figure.subplot.left'] = 0.16
    plot.rcParams['figure.subplot.right'] = 0.98
    plot.rcParams['pdf.fonttype'] = 42
    plot.rcParams['ps.fonttype'] = 42

    plot.figure(figsize=(5, 4))

    plot.rcParams['xtick.direction'] = 'in'
    plot.rcParams['ytick.direction'] = 'in'
    ax = plot.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.tick_params(width=2)

    plot.xticks(fontsize=18)
    plot.yticks(ticks=[0.2, 0.4, 0.6, 0.8, 1], fontsize=20) 
    plot.xlim([0, 190])
    plot.ylim([0, 1.05])
    plot.xlabel("Size (MB)", fontsize=20)
    plot.ylabel("CDF", fontsize=20)
    plot.plot(sorted_data,yvals, color='b', linewidth=2.5)

    ax.text(80, 0.3,\
        f"Mean={np.average(sorted_data):,.2f}\nMedian={np.median(sorted_data):,.2f}\nMin={np.min(sorted_data):,.2f}\nMax={np.max(sorted_data):,.2f}",\
        bbox=dict(boxstyle='square', facecolor='none', edgecolor='b', linewidth=2),\
        fontsize=20, color='b')
    plot.savefig(os.path.join('fig','All-Size-CDF.pdf'))
    plot.show()

def draw_gl_per_frame_CDF():
    data = np.loadtxt('API_calls_per_frame.csv',delimiter = ",", encoding='utf8')
    plot.rcParams['figure.subplot.top'] = 0.99
    plot.rcParams['figure.subplot.bottom'] = 0.20
    plot.rcParams['figure.subplot.left'] = 0.05
    plot.rcParams['figure.subplot.right'] = 0.99
    plot.rcParams['pdf.fonttype'] = 42
    plot.rcParams['ps.fonttype'] = 42
    plot.figure(figsize=(5, 4))
    x = np.sort(data)
    y = np.arange(len(x))/float(len(x))
    plot.plot(x,y,color = 'b', linewidth=2.5)
    plot.tick_params(labelsize=18, width=2)
    plot.ylabel("CDF", fontsize=20)
    plot.xlabel("Number of API Calls", fontsize=20)

    plot.ylim([0, 1.05])
    plot.xlim([0, 27000])
    plot.yticks([0.2,0.4,0.6,0.8,1.0],["0.2","0.4","0.6","0.8","1.0"])
    plot.xticks([0,5000,10000,15000,20000,25000],['0','5K',"10K","15K","20K","25K"])
    ax = plot.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.text(10000, 0.25,\
        f"Mean={np.average(x):,.0f}\nMedian={np.median(x):,.0f}\nMin={np.min(x):,.0f}\nMax={np.max(x):,.0f}",\
        bbox=dict(boxstyle='square', facecolor='none', edgecolor='b', linewidth=2),\
        fontsize=20, color='b')
    plot.tight_layout()
    plot.savefig(os.path.join( "fig", "NumAPI_CDF.pdf"))
    plot.show()

if __name__ == "__main__":
    draw_api_distribution_CDF()
    draw_data_size_CDF()
    draw_gl_per_frame_CDF()
