import rdflib
from copy import copy
import progressbar

# various rdf locations
# let's mix OGMS ontology with instance ontologies

OGMS = "http://ogms.googlecode.com/svn/releases/2014-06-20/ontology/ogms.owl"
# make a graph we'll read our stuff into
ogms_graph = rdflib.Graph().parse(location=OGMS, format='application/rdf+xml')

# some instance ontologies
other_ontologies = {
    "INFECTIOUS DISEASE": {
        "output_filename": "infectious_disease.txt",
        "location": "http://infectious-disease-ontology.googlecode.com/svn/releases/2014-08-01/ido.owl"
    },
    "ORAL HEALTH AND DISEASE": {
        "output_filename": "oral_health_and_disease.txt",
        "location": "http://purl.obolibrary.org/obo/ohd/dev/ohd.owl"
    },
    "BIOMEDICAL INVESTIGATIONS": {
        "output_filename": "biomedical_investigations.txt",
        "location": "http://purl.obolibrary.org/obo/obi.owl"
    }
}

progress = 0
with progressbar.ProgressBar(max_value=len(other_ontologies)) as bar:
    for graph in other_ontologies:
        progress += 1
        g = copy(ogms_graph)

        # parse them into our holding graph 'g'
        g.parse(location=OGMS, format="application/rdf+xml")
        g.parse(location=other_ontologies[graph]['location'], format="application/rdf+xml")

        # a query to get slabel and olabel where the relationships is rdfs:subClassOf
        query = """SELECT ?slabel ?label
                    WHERE
                        {?s rdfs:subClassOf ?o .
                        ?s rdfs:label ?slabel .
                        FILTER (isIRI(?o)).
                        ?o rdfs:label ?label} """

        with open(other_ontologies[graph]['output_filename'], "w") as writer:
            for row in g.query(query):
                # save these triples somewhere
                writer.write("{s} {p} {o}\n".format(s=row[0], p="is", o=row[1]))
        bar.update(progress)
