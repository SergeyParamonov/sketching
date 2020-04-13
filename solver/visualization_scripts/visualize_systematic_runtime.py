import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from pudb import set_trace as bp

mapping = {"ours":"Our Encoding", "hakank":"Hakank.org","potassco":"Potassco","tson":"Tran Cao Son Encoding", "avg":"Average"}


def main():
    filename_template = "logs/different_n_queens_time.csv"
    raw_data = pd.read_csv(filename_template)
    aggregated = raw_data.groupby(['task','#examples']).median()
    average    = raw_data.groupby(['#examples']).median()
    tasks=sorted(list(set(raw_data['task']) | set(['avg'])))

    

  # print(average)
    sns.set(font_scale=4.0)
    sns.set_style("whitegrid")
    markers=['o','d','s','v','^']
    colors = ['g','r','g',]
    labels=[]
    for m,task in zip(markers,tasks):
      labels.append(task)
      if task != 'avg':
        plt.plot(aggregated.ix[task]['time(s)'], linestyle='-', marker=m, markersize=30)
      else:
        plt.plot(average['time(s)'], linestyle='-', marker=m, markersize=30)
    plt.xlim(plt.xlim()[0], plt.xlim()[1]+2)                                                                                             
    plt.xlabel("Number of Examples")                                                                                                           
    plt.ylabel("Runtime in Seconds")                                                                                                          
    plt.legend(labels=list(map(lambda x: mapping[x], labels)),loc="best")
    plt.show()

if __name__ == "__main__":
    main()
