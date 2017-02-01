import pandas as pd
import numpy as np
import seaborn as sns

def main(fname):
    # comments here
    df = pd.read_csv(fname)
    eval_factorplot(df)
    # eval_boxplot(df)
    eval_swarmplot(df)



def eval_factorplot(df):
    xname = "Boost_level"
    yname = "Score"
    sns.factorplot(data=df, x=xname, y=yname)
    sns.plt.show()


def eval_boxplot(df):
    xname = "Boost_level"
    yname = "Score"
    sns.boxplot(x=xname, y=yname, data=df)
    sns.plt.show()

def eval_swarmplot(df):
    xname = "Boost_level"
    yname = "Score"
    sns.boxplot(x=xname, y=yname, data=df)
    sns.swarmplot(x=xname, y=yname, data=df, color=".25")
    sns.plt.show()






if __name__ == '__main__':
    fname = '../../scores.csv'
    main(fname)
