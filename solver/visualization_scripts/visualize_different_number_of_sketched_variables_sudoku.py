import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def main():
    sudoku_4 = pd.read_csv("logs/log_sudoku_sketchedvariables_4_time_vs_#examples")
    sudoku_3 = pd.read_csv("logs/log_sudoku_sketchedvariables_3_time_vs_#examples")
    sudoku_2 = pd.read_csv("logs/log_sudoku_sketchedvariables_2_time_vs_#examples")
    sudoku_1 = pd.read_csv("logs/log_sudoku_sketchedvariables_1_time_vs_#examples")
    sns.set(font_scale=3)
    sns.set_style("whitegrid")
    plt.plot(sudoku_4['number_of_examples'],sudoku_4['time'], linestyle='-', marker='o', markersize=20)
    plt.plot(sudoku_3['number_of_examples'],sudoku_3['time'], linestyle='-', marker='s', markersize=20)
    plt.plot(sudoku_2['number_of_examples'],sudoku_2['time'], linestyle='-', marker='v', markersize=20)
    plt.plot(sudoku_1['number_of_examples'],sudoku_1['time'], linestyle='-', marker='D', markersize=20)
    plt.xlim(plt.xlim()[0]-1, plt.xlim()[1]+5)
    plt.ylim(-1, plt.ylim()[1]+1)
    plt.legend(labels=["Sudoku # of Sketched Eq ?= 4","Sudoku # of Sketched Eq ?= 3","Sudoku # of Sketched Eq ?= 2","Sudoku # of Sketched Eq ?= 1"],loc='best')
    plt.xlabel("Number of Examples")
    plt.ylabel("Runtime in Seconds")
    plt.show()

if __name__ == "__main__":
    main()
