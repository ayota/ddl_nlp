import gensim
import csv
import pandas as pd
import sklearn


class UMLS(object):

    def __init__(self):
        self.medical_coder_similarities = pd.read_csv('data/evaluation/UMLS_synonyms/UMNSRS_similarity.csv')

    def get_words_list(self):
        """
        Generates a list of all of the words found in the UMLS medical coder similarity CSV.
        :return:
        """
        return set(self.medical_coder_similarities['TERM1']) | set(self.medical_coder_similarities['TERM2'])


class SIMILARITY_PREDICTOR(object):

    def ingest_gensim_vectors(self):
        '''
        This function ingests model vectors resulting from word2vec for each word that exists in the medical_coder terms
        and generates a dataframe where each row is a term and each column is a different index location of the model vector.
        :return:
        '''
        pass

    def generate_folds(self):
        data = self.ingest_gensim_vectors()

def get_model_features(subject, fold):
    '''
    Retrieves a gensim model for a specific subject (training run) and fold.
    :param subject: The name of the word2vec training run.
    :param fold: The number as an int of the fold
    :return:
    '''
    return gensim.models.Word2Vec.load('models/' + subject + '/' + str(fold) + '/' + subject + '.model')

def gen_features(word_list):
    '''
    This function generates a Pandas Dataframe where each row represents the comparison between two words found in
    the UMLS. The feature set includes a response which is taken from self.medical_coder_similarities['Mean'] where
    a higher mean means the words are more similar.  We restrict ourselves to features that can only be generated from
    out word2vec implementation.
    :return:
    '''

    for word in word_list:
        model[word]

model = get_model_features(subject='jazz', fold = 1)

model.most_similar('jazz')

