import requests
r = requests.get("http://ogms.googlecode.com/svn/releases/2014-06-20/ontology/ogms.owl")
with open("ogms.owl", "w") as f: #need a real place to put this
	f.write(r.text) # is a unicode object