import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    number_of_solutions  = pd.read_csv("logs/precision_queens.csv")
    sns.set(font_scale=2.5)
    sns.set_style("whitegrid")
    fig, ax = plt.subplots()

    sns.factorplot(x='number_of_examples', y = 'precision',hue="sketched",data=number_of_solutions,legend_out=False,scale=2.5, markers=['o','s','v','^','d'])
#   plt.xlim(plt.xlim()[0]-0.1, plt.xlim()[1]+0.1)                                                                                             
    plt.ylim(-0.05, 1.05)                                                                                                              
    plt.xlabel("Number of Examples")                                                                                                           
    plt.ylabel("Precision")                                                                                                          
    a= plt.legend(loc='best')
    a.set_title('# Sketched Vars')
#   plt.legend(labels=[],loc='best')
    plt.show()

if __name__ == "__main__":
    main()
