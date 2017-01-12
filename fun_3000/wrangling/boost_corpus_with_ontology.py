import io
import optparse
from os import path, listdir
import shutil

from utils import PARENT_DIR, read_source


def run(run_directory, corpus_filename="output.txt", multiplier=1):
    """
    Takes a corpus file and appends ontology user-specified number of times. Output filename is of format [MULTIPLIER]_boost_[CORPUS_FILENAME] (e.g. filename 'output.txt' and multiplier `5` would result in output filename 5_boost_output.txt)

    :param run_directory: where the data for the given run is stored (e.g., run_1, run_2)
    :param corpus_filename: what the clean corpus file is called within the run directory
    :param multiplier: int by which to multiply the available ontologies
    :return:
    """
    # figure out where the corpus file is. should be in ddl_nlp/data/{run_directory}/{corpus_filename}
    absolute_corpus_filename = path.join(PARENT_DIR, 'data', run_directory, corpus_filename)

    # construct filename based on input corpus name and multiplier
    output_filename = path.join(PARENT_DIR, 'data', run_directory, "%s_boost_%s" % (multiplier, corpus_filename))

    # copy corpus file data into output file
    shutil.copy(absolute_corpus_filename, output_filename)

    # Get our ontology file.
    # Step 1: We have an ontology directory and we want to loop over the files inside. 
    # Step 2: For each open file, we want to add a space and multiply it by the multiplier.
    # Step 3: Append to the output corpus. 

    ontology_path = path.join(PARENT_DIR, 'ontologies', run_directory)

    files = listdir(run_directory)
    for fn in files:
        with io.open(fn, 'rt') as ontology:
            ontology_text = ontology.read() + ' '
            ontology_text = ontology_text * multiplier

        with io.open(output_filename, "at") as f:
            f.write('\n') # maybe for nice formatting?
            f.write(ontology_text)

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-d', '--run_directory', dest='run_directory', default='', help='Specify run directory name, e.g. run_1 for files in data/run_1')
    parser.add_option('-f', '--filename', dest='corpus_filename', default='output.txt', help='Specify the name of the cleaned corpus file generated from the data directory.')
    parser.add_option('-m', '--multiplier', dest='multiplier', default=1, type='int', help='Specify how many times you want to append the ontologies to the corpus.')
    (opts, args) = parser.parse_args()

    run(opts.run_directory, opts.corpus_filename, opts.multiplier)
