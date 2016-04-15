# ddl_nlp
Repo for DDL research lab project.

The general workflow for an individual experiment goes through these steps.

1. Ingestion: We ingest corpuses (form various sources, potentially ontologies into a defined folder structure.
2. Generate_Folds: A script is run that generates/splits the data up into several 'folds' and both a test and train file
is developed under each fold.  The folder structure fully supports this as described below.
3. Gensim word2vec is run and a model result is generated for each fold.
4. We then take the resulting model file and the human medical coder results and combine them into a single dataset
where we run a random forest regressor on them for each fold. This results in an overall score (R^2) for an experiment
across all folds.

# Usage

### To get data from wikipedia (optional):


```
python fun_3000/ingestion/wikipedia_ingest.py -s search_term
```

Optionally, you can specify a directory name where the data will be stored (by default, the script will use your search term as a directory name):

```
python fun_3000/ingestion/wikipedia_ingest.py -s search_term -d data_dir
```

### To generate data-folds

You can generate a folder structure that will contain prepared training and test sets for k number of folds. Below we do
3 folds (-k), we include a build that builds in an ontology into the corpus (-o), and we set the random seed to 10 (-s).
Keep in mind that usually at this point in the pipeline Drake is running the remainder of the steps including this one.
So usually you won't be calling this script manually.
```
python fun_3000/wrangling/generate_folds.py -d experiment_name -k 3 -o True -s 10
```

The folder structure follows the following pattern UNDER the 'data' directory.  Where the experiment_name is a human/user
determined name for the entire experiment.
```
.
+-- experiment_name
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
+-- experiment_name
|   +--ontology_filename_1.txt
|   +--ontology_filename_2.txt
```

In the example above only 2 folds were generated.

To generate the proper files and folder structure do the following:

```
python fun_3000/wrangling/generate_folds.py -d 'jazz' -k 3 -o True -s 10
```
where: 

* k is the number of folds you want to generate

* o if we are including an ontology in this run this should be true.

* d is the data folder

* s is the random seed

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
python fun_3000/ingestion/wikipedia_ingest.py -s 'jazz'
```

Confirm that the text content was downloaded and stored under data/jazz/model_data.txt

(Alternatively: you can manually create a directory under data/ and placing all corpus files within it)

### Step 2: Create a Word2Vec model

```
python fun_3000/word2vec.py -i jazz
```
Confirm that the model was created and saved under models/jazz/jazz.model

### Step 3: Explore the model

Within a python REPL:

```python
>>> import gensim
>>> model = gensim.models.Word2Vec.load('models/jazz/jazz.model')
>>> model.most_similar('jazz')
    [('sound', 0.9113765358924866), ('well', 0.9058974981307983), ('had', 0.9046300649642944), ('bass', 0.9037381410598755), ('In', 0.9003950953483582), ('blues', 0.9001777768135071), ('on', 0.8995728492736816), ('at', 0.8993135690689087), ('rather', 0.8992522954940796), ('such', 0.8990519046783447)]
```

#Workflow
We maintain both a master and a develop branch.  All features are to be built as a branch off of develop and pull requests (pr) will be made into develop.  Only major releases will be pulled into the master branch.

# Running a pipeline with Drake

Requirement: Make sure Drake is installed. See [here](https://github.com/Factual/drake) for installation instructions.

### Step 1: Configuration

Place a blank file named workflow.start in whichever data directory you want to use for the pipeline run. (IMPORTANT: if you end up changing your corpus file(s), you'll need to remove the workflow.start file and recreate it)

Open the file named Drakefile and change any of the configuration settings at the top of the file. They correspond to the same options that the word2vec.py script supports.

### Step 2: Execution

All you need to do is run the following from the main directory:

```
drake -w Drakefile
```

Review the steps and enter 'y' to accept them.

### Post-Execution

Drake will create a workflow/ directory to store some progress files and track step completion. If you wish to re-start the pipeline from a particular step, delete the corresponding .complete file from the workflow/ directory.
