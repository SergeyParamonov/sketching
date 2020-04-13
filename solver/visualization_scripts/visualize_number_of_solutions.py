import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
#   number_of_solutions  = pd.read_csv("logs/number_of_solutions_experiment_standartized.txt")
    number_of_solutions  = pd.read_csv("logs/number_of_solutions_experiment_truncated.txt")
    average_number_of_solutions_per_example = list(number_of_solutions.groupby('number_of_examples').mean()['number_of_solutions'])
#   fap = list(reversed(list(number_of_solutions.loc[number_of_solutions['sketch'] == 'fap']['number_of_solutions'])))
#   iso  = list(reversed(list(number_of_solutions.loc[number_of_solutions['sketch'] == 'subgraph_isomorphism']['number_of_solutions'])))
#   number_of_examples = list(range(1,7)) #1..6
#   number_of_solutions_fap 
    sns.set(font_scale=2.5)
    sns.set_style("whitegrid")
  # plt.plot(number_of_examples,iso,number_of_examples,fap,number_of_examples, average_number_of_solutions_per_example, linestyle='-', marker='o', markersize=20)
#   plt.plot(number_of_examples, number_of_solutions['number_of_solutions'] , linestyle='-', marker='o', markersize=20)
    sns.factorplot(x='number_of_examples', y = 'number_of_solutions',hue="sketch",data=number_of_solutions,legend_out=False,scale=2.5, markers=['o','s','>','<','v','^','d','*','+','1'])
    plt.xlim(plt.xlim()[0]-0.1, plt.xlim()[1]+0.1)                                                                                             
    plt.ylim(0.87, plt.ylim()[1])                                                                                                              
    plt.xlabel("Number of Examples")                                                                                                           
    plt.ylabel("Number of Solutions")                                                                                                          
    plt.yscale('log')                                                                                                                          
    #plt.legend(labels=[],loc='best')
    plt.show()

if __name__ == "__main__":
    main()
