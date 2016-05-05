#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.cross_validation import KFold
from os import path, makedirs, listdir
import re
import numpy as np
import optparse
import sys

def clean_corpus(corpus=None):
    '''
    cleans out all non-ascii characters, newlines, carriage returns, wikipedia headers, other fun stuff
    :param corpus: a string from a text file representing the corpus
    :return:
    '''

    corpus = re.sub(r'<.*?>', ' ', corpus)
    corpus = re.sub(r'{.*?}', ' ', corpus)
    corpus = re.sub(r'${.*?}', ' ', corpus)
    corpus = re.sub(r'={2,}.*?={2,}', ' ', corpus)
    corpus = re.sub(r'\n|\r', ' ', corpus)
    corpus = re.sub(r'\\x[a-zA-Z0-9]{2,}', ' ', corpus)
    corpus = re.sub(r'\s{2,}.*?\s{2,}', ' ', corpus)
    corpus = corpus.strip()
    return corpus

def tokenize_sentences(corpus=None):
    '''
    split the corpus into sentences.
    :param corpus: a string from a text file representing the corpus
    :return:
    '''
    return re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',corpus)

def bad_sentence(sentence, sent_len):
    '''
    Runs a series of tests to remove suspect sentences. Check for proper punctuation and capitalization.
    :param sentence: sentence to check 
    :param sent_len: min number of words required to be considered a sentence
    :return True or False: True means sentence is bad
    '''
    words = len(sentence.split(' '))
    if words < sent_len: return True
    if sentence[-1] not in ['.','?','!','.)']: return True
    if sentence[0].islower(): return True
    if sentence[0].isdigit(): return True

def validate_sentences(sentences=None, sent_len=10):
    '''
    Iterates through list of sentences in corpus and removes those that start with lowercase letters or numbers, and that are less than a certain length.
    :param sent_len: a list of sentences
    :param length: the minimum length for a sentence
    :return: list of sentences
    '''
    for index,text in enumerate(sentences):
        sentences[index] = clean_corpus(text)
        if bad_sentence(sentences[index], sent_len): sentences.pop(index)
    return sentences

def generate_word2vec_folds(corpus='Empty', folds=3, seed=10):
    '''
    Generates a series of text files that each represent a training or test split of the text data.  Since word2vec does
    not conduct any calculations that rely on interactions across sentence boundaries this cross-validation k-fold generator
    splits the text by sentence and then chooses random sentences together into the same corpus.  This fold generator also
    assumes the original corpus and any ontological additions have not been added to the same file yet.  It expects both.
    The training set includes all of the ontological additions, not just a random subset.
    :return:
    '''
    #tokenize the corpus into sentences because we need to get a random sample of sentences from the resulting list.
    cleaned_corpus=clean_corpus(corpus) #remove random characters from corpus

    tokenized_corpus=tokenize_sentences(cleaned_corpus) #split into sentences

    tokenized_corpus=validate_sentences(tokenized_corpus, 10) #keep only sentences that are >= 10 words, start with capital

    tokenized_corpus=np.array(tokenized_corpus)

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
    :param ontology_text: The raw ontology text.
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
    :param ontology_text: Raw string of constructed ontology sentences.
    :return:
    '''

    if ontology_text is not None:
        for row_index in range(len(folds_dict)):
            folds_dict[row_index]['train'] = folds_dict[row_index]['train'] + ' ' + ontology_text

    return folds_dict

def store_file(folds_dict, input_data_dir):
    '''
    Derive the location to save the resulting json file that includes all of the fold definitions.  Each fold generates a
      seperate directory depending on the number of folds chosen.  Within each fold directory is a train and test directory.
      Files are stored in all proper locations after parsing a dict with all of the data in it..
    :param folds_dict:
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

    specific_data_dir = path.join(data_dir, input_data_dir)

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

def read_source(input_data_dir, source_type='corpus'):
    """
    Reads a set of source files in an input_data_dir and generates a single string from those input files.
    :param input_data_dir: The subject name of the test. For example 'jazz' or 'medical', etc.
    :param source_type: Either 'corpus' or 'ontology'.
    :return:
    """
    # Set data directory
    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, '../..'))

    if source_type == 'corpus':
        data_dir = path.join(parent_dir, 'data')
    else:
        data_dir = path.join(parent_dir, 'ontology')

    this_model_dir = path.join(data_dir, input_data_dir)

    # Below grabs all of the files in the current model directory and builds a single string corpus out of them.  This
    # avoids the sub-directories if they exist.
    input_data = ''
    if path.exists(this_model_dir):
        for some_corpus_file in listdir(this_model_dir):
            if path.isfile(path.join(this_model_dir, some_corpus_file)):
                with open(path.join(this_model_dir, some_corpus_file),'rb') as infile:
                    new_file_data = infile.read()
                    input_data = ''.join((input_data, new_file_data))

        return input_data

    else:
        print 'Could not find the data/ontology directory: ', this_model_dir
        sys.exit(0)


def run(input_data_dir, ontology_flag=False, k=5, seed=10):
    """
    Pulls the corpus and ontology if provided and builds k folds for test and train into the data directory.
    :param input_data_dir:
    :param ontology_flag: If True then we are including an ontology.
    :param k: Number of folds
    :param seed: Any seed number for the split generator for the folds.
    :return:
    """
    corpus = read_source(input_data_dir, source_type='corpus')
    
    if ontology_flag == 'True':
        ontology = read_source(input_data_dir, source_type='ontology')
    else:
        ontology = ''

    corpus_split=generate_word2vec_folds(corpus=corpus, folds=k)
    collapsed_lists=collapse_corpus_sentence_list(folds_dict=corpus_split)
    final_splits=append_ontology_text(folds_dict=collapsed_lists, ontology_text=ontology)
    store_file(folds_dict=final_splits, input_data_dir=input_data_dir)

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-d', '--data_dir', dest='input_data_dir', default='', help='Specify data directory')
    parser.add_option('-k', '--folds', dest='k', default=3, help='Specify number of folds requested', type='int')
    parser.add_option('-o', '--ontology_flag', action='store_true', dest='ontology_flag', default=False, help='if specified, an ontology is provided')
    parser.add_option('-s', '--seed', dest='seed', default=100, help='Specify the seed for the random number generator', type='int')
    (opts, args) = parser.parse_args()

    run(opts.input_data_dir, opts.ontology_flag, opts.k, opts.seed)
