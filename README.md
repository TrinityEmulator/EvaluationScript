# Evaluation Data and Scripts
![status](https://github.com/TrinityEmulator/EvaluationScript/actions/workflows/python-app.yml/badge.svg)

Here contains the evaluation scripts for generating our major figures in Trinity's paper. 

### Requirements
To run the scripts, you'll
need first to install the `Python 3` environment. Also, we have some additional dependencies. To install them,
type `pip3 install -r requirements.txt` at the root directory of the repo. 

### Script Usages
To run a script named `xxx.py`, simpy type `python3 xxx.py` in your terminal. The scripts functions are detailed as
follows.

* `DrawBenchmarkFigure.py`

  This script draws `Figure 4` and `Figure 5`. Figures are placed in `Game/fig`.

* `DrawAppFigure.py`
  
  This script draws `Figure 6`~`Figure 10`. Figures are placed in `Benchmark/fig`.
