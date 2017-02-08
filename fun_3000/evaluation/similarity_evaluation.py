# import gensim
# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor as rfr
# import numpy as np
# from sklearn.cross_validation import cross_val_score
import random
from os import path
import optparse
import time
import csv

CURRENT_DIR = path.dirname(path.realpath(__file__))
PARENT_DIR = path.abspath(path.join(CURRENT_DIR, '../..'))


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-r', '--training_run', dest='train_run', default='', help='Specify training run to test.')
    # parser.add_option('-f', '--folds', dest='k', default=3, help='Specify number of folds in training run', type='int')
    parser.add_option('-o', '--output_file', dest='output', default='scores.csv',help='File to store model score for run.')
    parser.add_option('-m', '--multiplier', dest='multiplier', help="What multiplier for the ontology boost was used for these models we are evaluating.")
    (opts, args) = parser.parse_args()

    score_final = random.random()

    with open(path.join(PARENT_DIR, opts.output), 'a') as output_file:
        output_writer = csv.writer(output_file)
        # output_writer.writerow([opts.train_run, score_final, time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y"),opts.multiplier])
        output_writer.writerow(
            [opts.train_run, score_final, time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y"), random.randint(1,5)])









