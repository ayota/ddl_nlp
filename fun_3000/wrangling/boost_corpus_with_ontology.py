import io
import optparse
from os import path

from utils import PARENT_DIR, read_source


def run(run_directory, corpus_filename="output.txt", multiplier=1):
    """
    Pulls the corpus and ontology if provided and builds k folds for test and train into the data directory.
    :param run_directory:
    :param corpus_filename: filename inside the run directory that is where the cleaned corpus file is stored.
    :param multiplier: int by which to multiply the available ontologies in each training fold
    :return:
    """
    # figure out where the corpus file is. should be in ddl_nlp/data/{run_directory}/{corpus_filename}
    absolute_corpus_filename = path.join(PARENT_DIR, 'data', run_directory, corpus_filename)
    with io.open(absolute_corpus_filename, "rt") as f:
        # TODO: right now this reads the entire corpus into a list at once
        # we probably want to change this into a generator later so we can stream this information
        # but we have to address how to random sample a generator in generate_folds.py to do so
        corpus = f.read()

    # get our ontology file
    ontology = read_source(run_directory, source_type='ontology')

    ontology_text = ontology + ' '
    ontology_text = ontology_text * multiplier
    corpus_with_ontology_multiplier_appended = corpus + ' ' + ontology_text

    # construct filename based on input corpus name and multiplier
    # e.g. filename 'output.txt' and multiplier `5` would result in output filename 5_boost_output.txt
    output_filename = path.join(PARENT_DIR, 'data', run_directory, "%s_boost_%s" % (multiplier, corpus_filename))
    with io.open(output_filename, "wt") as f:
        f.write(corpus_with_ontology_multiplier_appended)

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-d', '--run_directory', dest='run_directory', default='', help='Specify run directory name e.g. run1 for files in data/run1')
    parser.add_option('-f', '--filename', dest='corpus_filename', default="output.txt", help="Specify the name of the cleaned corpus file generated from the data directory.")
    parser.add_option('-m', '--multiplier', dest='multiplier', default=1, type='int', help="How much you want to multiply the ontologies by in each fold.")
    (opts, args) = parser.parse_args()

    run(opts.run_directory, opts.corpus_filename, opts.multiplier)
