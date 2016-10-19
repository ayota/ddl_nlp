import rdflib
from copy import copy
from os import path, pardir, makedirs
import optparse
import logging

def ingest_and_wrangle_owls(data_directory):
    """
    Ingest some instance ontologies with the source ontology and create individual txt files that
    represent instance ontology->source ontology `rdfs:subClassOf` relationships with the sentence
    {instance ontology label} is {source ontology superclass label}
    """

    # set up locations
    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, pardir))
    root_dir = path.abspath(path.join(parent_dir, pardir))
    data_dir = path.join(root_dir, 'data')

    # set up where our ontologies are going to go, in {root dir}/data/{data directory name}/ontologies
    output_dir = path.join("ontologies", data_directory)
    if not path.exists(output_dir):
        makedirs(output_dir)
    # get source and instance ontologies from config
    from ConfigParser import SafeConfigParser
    CONFIG_PARSER = SafeConfigParser()
    CONFIG_PARSER.read(current_dir + '/ingestion_config.conf')
    other_ontologies = CONFIG_PARSER.items('ontologies')
    # get the source ontology which should be the first one in the config file
    source_ontology = other_ontologies.pop(0)
    # get the source ontology which should be the first one in the config file
    source_ontology_fallback = other_ontologies.pop(0)
    # make a graph we'll read our stuff into
    # for now this checks two seperate locations for the source owl file.
    try:
        source_graph = rdflib.Graph().parse(location=source_ontology[1], format='application/rdf+xml')
        logging.info('Used the main location to retrieve the owl located at http://ogms.googlecode.com/svn/releases/2014-06-20/ontology/ogms.owl')
    except:
        source_graph = rdflib.Graph().parse(location=source_ontology_fallback[1], format='application/rdf+xml')
        logging.info('Used the fallback (2nd option) to retrieve the owl located at https://raw.githubusercontent.com/OGMS/ogms/master/src/ontology/ogms.owl')

    progress = 0
    for ontology in other_ontologies:
        name = ontology[0]
        location = ontology[1]
        progress += 1
        g = copy(source_graph)

        try:
            # parse instance ontology into our holding graph 'g'
            g.parse(location=location, format="application/rdf+xml")

            # a query to get slabel and olabel where the relationships is rdfs:subClassOf
            query = """SELECT ?slabel ?label
                        WHERE
                            {?s rdfs:subClassOf ?o .
                            ?s rdfs:label ?slabel .
                            FILTER (isIRI(?o)).
                            ?o rdfs:label ?label} """
            # write it down
            with open(path.join(output_dir, name+".txt"), "w") as writer:
                for row in g.query(query):
                    # save these triples somewhere
                    writer.write("{s} {p} {o}\n".format(s=row[0], p="is", o=row[1]))
            logging.info('Successfully retrieved ontology from %s' % location)
        except: #if does not exist then log it!
            logging.warning('Could not locate %s' % location)

        print(logging.info('Ontology %s of %s complete.' % (str(progress), len(other_ontologies))))


if __name__=='__main__':
    """Usage:

    python ingest_ontologies.py -d run1

    """

    parser = optparse.OptionParser()
    parser.add_option('-d', '--data_directory', dest='data_directory', default=None, help='Specify a directory name to save ontology data in e.g. run1 to put in /ddl_nlp/ontologies/run1/')
    (opts, args) = parser.parse_args()

    data_directory = opts.data_directory

    ingest_and_wrangle_owls(data_directory)
