from os import path, pardir, makedirs, listdir

import gensim
import optparse
import logging
import time
from os import path, listdir

logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):

    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for input_file_name in listdir(self.dirname):
            for line in open(path.join(self.dirname, input_file_name)):
                yield line.split()                                             

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        logging.info('%r %2.4f sec' % (method.__name__, te-ts))
        return result

    return timed

def run_model(input_data_dir, parallel_workers=4, hidden_layer=100, context_window=5, model_name=None):
    """
    This function runs gensim.models.Word2Vec on all folds for a given input data directory.  Specifically, this wrapper function
    derives the proper right directories to search for the data-folds and then loops over those locations running ron_model_fold
    for each.
    :param input_data_dir: The name of the location where the input data is coming.
    :param parallel_workers:
    :param hidden_layer: The number of neurons in the hidden layer of the word2vec model
    :param context_window: The size of teh context window
    :param model_name: the name of the model file to be output.  If none then it outputs the input_data_dir as the filename.
    :return:
    """
    # Set data directory
    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, pardir))

    data_dir = path.join(parent_dir, 'data')
    this_data_dir = path.join(data_dir, input_data_dir)
    models_dir = path.join(parent_dir, 'models')
    this_model_dir = path.join(models_dir, input_data_dir)
    
    if not path.exists(this_model_dir):
        makedirs(this_model_dir)

    #get the folder names under the data directory.  Each directory represents a fold and we need to loop through
    model_directory_fold_directories = filter(lambda x: path.isdir(path.join(this_data_dir, x)), listdir(this_data_dir))

    #loop through each of the fold subdirectories providing the folder location for the data each time and the intended
    # location for the resulting model file to be stored.
    for i in model_directory_fold_directories:
        model_fold_directory=path.join(this_model_dir, i)
        fold_data_directory=path.join(this_data_dir, i)
        fold_model_data_dir = path.join(fold_data_directory, 'train')
        run_model_fold(input_data_dir=input_data_dir,
                       model_data_dir=fold_model_data_dir,
                       this_model_dir=model_fold_directory,
                       parallel_workers=parallel_workers,
                       hidden_layer=hidden_layer,
                       context_window=context_window,
                       model_name=model_name)

def run_model_fold(input_data_dir, model_data_dir, this_model_dir, parallel_workers=4, hidden_layer=100, context_window=5, model_name=None):
    '''
    Build a word2vec model of the provided corpus.
    :param input_data_dir:
    :param parallel_workers:
    :param hidden_layer:
    :param context_window:
    :param model_name:
    :return:
    '''
    corpus = MySentences(model_data_dir)
    model = gensim.models.Word2Vec(corpus, workers=parallel_workers, size=hidden_layer, window=context_window)

    if not path.exists(this_model_dir):
        makedirs(this_model_dir)

    if model_name is None:
        # Replace / with _ to prevent creation of unecessary directories, because this expects the fold structure
        filename = input_data_dir.replace('/', '_')
        logging.info(filename)
        model_path = this_model_dir + '/' + filename +'.model'
    else:
        model_path = this_model_dir + '/' + model_name + '.model'

    model.save(model_path)

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input_data_dir', dest='input_data_dir', default='generic', help='Specify local corpus directory')
    parser.add_option('-p', '--parallel_workers', dest='parallel_workers', default=1, help='Specify the number of parallel threads', type='int')
    parser.add_option('-w', '--window_size', dest='context_window', default=5, help='Specify the context window size', type='int')
    parser.add_option('-l', '--hidden_layer_size', dest='hidden_layer', default=100, help='Specify the hidden layer size', type='int')
    parser.add_option('-o', '--output_model_name', dest='model_name', default=None, help='Specify a name for your model. If not specified, the data directory name will be used.')
    (opts, args) = parser.parse_args()

    if opts.model_name is not None:
        run_model(opts.input_data_dir, opts.parallel_workers, opts.context_window, opts.hidden_layer, opts.model_name)    
    else:
        run_model(opts.input_data_dir, opts.parallel_workers, opts.context_window, opts.hidden_layer)
