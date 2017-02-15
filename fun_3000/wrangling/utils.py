import sys
from os import path, listdir
import io

# TODO: SUPER FRAGILE for this to be in a utils file especially if we move this
# drama
CURRENT_DIR = path.dirname(path.realpath(__file__))
PARENT_DIR = path.abspath(path.join(CURRENT_DIR, '../..'))


def read_source(path):
    """
    Reads a set of source files in an input_path and generates a single string from those input files.
    :param run_directory: The subject name of the test. For example 'run1' or 'medical', etc.
    :type run_directory: str
    :return: concatenated string of all the files in the source directory
    :rtype: str
    """
    # Below grabs all of the files in the current model directory
    # and yields ascii decoded lines from them.
    # avoids the sub-directories if they exist.
    for some_corpus_file in listdir(path):
        if path.isfile(path.join(path, some_corpus_file)):
            with io.open(path.join(path, some_corpus_file),'rb') as infile:
                for line in infile.readlines():
                    yield line.decode(encoding='ascii', errors='ignore')