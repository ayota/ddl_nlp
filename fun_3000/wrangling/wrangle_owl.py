import rdflib
g = rdflib.Graph()
g.parse(location="http://ogms.googlecode.com/svn/releases/2014-06-20/ontology/ogms.owl"
, format="application/rdf+xml")
f = rdflib.Graph()
# interested to see how many get converted to literals
literal_s = 0
literal_p = 0
literal_o = 0
remaining_s = 0
remaining_p = 0
remaining_o = 0
# query will grab labels for s, p, o where it can find it
# using the namespace rdfs:label
# otherwise it will return the URI
# recommended reading: http://www.cambridgesemantics.com/semantic-university/sparql-by-example#%281%29|
for row in g.query("""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	SELECT ?s ?s_label ?p_label ?o_label ?p ?o
WHERE
{
  ?s ?p ?o .
  ?s rdfs:label ?s_label .
Optional {  ?p rdfs:label ?p_label . }
Optional {  ?o rdfs:label ?o_label . }
}
	"""):
	# construct triples from the info we have
	# if the SPARQL could not find something it is None
	triple = []
	if row.s_label:
		triple.append(row.s_label)
		literal_s= literal_s+1
	if row.p_label:
		triple.append(row.p_label)
		literal_p= literal_p+1
	else:
		triple.append(row.p)
		# checking if p was stored as a literal
		# never happens in this set
		if type(row.p) == rdflib.term.Literal:
			literal_p = literal_p+1
		else:
			remaining_p=remaining_p+1
	if row.o_label:
		triple.append(row.o_label)
		literal_o= literal_o+1
	else:
		triple.append(row.o)
		# checking if o was stored as a literal
		# common in this set
		if type(row.o) == rdflib.term.Literal:
			literal_o = literal_o+1
		else:
			remaining_o=remaining_o+1
	f.add(triple)

# now for metrics
print("length of graph: ", len(f))
# problem URIs appear to be in Turtle
# and specifically items from core i.e. rdf-schema, 22-rdf-syntax-ns, or owl namespaces
print("literal s", literal_s)
print("remaining s", remaining_s)
print("literal p", literal_p)
print("remaining p", remaining_p)
print("literal o", literal_o)
print("remaining o", remaining_o)
# ('length of graph: ', 541)
# ('literal s', 541)
# ('remaining s', 0)
# ('literal p', 295)
# ('remaining p', 246)
# ('literal o', 414)
# ('remaining o', 127)
