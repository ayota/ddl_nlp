from os import path, pardir, makedirs, listdir

import gensim
import optparse
import logging
import time

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

@timeit
def train_model(corpus, parallel_workers=4):
    return gensim.models.Word2Vec(corpus, workers=parallel_workers)

def run_model(input_data_dir, parallel_workers=4, model_name=None):
    
    # Set data directory
    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, pardir))
    
    data_dir = path.join(parent_dir, 'data')
    model_data_dir = path.join(data_dir, cached_corpus_dir)

    models_dir = path.join(parent_dir, 'models')
    this_model_dir = path.join(models_dir, cached_corpus_dir)
    if not path.exists(this_model_dir):
        makedirs(this_model_dir)
  
    corpus = MySentences(model_data_dir)
    model = train_model(corpus, parallel_workers)

    if model_name is None:    
        model_path = this_model_dir + '/' + cached_corpus_dir +'.model'
    else:
        model_path = this_model_dir + '/' + model_name + '.model'

    model.save(model_path)

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input_data_dir', dest='cached_corpus_dir', default='generic', help='Specify local corpus directory')
    parser.add_option('-p', '--parallel_workers', dest='parallel_workers', default=1, help='Specify the number of parallel threads', type='int')
    parser.add_option('-o', '--output_model_name', dest='model_name', default=None, help='Specify a name for your model. If not specified, the data directory name will be used.')
    (opts, args) = parser.parse_args()

    if opts.model_name is not None:
        run_model(opts.cached_corpus_dir, opts.parallel_workers, opts.model_name)    
    else:
        run_model(opts.cached_corpus_dir, opts.parallel_workers)
 