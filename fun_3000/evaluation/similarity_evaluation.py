import gensim
import pandas as pd
from sklearn.ensemble import RandomForestRegressor as rfr
import numpy as np
from sklearn.cross_validation import cross_val_score
import optparse
import time
import csv

class FEATURE_BUILDER():
    '''
    This class is intended to be used to build a dataframe that will be used in post word2vec machine learning and
    evaluation. This combines the list of work similarity comparisons from UMLS with the vector outputs from gensim.
    Essentially the feature set becomes an N=5 length vector where if each row is a comparison between two words the vector
    is the subtraction between the vector representations for each word.
    '''
    def __init__(self):
        # Grabs the csv with the medical coder Mean similarity scores between various medical terms.
        self.medical_coder_similarities = pd.read_csv('data/evaluation/UMLS_synonyms/UMNSRS_similarity.csv')

    def get_words_list(self):
        """
        Generates a list of all of the words (with no repeats) found in the UMLS medical coder similarity CSV.
        the output from this function should also be used in ingestion to generate a list of terms we want to use
        to pull corpuses from various places..
        :return:
        """
        return set(self.medical_coder_similarities['Term1']) | set(self.medical_coder_similarities['Term2'])

    def get_model_features(self, subject, fold):
        '''
        Retrieves a gensim model for a specific training run and fold.
        :param subject: The name of the word2vec training run.
        :param fold: The number as an int of the fold
        :return: A model object that was generated fro this training run and fold.
        '''
        return gensim.models.Word2Vec.load('models/' + subject + '/' + str(fold) + '/' + subject + '.model')

    def gen_features(self, model, word_list):
        '''
        This function generates a Pandas Dataframe where each row represents the comparison between two words found in
        the UMLS. The feature set includes a response which is taken from self.medical_coder_similarities['Mean'] where
        a higher mean means the words are more similar.  We restrict ourselves to features that can only be generated from
        out word2vec implementation.
        :param word_list: A unique list of words that is included in the human assisted word comparison results. i.e. all the
        words that were compared by humans.
        :return: A dataframe with one column for each Term named Term1 and Term2 and N other columns one for each index location
        of a word vector. For example, if we tune word2vect to output a 5 index long array for each trained word the dataframe
        will include 5 columns, one for each array position.
        '''
        word_comparison = []
        word_list = list(word_list)
        for word in word_list:
            for comparison_word in word_list:
                word_comparison.append((word, comparison_word))

        terms_dataframe = pd.DataFrame(word_comparison, columns = ['Term1','Term2'])

        # We are going to compare every word against itself and every other word so if we have 5 words that have been compared
        # by medical coders we weill end up with 25 comparisons.  (the number of rows).  The number of

        # WARNING: 5 below is hardcoded. If we change the hyperparameter for the middle layer of the gensim model this will
        # error
        width = 5

        feature_array = np.zeros((len(word_list)*len(word_list), width)) # Initialize an empty numpy array of the size we want.

        # The features that are generated are the vector subtraction between two vector representations of the words.
        k = 0
        for word in word_list:
            for comparison_word in word_list:
                try:
                    feature_array[k] = model[word] - model[comparison_word]
                except:
                    feature_array[k] = np.empty((1, width))
                    feature_array[k] = np.NAN
                k += 1

        feature_dataframe = pd.DataFrame(feature_array)

        combined = pd.concat([terms_dataframe, feature_dataframe], axis=1)

        return combined

    def generate_response_frame(self, human_similarity_results):
        '''
        Generates a dataframe with all combinations of term similarities from an input dataframe (the source human measured
        comparisons between words).  Build both backward and forward comparisons. Meaning if we see a comparison between
        'cat' and 'dog' we also should generate a record for the comparison between 'dog' and 'cat'.
        :param human_similarity_results: A dataframe with at lease the following three columns ['Term1','Term2','Mean'] where
        Mean is the similarity score between the two terms.
        :return: a Dataframe with columns 'Term1', 'Term2', and 'Mean'
        '''
        human_similarity_results_backwards = human_similarity_results
        # Switch the names of term 1 and term 2 columns so we get the reverse order of the words as well for evaluation.
        human_similarity_results_backwards.rename(columns={'Term1': 'Term2', 'Term2': 'Term1'}, inplace=True)
        # Generate a dataframe with both the forward and backward relationships between words.
        forward_and_backwards = pd.concat([human_similarity_results, human_similarity_results_backwards], axis=0)

        return forward_and_backwards[['Term1', 'Term2', 'Mean']]

    def generate_df_with_response(self, features, response):
        '''
        Combines a dataframe that includes all of the features that are previously generated from the word2vec model and
        our reference data from the medical coders which gives us a float response 'mean' for a lot of the word pairs.
        :return:
        '''
        combined = pd.merge(left=features, right=response, how='inner', on=['Term1', 'Term2'])
        combined.drop_duplicates(inplace=True)

        # We cannot have any NAs in the dataframe for it to run in sklearn.
        combined.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

        return combined


class SIMILARITY_PREDICTOR(object):
    '''
    This class simply runs a dumb (no tuning) random forest regressor on the feature and response dataframe that is
    generated from the FEATURE BUILDER.
    '''
    def train_cv_and_score(self, data):
        '''
        The main sklearn function used in this is cross_val_score which basically does it all sets up folds, trains,
        runs a cross validated R^2 score.
        :param data: The dataset with all of the features, the response column, and another two columns (one for each term)
        :return: a single cross validated score (R^2) for a single fold from the gensim model result.
        '''

        # The features.  The first 2 columns are the names of the terms so those are removed.  The last column is the Response
        X = np.array(np.array(data.iloc[:, 2:-1]))
        # The response.  The last column is the Response.
        y = np.array(np.array(data['Mean']))

        estimator = rfr()

        score = cross_val_score(estimator, X, y).mean()

        return score

def build_feature_response_data(training_run, fold):
    '''
    Given a training run name or 'subject' and a specific fold within the run generate a dataframe that is ready for
    random forest regressor training and scoring.  This gets data from UMLS and uses the gensim model object to generate
    the dataframe.
    :param training_run: name of the folder as a string for the training run in question.
    :param fold: The fold within the training run you want to build the dataset for
    :return:
    '''
    y = FEATURE_BUILDER()
    word_list = y.get_words_list()
    model = y.get_model_features(subject=training_run, fold = fold)
    features = y.gen_features(model, word_list)
    response_frame = y.generate_response_frame(y.medical_coder_similarities)
    frame = y.generate_df_with_response(features, response_frame)

    return frame

def score(data):
    '''
    Runs training for a random forest regressor on a single dataset and returns a cross validated score which is an
    R^2 value.
    :param data:
    :return:
    '''
    sp = SIMILARITY_PREDICTOR()
    return sp.train_cv_and_score(data)

def build_train_and_score(training_run, fold):
    '''
    A wrapper function for building the dataset for a training_run and fold ready for post gensim evaluation.
    :param training_run:  name of the folder as a string for the training run in question.
    :param fold:  The fold within the training run you want to build the dataset for
    :return: An R^2 score for this specific fold for this specific training_run.
    '''
    data = build_feature_response_data(training_run=training_run, fold=fold)
    final_score = score(data)
    return final_score

def full_cross_validated_score(training_run, folds):
    '''
    Runs post gensim evaluation for all folds under a given training run (experiment).
    :param training_run:
    :param folds: Number of folds we decided on in the gensim run.
    :return: An average score across all folds. The score is an R^2 value.
    '''
    scores = []
    for fold in range(1,folds+1):
        scores.append(build_train_and_score(training_run, str(fold)))

    return sum(scores) / float(len(scores))

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-r', '--training_run', dest='train_run', default='', help='Specify training run to test.')
    parser.add_option('-f', '--folds', dest='k', default=3, help='Specify number of folds in training run', type='int')
    parser.add_option('-o', '--output_file', dest='output', default='scores.csv',help='File to store model score for run.')
    (opts, args) = parser.parse_args()

    score_final = full_cross_validated_score(opts.train_run, opts.k)

    with open(opts.output, 'a') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow([opts.train_run, score_final, time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y")])







