import rdflib
g = rdflib.Graph()
g.parse(location="http://ogms.googlecode.com/svn/releases/2014-06-20/ontology/ogms.owl"
, format="application/rdf+xml")
for subj, pred, obj in g:
	print(subj, pred, obj)