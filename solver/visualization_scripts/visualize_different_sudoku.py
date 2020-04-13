import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def main():
    sudoku_full = pd.read_csv("logs/sudoku_runtime.csv")
    sudoku_negation = pd.read_csv("logs/log_sudoku_sketchedvariables_only_negation_time_vs_#examples")
    sudoku_eq       = pd.read_csv("logs/log_sudoku_sketchedvariables_4_time_vs_#examples")
    sns.set(font_scale=3)
    sns.set_style("whitegrid")
    plt.plot(sudoku_full['number_of_examples'],sudoku_full['time'],linestyle='-', marker='v', markersize=20)
    plt.plot(sudoku_negation['number_of_examples'] ,sudoku_negation['time'], linestyle='-', marker='s', markersize=20)
    plt.plot(sudoku_eq['number_of_examples'], sudoku_eq['time'],linestyle='-', marker='o', markersize=20)
    plt.xlim(plt.xlim()[0]-3, plt.xlim()[1]+15)
    plt.ylim(-15, plt.ylim()[1]+10)
    plt.legend(labels=["Full Sketch: 4 ?= and 1 ?not", "Only 1 ?not", "Only 4 ?=" ],loc='best')
    plt.xlabel("Number of Examples")
    plt.ylabel("Runtime in Seconds")
    plt.show()

if __name__ == "__main__":
    main()
