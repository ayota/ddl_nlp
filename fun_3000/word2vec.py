from os import path, pardir, makedirs, listdir

import gensim
import optparse
import logging
import time
from os import path, listdir

logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        for line in open(path.join(self.file_path)):
            yield line.split()

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        logging.info('%r %2.4f sec' % (method.__name__, te-ts))
        return result

    return timed

def run_model(data_directory, boosted_filename, parallel_workers=4, hidden_layer=100, context_window=5, model_name=None):
    '''
    Build a word2vec model of the provided corpus.
    :param data_directory:
    :param parallel_workers:
    :param hidden_layer:
    :param context_window:
    :param model_name:
    :return:
    '''
    # Set data directory
    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, pardir))

    abs_path_to_data_directory = path.join(parent_dir, 'data', data_directory)
    input_file_path = path.join(abs_path_to_data_directory, boosted_filename)

    corpus = MySentences(input_file_path)
    model = gensim.models.Word2Vec(corpus, workers=parallel_workers, size=hidden_layer, window=context_window)

    # Replace / with _ to prevent creation of unecessary directories, because this expects the fold structure
    filename = data_directory.replace('/', '_')
    logging.info(filename)
    model_path = abs_path_to_data_directory + '/' + filename +'.model'

    print model_path
    model.save(model_path)

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-d', '--data_directory', dest='data_directory', default='generic', help='Specify local corpus directory')
    parser.add_option('-f', '--filename', dest='input_filename', default='1_boost_output.txt',
                      help="Specify the name of the file that contains the boosted corpus.")
    parser.add_option('-p', '--parallel_workers', dest='parallel_workers', default=1, help='Specify the number of parallel threads', type='int')
    parser.add_option('-w', '--window_size', dest='context_window', default=5, help='Specify the context window size', type='int')
    parser.add_option('-l', '--hidden_layer_size', dest='hidden_layer', default=100, help='Specify the hidden layer size', type='int')

    (opts, args) = parser.parse_args()

    run_model(opts.data_directory, opts.input_filename, opts.parallel_workers, opts.context_window, opts.hidden_layer)