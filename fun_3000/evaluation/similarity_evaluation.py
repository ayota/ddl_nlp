import gensim
import csv
import pandas as pd
import sklearn
import numpy as np


class TRAINING_BUILDER():
    '''
    This class
    '''
    def __init__(self):
        self.medical_coder_similarities = pd.read_csv('data/evaluation/UMLS_synonyms/UMNSRS_similarity.csv')

    def get_words_list(self):
        """
        Generates a list of all of the words found in the UMLS medical coder similarity CSV.
        :return:
        """
        return set(self.medical_coder_similarities['Term1']) | set(self.medical_coder_similarities['Term2'])

    def get_model_features(self, subject, fold):
        '''
        Retrieves a gensim model for a specific subject (training run) and fold.
        :param subject: The name of the word2vec training run.
        :param fold: The number as an int of the fold
        :return:
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
        import pdb; pdb.set_trace()
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

    def generate_folds(self, data):

        kf = sklearn.cross_validation.KFold(n=data.shape[0], n_folds=3, shuffle=True)

        # The features.  The first 2 columns are the names of the terms so those are removed.  The last column is the Response
        X = np.array(np.array(data.iloc[:,2:-1]))
        # The response.  The last column is the Response.
        y = np.array(np.array(data['Mean']))

        for train_index, test_index in kf:
            print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

    def run_model(self, training):
        sklearn.ensemble.RandomForestRegressor(training)


# word_list = ['include', 'rock,', 'Billy']
#
# y = TRAINING_BUILDER()
# word_list = y.get_words_list()
# model = y.get_model_features(subject='jazz', fold = 1)
# features = y.gen_features(model, word_list)
# response_frame = y.generate_response_frame(y.medical_coder_similarities)
# training_frame = y.generate_df_with_response(features, response_frame)
#
# model.most_similar('jazz')

