import sys
from os import path, listdir

# TODO: SUPER FRAGILE for this to be in a utils file especially if we move this
# drama
CURRENT_DIR = path.dirname(path.realpath(__file__))
PARENT_DIR = path.abspath(path.join(CURRENT_DIR, '../..'))


def read_source(run_directory, source_type):
    """
    Reads a set of source files in an input_data_dir and generates a single string from those input files.
    :param run_directory: The subject name of the test. For example 'run1' or 'medical', etc.
    :type run_directory: str
    :param source_type: Either 'corpus' or 'ontology'.
    :type source_type: str
    :return: concatenated string of all the files in the source directory
    :rtype: str
    """
    # Figure out data directory

    if source_type == 'corpus':
        data_dir = path.join(PARENT_DIR, 'data', run_directory)
    elif source_type == 'ontology':
        data_dir = path.join(PARENT_DIR, 'ontologies', run_directory)

    # Below grabs all of the files in the current model directory and builds a single string corpus out of them.  This
    # avoids the sub-directories if they exist.
    input_data = ''
    if path.exists(data_dir):
        for some_corpus_file in listdir(data_dir):
            if path.isfile(path.join(data_dir, some_corpus_file)):
                with open(path.join(data_dir, some_corpus_file),'rb') as infile:
                    new_file_data = infile.read()
                    input_data = ''.join((input_data, new_file_data))

        return input_data

    else:
        print 'Could not find the data/ontology directory: ', data_dir
        sys.exit(0)