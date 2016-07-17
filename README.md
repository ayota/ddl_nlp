# ddl_nlp: Ontology Assisted NLP. 
Repo for DDL research lab project.  The codebase takes care of all ingestion, training, and evaluation for ontology 
assisted word2vec training activities. A Drakefile is used to conduct the entire pipeline AFTER ingestion through evaluation.

### WORKFLOW: Drake
We maintain both a master and a develop branch.  All features are to be built as a branch off of develop and pull requests (pr) will be made into develop.  Only major releases will be pulled into the master branch.

#### Running a pipeline with Drake

Requirement: Make sure Drake is installed. See [here](https://github.com/Factual/drake) for installation instructions.

##### Step 1: Configuration

Place a blank file named workflow.start in whichever data directory you want to use for the pipeline run. (IMPORTANT: if you end up changing your corpus file(s), you'll need to remove the workflow.start file and recreate it)

Open the file named Drakefile and change any of the configuration settings at the top of the file. They correspond to the same options that the word2vec.py script supports.

##### Step 2: Execution

All you need to do is run the following from the main directory:

```
drake -w Drakefile
```

Review the steps and enter 'y' to accept them.

### Post-Execution

Drake will create a workflow/ directory to store some progress files and track step completion. If you wish to re-start the pipeline from a particular step, delete the corresponding .complete file from the workflow/ directory.



### Ingestion

The ingestion module pulls ontologies along with text from several sources and stores them in two files (one for 
ontologies, one for text). There is a controller script, `get_corpus.py`, which pulls data from all sources based on a 
set of search terms submitted via csv.

#### Ingestion: Controller script

Required inputs when running the get_corpus script are described below.

-s = Specify the filename for list of search terms; default is med_terms.csv.
-r = Specify the number of search results to be returned by abstract queries. By default, the script fetches the top 
result from each source ('wikipedia', 'arxiv', 'pub med' and 'medline') for each term in the 'search_file'. This can be 
changed by setting the `-r` option. Both search term and directory name are required.
-d = Specify a directory for corpus text and ontology.  This is the specific name of the test we are running. example: 'run_2'

An example of how to run the ingestion controller script is shown below:

```
python fun_3000/get_corpus.py -s path_to_search_file -d run_1 

```
Where 'path_to_search_file' is a txt file with a list of terms you want to search.

#### Pulling from individual sources

Data can be pulled from each source individually by importing the ingestion module and running the individual commands.
get_corpus is simply a wrapper that grabs everything.  You can also just run the ingestion scripts individually from the
command line.

The options of scripts to run from the command line are below:

ingestion/med_abstract_ingest.py
ingestion/wikipedia_ingest.py
ingestion/med_textbook_ingest.py
ingestion/ingest_ontologies.py

##### Wikipedia

Grabs up to the desired number of results (defined by results parameter `-r`) for the specified search term (term) and 
puts them in the specified directory (data_dir). **update when wikipedia ingest updated to exclude reference/notes section**

```
import ingestion

wiki_search = ingestion.wikipedia_ingest
wiki_search.get_wikipedia_pages(term={some_term}, data_dir={data/some_run}, results= {some int})
```

##### Medical abstracts
Grabs up to the desired number of results (defined by results parameter) for the specified search term (term) and puts 
them in the specified directory (data_dir).

This will search three journal sites with STEM articles:

* [Arxiv](https://arxiv.org/)

* [PubMed](http://www.ncbi.nlm.nih.gov/pubmed)

* [Medline](http://www.mrc-lmb.cam.ac.uk/genomes/madanm/pres/pubmed1.htm) (via [biopython package](http://biopython.org/DIST/docs/api/Bio.Entrez-module.html))


```
import ingestion

med_search = ingestion.med_abstract_ingest
med_search.get_medical_abstracts(term={some_term}, data_dir={data/some_run}, results= {some int})
```

##### Medical textbooks

This imports two texts into the specified directory:

* [Gray's Anatomy](ttps://archive.org/stream/GraysAnatomy40thEd_201403/Gray%27s%20Anatomy%20-%2040th%20Ed_djvu.txt)

* [Stedman's Medical Dictionary](https://archive.org/stream/cu31924052393315/cu31924052393315_djvu.txt)

```
import ingestion

book_grab = ingestion.med_textbook_ingest
book_grab.get_books(directory)
```

##### Ontologies

Ontologies are formal specifications of linguistic relationships designed by domain experts and linguists, usually described on the web using XML-based syntaxes RDF ([w3c](https://www.w3.org/RDF/)) or its superset OWL and OWL derivatives ([w3c](https://www.w3.org/2001/sw/wiki/OWL)). Ontologies are intended to build on one another to enforce a common vocabulary. For example a popular base ontology is FOAF (aka friend-of-a-friend ([wikpedia](https://en.wikipedia.org/wiki/FOAF_(ontology))), which provides a common vocabulary for describing relationships and attributes between and about people. Ontologies are also intended to be accessible over the [Semantic Web/web of data](https://www.w3.org/2013/data/) and thus should live and refer to each other on the web using URIs accessible over http.

Ontologies can be separated into what we here refer to as 'base ontologies' or 'instance ontolgoies'. Base ontologies represent common vocabularies relevant to describe relationships and attributes for entities within a specific domain (such as FOAF, or in our case for fun_3000, OGMS (Ontology for General Medical Science, [ref](https://bioportal.bioontology.org/ontologies/OGMS)). Instance ontologies use the structure provided by the base ontology to link language instances heirarchically back with a base ontology so that certain logical conclusions can be made across instances using the base ontology as a backbone. For example, knowing that A is a type of B and B is a type of C, logically you can conclude that A is a type of C; specifying the relationships between A, B, and C in instance ontologies using the relations and attribute of a base ontology allow such logical conclusions to be made against the web of data.

For fun_3000, URLs to RDF/XML MIME-type ontology files are specified in the `[Ontologies]` section of the configuration file `fun_3000/ingestion/ingestion_config.conf`. In this conf file you must describe:

- `source_ontology`: in our terminology, this is the base ontology our instance ontologies will derive meaning from
- `source_ontology_fallback`: a private host of the source ontology in case of internet problems
- any number of instance ontologies that utilize structure from the `source_ontology` that are specified with a variable name that uniquely identifies them and the URL to their location

Ontologies are ingested and parsed into a natural language form via the module `fun_3000/ingestion/ingest_ontologies.py`. This script pulls the source ontology and the instance ontologies into a single graph and parses out sentences based on the human labels of entities that are joined by the `rdf:type` relationship ([w3c](https://www.w3.org/TR/rdf-schema/#ch_type)). This script makes the assumption that a valid English human language equivalent for the `rdf:type` relationship is the verb "is". For example, the OWL snippet:

```
<owl:NamedIndividual rdf:about="http://purl.obolibrary.org/obo/OBI_0000759"><!-- Illumina -->
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/OBI_0000245"/><!-- organization -->
        <rdf:type>
            <owl:Restriction>
                <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/RO_0000087"/><!-- has role -->
                <owl:someValuesFrom rdf:resource="http://purl.obolibrary.org/obo/OBI_0000571"/><!-- manufacturer role -->
            </owl:Restriction>
        </rdf:type>
        <rdfs:label rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Illumina</rdfs:label>
        <obo:IAO_0000111 rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Illumina</obo:IAO_0000111>
        <obo:IAO_0000117 rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Philippe Rocca-Serra</obo:IAO_0000117>
        <obo:IAO_0000114 rdf:resource="http://purl.obolibrary.org/obo/IAO_0000123"/><!-- metadata incomplete -->
    </owl:NamedIndividual>
```

would convert to the sentence "Illumina is organization".

To run the ontology ingestion in a script, use the `ingest_and_wrangle_owls` module with the following syntax:

```
import ingestion

ontology_grab = ingestion.ingest_ontologies
ontology_grab.ingest_and_wrangle_owls(directory)
```

You can also run the ontology ingestion module directly as a script; see usage notes in the script itself.

### To generate data-folds

You can generate a folder structure that will contain prepared training and test sets for k number of folds.

The folder structure follows the following pattern UNDER the data directory
```
.
+-- {SOME_RUN}
|   +--corpus_filename_1.txt
|   +--corpus_filename_2.txt
|   +--1
|   +--|   +--train
|   +--|   +--|   +--train.txt
|   +--|   +--test
|   +--|   +--|   +--test.txt
|   +--2
|   +--|   +--train
|   +--|   +--|   +--train.txt
|   +--|   +--test
|   +--|   +--|   +--test.txt
```
The script also expects ontology generated files to exist in a SISTER (to data) 'ontology' folder like the example below
```
+-- {SOME_RUN}
|   +--ontology_filename_1.txt
|   +--ontology_filename_2.txt
```

In the example above only 2 folds were generated.

To generate the proper files and folder structure do the following:

```
python fun_3000/wrangling/generate_folds.py -d '{SOME_RUN}' -k 3 -o True -s 10
```
where: 

* k is the number of folds you want to generate

* o if we are including an ontology in this run this should be true.

* d is the data folder

* s is the random seed

#### Cleaning text

There are several functions called during the generate folds process before and after the sentences are tokenized to remove HTML and Latex code, formatting, headers, and other potentially bothersome elements from the text.

Full list of stuff that is removed:

* Remove all html tags {<-->)
* Remove all latex ({--} and ${--})
* Remove headers from wikipedia articles
* Remove new lines and carriage returns (this messes up the tokenize script)
* Remove all non-ascii characters (like copyright symbols)
* Remove extraneous spaces (this also messes up the tokenize script)
* Remove sentences less than 10 words long (or some length defined in parameter), that don't end with a period, don't start with a capital letter, or start with a number


### To create a model:

```
python fun_3000/word2vec.py -i data_dir
```

The script will use all data files within data/*data_dir*/ and build a Word2Vec model from them.  In the example above 
the data_dir might be = '<data_dir>/1/train'

The model will be saved under models/*data_dir*/ for future use.

You can specify additional options, such as the number of parallel execution threads, the size of the hidden layer and the output model name. For script usage information, run:

```
python fun_3000/word2vec.py -h
```
*Note*: if no model name is specified, output name will be <data_dir>_1_train.model (using the example above).

# Example using Wikipedia data

Let's say you wanted to train a Word2Vec model with the "Jazz" wikipedia page as your corpus:

### Step 1: Retrieve wikipedia page content

```
python fun_3000/ingestion/wikipedia_ingest.py -s '{SOME_RUN}'
```

Confirm that the text content was downloaded and stored under data/{SOME_RUN}/model_data.txt

(Alternatively: you can manually create a directory under data/ and placing all corpus files within it)

### Step 2: Create a Word2Vec model

```
python fun_3000/word2vec.py -i {SOME_RUN}
```
Confirm that the model was created and saved under models/{SOME_RUN}/{SOME_RUN}.model

### Step 3: Explore the model

Within a python REPL:

```python
>>> import gensim
>>> model = gensim.models.Word2Vec.load('models/{SOME_RUN}/{SOME_RUN}.model')
>>> model.most_similar('jazz')
    [('sound', 0.9113765358924866), ('well', 0.9058974981307983), ('had', 0.9046300649642944), ('bass', 0.9037381410598755), ('In', 0.9003950953483582), ('blues', 0.9001777768135071), ('on', 0.8995728492736816), ('at', 0.8993135690689087), ('rather', 0.8992522954940796), ('such', 0.8990519046783447)]
```

### Evaluation
Evaluation returns a single score for all fols for an individual run.  It is the average of scores across the folds.  Our
scores are stored in scores.csv in the base directory.  Every time you run th workflow this csv will be appended to.  There
is a column that provides the run name in the csv and the data and time.

```
python fun_3000/evaluation/similarity_evaluation.py -r 'run_1' -f 3 -o scores.csv
```
where:

-r is the name of the run
-f is the number of folds, defaults to 3
-o is the output file, defaults to scores.csv
