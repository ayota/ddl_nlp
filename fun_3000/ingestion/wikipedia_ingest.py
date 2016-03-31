from wikipedia import page as wpg, search as src
from os import path, pardir, makedirs

import logging
import optparse
import codecs

logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

def save_wiki_text(wiki_search_term, storage_path):
    page = wpg(wiki_search_term)
    
    logging.info('Saving data to: %s' % storage_path)
    with codecs.open(storage_path, 'w+', 'utf-8') as f_out:
        f_out.write(page.content)

def main():

    parser = optparse.OptionParser()
    parser.add_option('-s', '--search_term', dest='search_term', default=None, type='string', help='Specify the wikipedia search term (Default is "Disease")')
    parser.add_option('-d', '--data_directory', dest='data_directory', default=None, help='Specify a directory name for saving search data')
    parser.add_option('-r', '--results', dest='results', default=1, help='Specify the number of search results to be returned by Wikipedia')
    (opts, args) = parser.parse_args()

    search_term = opts.search_term
    data_directory = opts.data_directory
    results = opts.results

    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, pardir))
    root_dir = path.abspath(path.join(parent_dir, pardir))

    data_dir = path.join(root_dir, 'data')
    if data_directory is not None:
        model_data_dir = path.join(data_dir, data_directory)
    else:
        model_data_dir = path.join(data_dir, search_term)

    if not path.exists(model_data_dir):
        makedirs(model_data_dir)

    if search_term is not None:
        wiki_results = src(search_term, results)

        for result in wiki_results:
            logging.info('Retrieving "%s" page from Wikipedia.' % (result))
            local_file_path = model_data_dir + '/' + result.replace('/', '_') + '.txt'
            save_wiki_text(search_term, local_file_path)
    else:
        logging.info('You have not specified a search term!')

if __name__ == '__main__':
    main()