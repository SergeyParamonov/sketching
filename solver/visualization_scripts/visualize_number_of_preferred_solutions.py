import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    linewidth= 8
    number_of_solutions  = pd.read_csv("current_test/number_of_solutions.txt")
    good = number_of_solutions[number_of_solutions['overall_examples'] == 1]
    bad  = number_of_solutions[number_of_solutions['overall_examples'] == 0]


    good_without     = list(good.groupby('number_of_examples').mean()['before_dominance_check'])
    bad_without     = list(bad.groupby('number_of_examples').mean()['before_dominance_check'])
    overall_with   = list(bad.groupby('number_of_examples').mean()['number_of_solutions'])

    number_of_examples = list(range(1,8)) #1..7
    sns.set(font_scale=3.0)
    sns.set_style("whitegrid")
    plt.plot(number_of_examples,good_without, linestyle='-', marker='d', markersize=30, linewidth=linewidth)
    plt.plot(number_of_examples,bad_without, linestyle='-', marker='s', markersize=30, linewidth=linewidth)
    plt.plot(number_of_examples,overall_with, linestyle='-', marker='o', markersize=30, linewidth=linewidth)
#   plt.plot(number_of_examples, number_of_solutions['number_of_solutions'] , linestyle='-', marker='o', markersize=20)
#   sns.factorplot(x='number_of_examples', y = 'number_of_solutions',hue="sketch",data=number_of_solutions,legend_out=False,scale=2.0)
    plt.xlim(plt.xlim()[0]-0.1, plt.xlim()[1]+0.2)
    plt.xlabel("Number of Examples")
    plt.ylabel("Number of Solutions")
    plt.yscale('log')
    plt.ylim(plt.ylim()[0]*0.85, plt.ylim()[1]*1.25)
    plt.legend(labels=["Easy Group: without preferences","Hard Group: without preferences", "Overall under preferences"],loc='best')
    plt.show()

if __name__ == "__main__":
    main()
