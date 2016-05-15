import logging
import ingestion
import optparse
import csv


logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

def import_terms(filename):
	'''
	Imports list of terms from csv, returns Python list
	:param filename: filename of csv
	:return: list
	'''
	search_terms = []

	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			search_terms.extend(row)
			
	return search_terms

def fetch_corpus(search_terms, data_dir, results):
	'''
	Runs through list of search terms for wikipedia and abstract ingestion functions. NOTE: This function returns
	nothing because it is simply saving the results to the filesystem for each search term.
	:param search_terms: a list of search terms.
	:param results: number of results to get from each source
	'''

	logging.info('Fetching wikipedia articles and medical abstracts')

	wiki_search = ingestion.wikipedia_ingest
	med_search = ingestion.med_abstract_ingest

	for term in search_terms:
		wiki_search.get_wikipedia_pages(term, data_dir, results)
		logging.info('Fetched %s term wiki artifacts.' % term)
		med_search.get_medical_abstracts(term, data_dir, results)
		logging.info('Fetched %s term medical abstract artifacts.' % term)

def fetch_books(directory):
	'''
	:param directory: filename for medical text directory
	'''

	logging.info('Fetching books')

	book_grab = ingestion.med_textbook_ingest
	book_grab.get_books(directory)

def fetch_ontologies(directory):
	"""
	Based on source and instance ontologies specified in ingestion/ingestion_config.conf, generate sentences from those ontologies
	:param directory:  parent directory for 'ontologies' subdirectory that will hold all the ontologies
	"""

	ontology_grab = ingestion.ingest_ontologies
	ontology_grab.ingest_and_wrangle_owls(directory)

if __name__ == '__main__':
	"""
	Usage:
		python get_corpus.py -s [CSV OF SEARCH TERMS] -r [NUM RESULTS YOU WANT RETURNED] -d [DIRECTORY FOR ALL FETCHED FILES]
	"""

	parser = optparse.OptionParser()
	parser.add_option('-s', '--search_file', dest='search_file', default=None, type='string', help='Specify the filename for list of search terms; default is med_terms.csv.')
	parser.add_option('-r', '--results', dest='results', default=1, type=int, help='Specify the number of search results to be returned by abstract queries.')
	parser.add_option('-d', '--directory', dest='directory', default=1, type='string', help='Specify a directory for corpus text and ontology.')

	(opts, args) = parser.parse_args()

	search_file = opts.search_file
	results = opts.results
	directory = opts.directory

	search_terms = import_terms(search_file)
	fetch_corpus(search_terms, directory, results)
	fetch_books(directory)
	fetch_ontologies(directory)
