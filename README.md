# ddl_nlp
Repo for DDL research lab project.

# Usage:

### To get data from wikipedia (optional):


```
python fun_3000/ingestion/wikipedia_ingest.py -s search_term
```

Optionally, you can specifiy a directory name where the data will be stored (by default, the script will use your search term as a directory name):

```
python fun_3000/ingestion/wikipedia_ingest.py -s search_term -d data_dir
```

### To create a model:


```
python fun_3000/word2vec_starter.py -c data_dir
```

The script will store all data files within data/*data_dir*/ and build a Word2Vec model from them.
The model will be saved under models/*data_dir*/ for future use.

## Example using Wikipedia data:

Let's say you wanted to train a Word2Vec model with the "Jazz" wikipedia page as your corpus:

# Step 1: Retrieve wikipedia page content

```
python fun_3000/ingestion/wikipedia_ingest.py -s 'jazz'
```

Confirm that the text content was downloaded and stored under data/jazz/model_data.txt

# Step 2: Create a Word2Vec model

```
python fun_3000/word2vec_starter.py -c jazz
```
Confirm that the model was created and saved under models/jazz/jazz.model

# Step 3: Explore the model

Within a python REPL:

```python
>>> import gensim
>>> model = gensim.models.Word2Vec.load('models/jazz/jazz.model')
>>> model.most_similar('jazz')
    [('sound', 0.9113765358924866), ('well', 0.9058974981307983), ('had', 0.9046300649642944), ('bass', 0.9037381410598755), ('In', 0.9003950953483582), ('blues', 0.9001777768135071), ('on', 0.8995728492736816), ('at', 0.8993135690689087), ('rather', 0.8992522954940796), ('such', 0.8990519046783447)]
```

#Workflow
We maintain both a master and a develop branch.  All features are to be built as a branch off of develop and pull requests (pr) will be made into develop.  Only major releases will be pulled into the master branch.
