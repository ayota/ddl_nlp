import io
import optparse
from os import path, makedirs

import numpy as np
from sklearn.cross_validation import KFold

from utils import PARENT_DIR, read_source


def generate_word2vec_folds(corpus=[], folds=3, seed=10, min_sentence_length=10):
    '''
    Generates a series of text files that each represent a training or test split of the text data.  Since word2vec does
    not conduct any calculations that rely on interactions across sentence boundaries this cross-validation k-fold generator
    splits the text by sentence and then chooses random sentences together into the same corpus.
    :param corpus: sequence of sentences representing entire corpus to work on
    :type corpus: sequence
    :param folds: how many train/test folds to make
    :type folds: int
    :param seed: random seed for the random number used to make the folds
    :type seed: int
    :param min_sentence_length: minimum sentence length that is considered valid
    :type min_sentence_length: int
    :return:
    '''

    tokenized_corpus=np.array(corpus)
    import pdb;pdb.set_trace()

    number_of_sentences=len(tokenized_corpus)

    kf = KFold(n=number_of_sentences, n_folds=folds, shuffle=True, random_state=seed)

    corpus_split = []
    for train_index, test_index in kf:
        corpus_split.append({'train':tokenized_corpus[train_index], 'test':tokenized_corpus[test_index]})

    return corpus_split

def collapse_corpus_sentence_list(folds_dict):
    '''
    Collapses the lists of sentences back down into a single string
    :param folds_dict: the dictionary that includes lists of sentences for every training, and test instance.
    :return:
    '''
    train_text = [' '.join(list(row['train'])) for row in folds_dict]
    test_text = [' '.join(list(row['test'])) for row in folds_dict]

    for row_index in range(len(folds_dict)):
        folds_dict[row_index] = {'train':train_text[row_index], 'test':test_text[row_index]}

    return folds_dict

def append_ontology_text(folds_dict, ontology_text):
    '''
    Appends the ontology text to the end of each training instance.
    :param folds_dict: a fold dict containing keys 'train' and 'test' which have values of strings
    :type folds_dict: dict{'train': str, 'test': str}
    :param ontology_text: Raw string of constructed ontology sentences.
    :type ontology_text: str
    :return: folds_dict with ontology content appended to the training instance
    :rtype: dict{'train': str, 'test': str}
    '''

    if ontology_text is not None:
        for row_index in range(len(folds_dict)):
            folds_dict[row_index]['train'] = folds_dict[row_index]['train'] + ' ' + ontology_text

    return folds_dict

def store_file(folds_dict, run_directory):
    '''
    Derive the location to save the resulting json file that includes all of the fold definitions.  Each fold generates a
      seperate directory depending on the number of folds chosen.  Within each fold directory is a train and test directory.
      Files are stored in all proper locations after parsing a dict with all of the data in it..
    :param folds_dict: folds_dict with ontology content appended to the training instance
    :type folds_dict: train and test split like dict{'train': str, 'test': str}
    :param run_directory: directory to store the data named after the run e.g. 'run1' or 'jazz'
    :return:
    '''
    def gen_fold_file(fold, fold_number, fold_dir, portion='train'):
        '''
        Given designation as either training or test and the fold number. Write the file to the correct location with
        correct name
        :param fold: the string text for the specific fold in question.
        :param fold_number: the index number for the fold
        :param portion: either training, test, or holdout if you are feeling that way.
        :return: None
        '''
        portion_dir = path.join(fold_dir, portion)
        if not path.exists(portion_dir):
            makedirs(portion_dir)
        fold_file = path.join(portion_dir, portion + '.txt')

        with open(fold_file,'wb') as outfile:
            outfile.write(fold[portion])

    current_dir = path.dirname(path.realpath(__file__))
    # assumes script being run from withing one of the sub-folders under fun_3000
    parent_dir = path.abspath(path.join(current_dir, '../..'))

    data_dir = path.join(parent_dir, 'data')

    specific_data_dir = path.join(data_dir, run_directory)

    if not path.exists(specific_data_dir):
        makedirs(specific_data_dir)

    # Generate a folder for each fold and under each fold folder build a  folder for train and test, then add a train
    # and test file in each folder.
    fold_number = 1
    for fold in folds_dict:
        fold_dir = path.join(specific_data_dir, str(fold_number))
        if not path.exists(fold_dir):
            makedirs(fold_dir)

        gen_fold_file(fold = fold, fold_number=str(fold_number), fold_dir=fold_dir, portion='train')

        gen_fold_file(fold = fold, fold_number=str(fold_number), fold_dir=fold_dir, portion='test')

        fold_number += 1


def run(run_directory, corpus_filename="output.txt", ontology_flag=False, k=5, seed=10, sentence_length=10):
    """
    Pulls the corpus and ontology if provided and builds k folds for test and train into the data directory.
    :param run_directory:
    :param corpus_filename: filename inside the run directory that is where the cleaned corpus file is stored.
    :param ontology_flag: If True then we are including an ontology.
    :param k: Number of folds
    :param seed: Any seed number for the split generator for the folds.
    :return:
    """
    # figure out where the corpus file is. should be in ddl_nlp/data/{run_directory}/{corpus_filename}
    absolute_corpus_filename = path.join(PARENT_DIR, 'data', run_directory, corpus_filename)
    with io.open(absolute_corpus_filename, "rt") as f:
        corpus = []
        for line in f.readlines():
            corpus.append(line)
    
    if ontology_flag == 'True':
        ontology = read_source(run_directory, source_type='ontology')
    else:
        ontology = ''

    corpus_split=generate_word2vec_folds(corpus=corpus, folds=k, seed=seed, min_sentence_length=sentence_length)
    collapsed_lists=collapse_corpus_sentence_list(folds_dict=corpus_split)
    final_splits=append_ontology_text(folds_dict=collapsed_lists, ontology_text=ontology)
    store_file(folds_dict=final_splits, run_directory=run_directory)

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-d', '--run_directory', dest='run_directory', default='', help='Specify run directory name e.g. run1 for files in data/run1')
    parser.add_option('-f', '--filename', dest='corpus_filename', default="output.txt", help="Specify the name of the cleaned corpus file generated from the data directory.")
    parser.add_option('-k', '--folds', dest='k', default=3, help='Specify number of folds requested', type='int')
    parser.add_option('-o', '--ontology_flag', action='store_true', dest='ontology_flag', default=False, help='if specified, an ontology is provided')
    parser.add_option('-s', '--seed', dest='seed', default=100, help='Specify the seed for the random number generator', type='int')
    parser.add_option('-l', '--sentence_length', dest='sentence_length', default=10, help="Specify the minimum length of a valid sentence. Shorter sentences will be thrown out of the corpus.")
    (opts, args) = parser.parse_args()

    run(opts.run_directory, opts.corpus_filename, opts.ontology_flag, opts.k, opts.seed, opts.sentence_length)
