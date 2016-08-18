from wikipedia import page as wpg, search as src
from wikipedia.exceptions import PageError, DisambiguationError
from os import path, pardir, makedirs

import logging
import optparse
import codecs

logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

def save_wiki_text(wiki_search_term, storage_path):
    '''
    Save the contents of a wiki page into a local txt file
    :param wiki_search_term: unique term referring a particular wiki page
    :param storage_path: where to save the file
    '''
    page = wpg(title=wiki_search_term, auto_suggest=False)

    logging.info('Saving data to: %s' % storage_path)
    with codecs.open(storage_path, 'w+', 'utf-8') as f_out:
        f_out.write(page.content)

def get_wikipedia_pages(search_term, data_directory, results=1):
    '''
    Take a search term and look up related pages on wikipedia, then save as many results as needed
    :param search_term: the topic you're looking for
    :param data_directory: where the pages will be saved locally (corpuses are saved each within its own dir under data/)
    :param results: how many related pages to save
    '''

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

    try:
        if search_term is not None:
            # get all the related pages by searching for the base term
            wiki_results = src(search_term, results, suggestion=False)

            # for each related page, save the page's content
            for result in wiki_results:
                logging.info('Retrieving "%s" page from Wikipedia.' % (result))
                local_file_path = model_data_dir + '/' + result.replace('/', '_') + '.txt'
                save_wiki_text(search_term, local_file_path)
                logging.info('Fetched %s term wiki artifacts.' % search_term)
        else:
            logging.info('You have not specified a search term!')
    except (PageError, DisambiguationError) as e:
        print dir(e)
        logging.info("Skipping download for term %s, received error %s" %(search_term, type(e)))


if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-s', '--search_term', dest='search_term', default=None, type='string', help='Specify the wikipedia search term (Default is "Disease")')
    parser.add_option('-d', '--data_directory', dest='data_directory', default=None, help='Specify a directory name for saving search data')
    parser.add_option('-r', '--results', dest='results', default=1, help='Specify the number of search results to be returned by Wikipedia')
    (opts, args) = parser.parse_args()

    search_term = opts.search_term
    data_directory = opts.data_directory
    results = opts.results

    get_wikipedia_pages(search_term, data_directory, results)