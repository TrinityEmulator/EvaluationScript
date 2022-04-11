# Evaluation Data and Scripts
![status](https://github.com/TrinityEmulator/EvaluationScript/actions/workflows/python-app.yml/badge.svg)

Here contains the evaluation scripts for generating our major figures in Trinity's paper. 

### 1. Requirements
To run the scripts, you'll
need first to install the `Python 3` environment. Also, we have some additional dependencies. To install them,
type `pip3 install -r requirements.txt` at the root directory of the repo. 

### 1. Script Usages
To run a script named `xxx.py`, simpy type `python3 xxx.py` in your terminal. The scripts functions are detailed as
follows.

* `DrawBenchmarkFigure.py`

  This script draws `Figure 4` and `Figure 5`. drawn Figures are placed in `Game/fig`.

* `DrawAppFigure.py`
  
  This script draws `Figure 6`~`Figure 10`. drawn Figures are placed in `Benchmark/fig`.

* `DrawDataTransferBench.py`
 
  This script draws `Figure 11`~`Figure 14`. drawn Figures are placed in `DataTransferBench/fig`.

### 3. Data Format

#### Benchmark
The raw benchmark data live in `Benchmark/Benchmark.xlsx`. It contains four data sheets, titled `{3DMark, GFXBench}_{External, Internal}`. Here `{3DMark, GFXBench}` refers to the two benchmark apps we test, and `{External, Internal}` refers to the tests on high-end and middle-end PCs, respectively.
Specific data format is documented is the first row and colum of each data sheet.

#### 3D App
3D app test results are included in `Game`. Here you'll find five folders named after the games we test, each of which contain the data for different emulators. 

Within the emulators' folders, you can find the raw data of FPS recorded during evaluation. In particular, there are two types of FPS raw data files with `hml` and `csv` suffixes, respectively, as we use different FPS measurement tools for DAOW and Bluestacks as they lack system-level supports for FPS capturing. 

However, you'll find that `hml` files are essentially the same as a `csv` one. You can find FPS data under the colum `Framerate` for `hml` files. For `csv` files, the second colum is the FPS data.

#### Data Transfer
This part of data are those of `Figure 11`~`Figure 14` (see Section 4.4 of our paper for detailed explanations), and are located in `DataTransferBench`. Specific descriptions of different folders are listed here.
| Folder | Description |
| ---  | --- |
| `teleporting` | Benchmark data of data teleporting |
| `goldfish-pipe` | Benchmark data of goldfish-pipe |
| `async_polling` | Benchmark data of teleporting with a fixed async + host polling strategy |
| `async_polling_aggregation` | Benchmark data of teleporting with a fixed async + host polling + data aggregation strategy |
| `sync_polling` | Benchmark data of teleporting with a fixed sync + host polling strategy |
| `sync_polling_aggregation` | Benchmark data of teleporting with a fixed sync + host polling + data aggregation strategy |
| `sync_vm-exit` | Benchmark data of teleporting with a fixed sync + VM_EXIT strategy |
| `sync_vm-exit_aggregation` | Benchmark data of teleporting with a fixed sync + VM_EXIT + data aggregation strategy |

Within each of the folder, there are a number of subfolders, whose name follows the convention of `{data_chunk_size in byte}_{number of threads}_0`. Each of the subfolder contains a `throughput.txt` file that hosts the raw throughput data we have measured in evaluation.
