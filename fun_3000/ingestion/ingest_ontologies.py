import rdflib
from copy import copy
import progressbar
from os import path, pardir, makedirs
import optparse

def ingest_and_wrangle_owls(data_dir):
    """
    Ingest some instance ontologies with the OGMS ontology and create individual txt files that
    represent instance ontology->OGMS `rdfs:subClassOf` relationships with the sentence
    {instance ontology label} is {OGMS superclass label}
    """

    # set up locations
    current_dir = path.dirname(path.realpath(__file__))
    parent_dir = path.abspath(path.join(current_dir, pardir))
    root_dir = path.abspath(path.join(parent_dir, pardir))

    # set up where our ontologies are going to go
    output_dir = path.join(data_dir, "ontologies")
    if not path.exists(output_dir):
        makedirs(output_dir)

    # various rdf locations
    # let's mix OGMS ontology with instance ontologies
    OGMS = "http://ogms.googlecode.com/svn/releases/2014-06-20/ontology/ogms.owl"
    # make a graph we'll read our stuff into
    ogms_graph = rdflib.Graph().parse(location=OGMS, format='application/rdf+xml')

    # get instance ontologies from config
    from ConfigParser import SafeConfigParser
    CONFIG_PARSER = SafeConfigParser()
    CONFIG_PARSER.read(current_dir + '/ingestion_config.py')
    other_ontologies = CONFIG_PARSER.items('ontologies')

    import pdb; pdb.set_trace()

    progress = 0
    with progressbar.ProgressBar(max_value=len(other_ontologies)) as bar:
        for ontology in other_ontologies:
            name = ontology[0]
            location = ontology[1]
            progress += 1
            g = copy(ogms_graph)

            # parse them into our holding graph 'g'
            g.parse(location=OGMS, format="application/rdf+xml")
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
            bar.update(progress)

if __name__=='__main__':
    parser = optparse.OptionParser()
    parser.add_option('-d', '--data_directory', dest='data_directory', default=None, help='Specify a parent directory name relative to where you are running the script for saving ontology data e.g. data to put in data/ontologies')
    (opts, args) = parser.parse_args()

    data_directory = opts.data_directory

    ingest_and_wrangle_owls(data_directory)