from pudb import set_trace as bp
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker



def main():
    filename_template = "logs/log_sudoku_grounding_time_vs_numberofexamples.csv"
    data = pd.read_csv(filename_template)
    sns.set(font_scale=3.0)
    sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
    sns.set_style("whitegrid")
    markers=['o','d','s']
    data.columns = ['number_of_examples', 'Gringo', 'Clasp']
    data['Total'] = data['Gringo'] + data['Clasp']
#   print(data)
    data = pd.melt(data, id_vars=['number_of_examples'], value_vars=['Gringo','Clasp', 'Total'])
    

    seaplot = sns.factorplot(x='number_of_examples', y="value",hue='variable', data=data, scale=2.0, markers=markers,legend=False)

    plt.xlabel("Number of Examples")                                                                                                           
    plt.ylabel("Time (in s)")                                                                                                          
    plt.ylim(0, 30)                                                                                                              
#   bp()
    

#   for ind, label in enumerate(plot.axes.flatten().get_xticklabels()):
#     if ind % 10 == 0:  # every 10th label is kept
#       label.set_visible(True)
#     else:
#       label.set_visible(False)
    ax = seaplot.ax.get_xaxis() 
    ax.set_major_locator(ticker.MultipleLocator(5))
#   bp()
    ax.set_ticklabels([5,10,50,100,150,200,250,300],[5,10,50,100,150,200,250,300])


    a= plt.legend(loc='best')
    a.set_title('System/Step')
    plt.show()

if __name__ == "__main__":
    main()
