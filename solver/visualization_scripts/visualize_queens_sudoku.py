import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def main():
    sudoku = pd.read_csv("logs/sudoku_runtime.csv")
#   queens = pd.read_csv("logs/queens_runtime.csv")
    latin_square = pd.read_csv("logs/log_latin_square_k_9_time_vs_numberofexamples.csv")
    number_of_examples = len(sudoku['number_of_examples'])
    sns.set(font_scale=3)
    sns.set_style("whitegrid")
    plt.plot(sudoku['number_of_examples'],sudoku['time'],linestyle='-', marker='s', markersize=20)
    plt.plot(sudoku['number_of_examples'][:number_of_examples],latin_square['time'][:number_of_examples], linestyle='-', marker='o', markersize=20)
    plt.xlim(plt.xlim()[0]-3, plt.xlim()[1]+15)
    plt.ylim(-15, plt.ylim()[1]+10)
    sudoku_legend = mlines.Line2D([],[],color='blue', label='Sudoku', marker='s',markersize=20)
    queens_legend = mlines.Line2D([],[],color='green', label='Latin Square 9x9', marker='o',markersize=20)
    plt.legend(handles=[sudoku_legend,queens_legend],loc='best')
    plt.xlabel("Number of Examples")
    plt.ylabel("Runtime in Seconds")
    plt.show()

if __name__ == "__main__":
    main()
