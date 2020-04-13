import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    filename_template = "logs/precision_n_queens_all_models.csv"
    queens_precision_all_iterations = pd.read_csv(filename_template)
    queens_precision = queens_precision_all_iterations.groupby(["model","examples"]).mean()
    sns.set(font_scale=4.0)
    sns.set_style("whitegrid")
    markers=['o','d','^',"<",">"]
    queens_overall = queens_precision_all_iterations.groupby("examples").mean()
    queens_overall = queens_overall.add_suffix("_avg").reset_index()
    queens_overall['model'] = "average"
    print(queens_overall)
    queens_precision = queens_precision.add_suffix("_avg").reset_index()
    queens_data = queens_precision.append(queens_overall)
  # print(queens_precision)
    print(queens_data)
  
    sns.factorplot(x='examples', y="precision_avg",hue='model', data=queens_data, scale=2.5, markers=markers, markersize=50)
#   plt.xlim(plt.xlim()[0], plt.xlim()[1]+0.1)                                                                                             
    plt.xlabel("Number of Examples")                                                                                                           
    plt.ylabel("Precision")                                                                                                          
    plt.ylim(0, 1.05)                                                                                                              
  # plt.legend(labels=[], bbox_to_anchor=(-0.5, 1), loc='best',  ncol=1)
    plt.show()

if __name__ == "__main__":
    main()
