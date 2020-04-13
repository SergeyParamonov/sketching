import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def main():
    number_of_solutions  = pd.read_csv("number.txt")
    sns.set(font_scale=2.5)
    sns.set_style("whitegrid")
    sns.factorplot(x='number_of_examples', y = 'number_of_solutions',hue="sketch",data=number_of_solutions,legend_out=False,scale=2.5, markers=['o','s','>','<','v','^','d','*','+','1'])
    plt.xlim(plt.xlim()[0]-0.1, plt.xlim()[1]+0.1)                                                                                             
    plt.ylim(0.87, plt.ylim()[1])                                                                                                              
    plt.xlabel("Number of Examples")                                                                                                           
    plt.ylabel("Number of Solutions")                                                                                                          
    plt.yscale('log')                                                                                                                          
    #plt.legend(labels=[],loc='best')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
