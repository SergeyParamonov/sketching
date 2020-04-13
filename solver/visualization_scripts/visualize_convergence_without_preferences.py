import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
def main():
    data = pd.read_csv("logs/black_white_queens_number_of_solutions.txt")
    sns.set(font_scale=3.5)
    sns.set_style("whitegrid")
    fap = data[data['problem'] == "FAP"]
    queens = data[data['problem'] == "B&W Queens"]
    sudoku = data[data['problem'] == "Sudoku"]
    plt.plot(fap['number_of_examples'], fap['Without Preferences'], color = "red", linestyle='-', marker='o', markersize=30)
#   plt.plot(fap['number_of_examples'], fap['With Preferences'], color = "red", linestyle='-', marker='s', markersize=30)
    plt.plot(queens['number_of_examples'], queens['Without Preferences'], color = "blue", linestyle='-', marker='>', markersize=30)
#   plt.plot(queens['number_of_examples'], queens['With Preferences'], color = "blue", linestyle='-', marker='d', markersize=30)
#   plt.plot(sudoku['number_of_examples'], sudoku['With Preferences'], color = "green", linestyle='-', marker='^', markersize=30)
    plt.plot(sudoku['number_of_examples'], sudoku['Without Preferences'], color = "green", linestyle='-', marker='*', markersize=30)
    plt.xlim(plt.xlim()[0]-0.25, plt.xlim()[1]+0.3)
    plt.ylim(0.85, plt.ylim()[1]+3000)
    plt.legend(labels=["FAP (5) without preferences", "B&W Queens (5) without preferences", "Sudoku (5) without preferences"],loc='best')
    plt.xlabel("Number of Examples")
    plt.ylabel("Number of Solutions")
    plt.yscale('log')   
    plt.show()

if __name__ == "__main__":
    main()
