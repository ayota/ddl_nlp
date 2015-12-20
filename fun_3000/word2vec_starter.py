from wikipedia import page as wpg
from os import path, pardir, makedirs, listdir

import gensim
import optparse
import codecs
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
def train_model(corpus, parallel_workers):
    return gensim.models.Word2Vec(corpus, workers=parallel_workers)

def run_model(cached_corpus_dir, parallel_workers, local_data_file='model_data.txt'):
    
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

    model_path = this_model_dir + '/' + cached_corpus_dir + '.model'
    model.save(model_path)

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-c', '--cached', dest='cached_corpus_dir', default='generic', help='Specify locally cached corpus directory')
    parser.add_option('-p', '--parallel_workers', dest='parallel_workers', default=1, help='Specify the number of parallel threads', type='int')
    (opts, args) = parser.parse_args()

    run_model(opts.cached_corpus_dir, opts.parallel_workers)
 