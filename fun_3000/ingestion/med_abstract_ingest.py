from os import path, pardir, makedirs
from ConfigParser import SafeConfigParser

import urllib2
import logging
import optparse
import codecs
import xmltodict

logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

CONFIG_PARSER = SafeConfigParser()
CONFIG_PARSER.read('ingestion_config.py')

def get_unicode_response(url):
    '''
    Do an HTTP GET, figure out the charset and convert to unicode
    :param url: Web URL where HTTP GET will be submitted
    :return: Unicode string
    '''

    query_response = urllib2.urlopen(url)
    query_response_content = query_response.read()
    encoding = query_response.headers['content-type'].split('charset=')[-1]
    unicode_reponse = unicode(query_response_content, encoding)
    return unicode_reponse


def get_document_ids(query_response, results):
    '''
    Returns a list of pubmed document ids from a search query XML response
    :param query_response: xml response provided by pubmed
    :return: list of document ids
    '''
    response_xml = xmltodict.parse(query_response)

    doc_list = []
    if results > 1:
        doc_list = [doc_id for doc_id in response_xml['eSearchResult']['IdList']['Id']]
    else:
        doc_list.append(''.join(response_xml['eSearchResult']['IdList']['Id']))

    return doc_list


def save_abstract_text(document_id, doc_url, storage_path):
    '''
    Fetch a medical abstract and save it 
    :param document_id: the query search term used for looking up the medical abstract 
    :param doc_url: URL for the online medical database document repository
    :param storage_path: path where to save the abstract fetched
    '''

    document_url = doc_url.replace('<DOC_ID>', document_id)
    doc_query_response = get_unicode_response(document_url)

    logging.info('Saving data to: %s' % storage_path)
    with codecs.open(storage_path, 'w+', 'utf-8') as f_out:
        f_out.write(doc_query_response)

def get_medical_abstracts(search_term, data_directory, results=1):
    '''
    Retrieve a list of abstract texts from a search query
    :param search_term: the query search term used for looking up the medical abstracts e.g. 'virus'
    :param data_directory: local directory where abstracts will be saved as text files e.g. 'virus'
    :param results: how many abstracts do we want to fetch
    '''
    
    global CONFIG_PARSER
    db_url = CONFIG_PARSER.get('medical_abstracts', 'pubmed_search_url')
    doc_url = CONFIG_PARSER.get('medical_abstracts', 'pubmed_doc_url')

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
        
        medical_url =  db_url.replace('<SEARCH_TERM>', search_term).replace('<RESULTS>', str(results))
        query_response = get_unicode_response(medical_url)

        document_ids = get_document_ids(query_response, results)

        for doc_id in document_ids:
            logging.info('Retrieving document #%s from nlm.nih.gov' % (doc_id))
            local_file_path = model_data_dir + '/' + doc_id + '.txt'
            save_abstract_text(doc_id, doc_url, local_file_path)
    else:
        logging.info('You have not specified a search term!')

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-s', '--search_term', dest='search_term', default=None, type='string', help='Specify the wikipedia search term (Default is "Disease")')
    parser.add_option('-d', '--data_directory', dest='data_directory', default=None, help='Specify a directory name for saving search data')
    parser.add_option('-r', '--results', dest='results', default=1, type=int, help='Specify the number of search results to be returned by Wikipedia')
    (opts, args) = parser.parse_args()

    search_term = opts.search_term
    data_directory = opts.data_directory
    results = opts.results

    get_medical_abstracts(search_term, data_directory, results)

