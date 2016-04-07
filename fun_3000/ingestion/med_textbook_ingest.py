import codecs
import logging
import optparse
from os import path, pardir, makedirs

from fun_3000.ingestion.utils import get_unicode_response

logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

def save_book(text, storage_path):
	'''
    Save text to file
    :param text: Block of text
    :param storage_path: Path for final file
    '''
	
	logging.info('Saving text to: %s' % storage_path)
	with codecs.open(storage_path, 'w+', 'utf-8') as f_out:
		f_out.write(text)

def get_books(data_directory):
    '''
    Retrieve text of medical textbooks
    :param data_directory: local directory where abstracts will be saved as text files e.g. 'med_books'
    '''
    
    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, pardir))
    root_dir = path.abspath(path.join(parent_dir, pardir))

    grays_url = "https://archive.org/stream/GraysAnatomy40thEd_201403/Gray%27s%20Anatomy%20-%2040th%20Ed_djvu.txt"
    
    #this is from 1920 ... is it too old?
    dict_url = "https://archive.org/stream/cu31924052393315/cu31924052393315_djvu.txt"

    data_dir = path.join(root_dir, 'data')
    if data_directory is not None:
        model_data_dir = path.join(data_dir, data_directory)
    else:
        model_data_dir = path.join(data_dir, 'med_books')

    if not path.exists(model_data_dir):
        makedirs(model_data_dir)

    grays_file_path = model_data_dir + '/' + 'grays_anatomy.txt'
    logging.info("Retrieving Gray's Anatomy text")
    grays_response = get_unicode_response(grays_url)
    save_book(grays_response, grays_file_path)

    dict_file_path = model_data_dir + '/' + 'dict_med_terms.txt'
    logging.info("Retrieving Dictionary of Medical Terms")
    dict_response = get_unicode_response(dict_url)
    save_book(dict_response, dict_file_path)


if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-d', '--data_directory', dest='data_directory', default=None, help='Specify a directory name for saving search data')
    (opts, args) = parser.parse_args()

    data_directory = opts.data_directory

    get_books(data_directory)


