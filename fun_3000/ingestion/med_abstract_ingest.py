from os import path, pardir, makedirs
from ConfigParser import SafeConfigParser
from Bio import Entrez

import urllib2
import logging
import optparse
import codecs
import xmltodict
import re

logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

def get_unicode_response(url):
    '''
    Do an HTTP GET, figure out the charset and convert to unicode
    :param url: Web URL where HTTP GET will be submitted
    :return: Unicode string
    '''
    try:
        query_response = urllib2.urlopen(url)
        query_response_content = query_response.read()
        encoding = query_response.headers['content-type'].split('charset=')[-1]
        unicode_response = unicode(query_response_content, encoding)
    except:
        #bad status line error ... can't fix it
        unicode_response = ''
    
    return unicode_response

def pub_get_ids(query, results):
    '''
    Returns a list of pubmed document ids from a search query XML response
    :param query_response: xml response provided by pubmed
    :param results: int number of results to return
    :return: list of document ids
    '''
    Entrez.email = 'ecayoz@gmail.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax=str(results),
                            retmode='xml', 
                            term=query)
    ids = Entrez.read(handle)
    return ids

def pub_get_papers(id_list):
    '''
    Returns a list of pubmed document ids from a search query XML response
    :param id_list: List of ids
    :return abstracts: Abstracts for given doc ids
    '''

    ids = ','.join(id_list)
    Entrez.email = 'ecayoz@gmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    abstracts = Entrez.read(handle)
    return abstracts

def fetch_pubmed(search_term, results):
    '''
    Fetch a medical abstract
    :param search_term: the query search term used for looking up the medical abstract
    :param results: int number of results to return
    :return: list of abstracts
    '''

    ids = pub_get_ids(search_term, results)
    id_list = ids['IdList']
    papers = pub_get_papers(id_list)
    abstracts = []

    for index, paper in enumerate(papers):
        try:
            summary = paper['MedlineCitation']['Article']['Abstract'].values()
        except KeyError:
            logging.info('Document does not have abstract.')

        for item in summary:
            abstracts.extend(item)

    return abstracts


def fetch_arxiv(query_response):
    '''
    Fetch results from query Arxiv, then parses xml to get abstracts
    :param query_response: url to for an Arxiv query
    :return: list of abstracts
    '''

    entries = xmltodict.parse(query_response, process_namespaces=True)[u'http://www.w3.org/2005/Atom:feed'][u'http://www.w3.org/2005/Atom:entry']

    try:
        abstracts = [entry['http://www.w3.org/2005/Atom:summary'] for entry in entries]
    except TypeError:
        abstracts = entries['http://www.w3.org/2005/Atom:summary']

    return abstracts

def fetch_medline(document_url):
    '''
    Fetch results from MedlinePlus query, then parses XML to get abstracts
    :param document_url: search query as url
    :return: list of abstracts
    '''

    query_response = get_unicode_response(document_url)
    entries = xmltodict.parse(query_response, process_namespaces=True)[u'nlmSearchResult'][u'list'][u'document']

    abstracts = []

    try:
        for entry in entries:
            for line in entry[u'content']:
                vals = line.values()
                if vals[0] == u'FullSummary':
                    text = vals[1]
                    abstracts.append(text)
    except TypeError:
        # only one result returned
        for line in entries[u'content']:
            vals = line.values()
            if vals[0] == u'FullSummary':
                text = vals[1]
                abstracts.append(text)

    return abstracts

def save_file(storage_path, abstracts):
    '''
    Save list of abstracts to file.
    :param storage_path: Storage path for the file.
    :param abstracts: List of abstracts
    '''

    with codecs.open(storage_path, 'a+', 'utf-8') as f_out:
        blob = ' '.join(abstracts)
        f_out.write(abstracts)

def get_medical_abstracts(search_term, data_directory, results=1):
    '''
    Retrieve a list of abstract texts from a search query
    :param search_term: the query search term used for looking up the medical abstracts e.g. 'virus'
    :param data_directory: local directory where abstracts will be saved as text files e.g. 'virus'
    :param results: how many abstracts we want to fetch
    '''
    
    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, pardir))
    root_dir = path.abspath(path.join(parent_dir, pardir))

    CONFIG_PARSER = SafeConfigParser()
    CONFIG_PARSER.read(current_dir + '/ingestion_config.py')
    # pubmed_search_url = CONFIG_PARSER.get('medical_abstracts', 'pubmed_search_url')
    arxiv_search_url = CONFIG_PARSER.get('medical_abstracts', 'arxiv_search_url')
    medline_search_url = CONFIG_PARSER.get('medical_abstracts', 'medline_search_url')
    # pubmed_doc_url = CONFIG_PARSER.get('medical_abstracts', 'pubmed_doc_url')

    data_dir = path.join(root_dir, 'data')
    if data_directory is not None:
        model_data_dir = path.join(data_dir, data_directory)
    else:
        model_data_dir = path.join(data_dir, search_term)

    if not path.exists(model_data_dir):
        makedirs(model_data_dir)

    if search_term is not None:
        local_file_path = model_data_dir + '/' + search_term + '.txt'

        #add pubmed to file
        abstracts_pubmed = fetch_pubmed(search_term, results)
        save_file(local_file_path, abstracts_pubmed)

        #add arxiv to file
        arxiv_url =  arxiv_search_url.replace('<SEARCH_TERM>', search_term).replace('<RESULTS>', str(results))
        query_response = get_unicode_response(arxiv_url)
        if query_response != '':
            abstracts_arxiv = fetch_arxiv(query_response)
            save_file(local_file_path, abstracts_arxiv)

        #add medline to file
        medline_url =  medline_search_url.replace('<SEARCH_TERM>', search_term).replace('<RESULTS>', str(results))
        abstracts_medline = fetch_medline(medline_url.rstrip())
        save_file(local_file_path, abstracts_medline)

    else:
        logging.info('You have not specified a search term!')

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-s', '--search_term', dest='search_term', default=None, type='string', help='Specify the desired search term (Default is "Disease")')
    parser.add_option('-d', '--data_directory', dest='data_directory', default=None, help='Specify a directory name for saving search data')
    parser.add_option('-r', '--results', dest='results', default=1, type=int, help='Specify the number of search results to be returned by abstract queries.')
    (opts, args) = parser.parse_args()

    search_term = opts.search_term
    data_directory = opts.data_directory
    results = opts.results

    get_medical_abstracts(search_term, data_directory, results)

