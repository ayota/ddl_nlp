# ddl_nlp
Repo for DDL research lab project.

# Usage:

### To get data from wikipedia (optional):

From fun_3000/ do:

```
python ingestion/wikipedia_ingest.py -s search_term
```

Optionally, you can specifiy a directory name where the data will be stored (by default, the script will use your search term as a directory name):

```
python ingestion/wikipedia_ingest.py -s search_term -d data_dir
```

### To create a model:

From fun_3000/ do:

```
python word2vec_starter.py -c data_dir
```

The script will all files within data/*data_dir*/ and build a Word2Vec model from them.
The model will be saved under models/*data_dir*/ for future use.

#Workflow
We maintain both a master and a develop branch.  All features are to be built as a branch off of develop and pull requests (pr) will be made into develop.  Only major releases will be pulled into the master branch.
