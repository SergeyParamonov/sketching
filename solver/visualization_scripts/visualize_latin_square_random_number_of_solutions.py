import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    filename_template = "current_test/log_number_of_solutions_latin_square_preferences_vars_{k}.csv"
    number_of_solutions = {k:pd.read_csv(filename_template.format(k=k)) for k in range(2,5)}
    number_of_solutions = {k:number_of_solutions[k].groupby("number_of_examples").mean() for k in number_of_solutions.keys()}
    sns.set(font_scale=4.0)
    sns.set_style("whitegrid")
    markers1=['v','>','^',]
    markers2=['o','d','*',]
    colors = ['b','r','g',]
    for (k,v),m1,m2,c in zip(number_of_solutions.items(),markers1,markers2,colors):
        plt.plot(v['solutions'], linestyle='-', marker=m1, markersize=30,color=c)
        plt.plot(v['without_preferences'], linestyle='-', marker=m2, markersize=30,color=c)
    plt.xlim(plt.xlim()[0], plt.xlim()[1]+0.1)                                                                                             
    plt.xlabel("Number of Examples")                                                                                                           
    plt.ylabel("Number of Solutions")                                                                                                          
#   plt.ylim(0.9, 100)                                                                                                              
#   plt.yscale('log')                                                                                                                          
    plt.legend(labels=["2 with preferences","2 without preferences","3 with preferences","3 without preferences","4 with preferences","4 without preferences"], bbox_to_anchor=(-0.5, 1), loc='best',  ncol=1)
    plt.show()

if __name__ == "__main__":
    main()
