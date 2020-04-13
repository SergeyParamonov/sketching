import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def main():
    latin9  = pd.read_csv("logs/log_latin_square_k_9_time_vs_numberofexamples.csv")
    latin10 = pd.read_csv("logs/log_latin_square_k_10_time_vs_numberofexamples.csv")
    latin11 = pd.read_csv("logs/log_latin_square_k_11_time_vs_numberofexamples.csv")
    latin12 = pd.read_csv("logs/log_latin_square_k_12_time_vs_numberofexamples.csv")
    latin13 = pd.read_csv("logs/log_latin_square_k_13_time_vs_numberofexamples.csv")
    latin14 = pd.read_csv("logs/log_latin_square_k_14_time_vs_numberofexamples.csv")
    sns.set(font_scale=3)
    sns.set_style("whitegrid")
    plt.plot(latin9['number_of_examples'],  latin9['time'], linestyle='-', marker='o', markersize=20)
    plt.plot(latin10['number_of_examples'], latin10['time'],linestyle='-', marker='s', markersize=20)
    plt.plot(latin11['number_of_examples'], latin11['time'],linestyle='-', marker='<', markersize=20)
    plt.plot(latin12['number_of_examples'], latin12['time'],linestyle='-', marker='>', markersize=20)
    plt.plot(latin13['number_of_examples'], latin13['time'],linestyle='-', marker='v', markersize=20)
    plt.plot(latin14['number_of_examples'], latin14['time'],linestyle='-', marker='d', markersize=20)
    plt.xlim(plt.xlim()[0]-3, plt.xlim()[1]+15)
    plt.ylim(-15, plt.ylim()[1]+10)
    plt.legend(labels=["9x9", "10x10", "11x11", "12x12","13x13","14x14"],loc='best')
    plt.xlabel("Number of Examples")
    plt.ylabel("Runtime in Seconds")
    plt.show()

if __name__ == "__main__":
    main()
