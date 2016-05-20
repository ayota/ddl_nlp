import re
import optparse


def clean_corpus(corpus):
    '''
    cleans out all non-ascii characters, newlines, carriage returns, wikipedia headers, other fun stuff
    :param corpus: a bytestream from a text file representing the corpus
    :type corpus: bytearray, str or mixed strings and bytes
    :return: cleaned corpus string
    :rtype: str
    '''
    corpus = corpus.decode(encoding='ascii', errors='ignore')  # force drop all non-ascii characters like copyright symbols
    corpus = re.sub(r'<.*?>', ' ', corpus)  # html tags
    corpus = re.sub(r'{.*?}', ' ', corpus)  # anything between brackets, from latex in medical abstracts
    corpus = re.sub(r'${.*?}', ' ', corpus)  # any line leading content between brackets, from latex in medical abstracts
    corpus = re.sub(r'={2,}.*?={2,}', ' ', corpus)  # wikipedia headers e.g. ===asdfkjlas===
    corpus = re.sub(r'%', ' percent ', corpus) # convert % symbol to its English word percent
    corpus = re.sub(r'\\x[a-zA-Z0-9]{2,}', ' ', corpus)  # escaped bytes in the decoded information
    corpus = re.sub(r'(\b([A-Za-z0-9]){1,1} ){2,}', ' ', corpus)  # copyright statements written like this: 2 0 1 6 E l s e i v e r L t d .
    corpus = re.sub(r'\s+', ' ', corpus)  # condense extra whitespace, tabs, newlines, other whitespace characters
    corpus = corpus.strip()
    return corpus


def bad_sentence(sentence, sent_len):
    '''
    Runs a series of tests to remove suspect sentences. Check for length and capitalization.
    :param sentence: sentence to check
    :type sentence: str
    :param sent_len: min number of words required to be considered a sentence
    :type sent_len: int
    :return True or False: True means sentence is bad
    :rtype: bool
    '''
    words = len(sentence.split())
    if words < sent_len:
        return True
    elif sentence[0].islower():
        return True
    elif sentence[0].isdigit():
        return True
    return False


def validate_sentences(clean_sentences=None, sent_len=10):
    '''
    Iterates through list of cleaned sentences in corpus and removes those that start with lowercase letters or numbers, and that are less than a certain length.
    :param clean_sentences: a list of strings of clean sentences
    :type clean_sentences: list[str]
    :param sent_len: the minimum length for a sentence
    :type sent_len: int
    :return: list of strings of valid sentences that met our thresholds in this function
    :rtype: list[str]
    '''
    valid_sentences = []
    for index,text in enumerate(clean_sentences):
        if bad_sentence(text, sent_len) == False:
            valid_sentences.append(text)
    return valid_sentences


def tokenize_sentences(corpus=None):
    '''
    split the corpus into sentences.
    :param corpus: a string from a text file representing the corpus
    :type corpus: str
    :return: list of strings, each sentence separated in the list
    :rtype: list[str]
    '''
    return re.split('(?<!\w\.\w\.)' # if not preceeded by an acronym like A.C.A.
                    '(?<![A-Z][A-Za-z]\.)' # and if not preceeded by an abbreviation like Ca. or CA.
                    '((?<=\.|\?|\!)' # then if directly preceeded by valid punctuation ., ? or !
                    '|(?<=\.\)))' # or the valid punctuation .)
                    '\s' # and the cursor is at a space
                    # then split on this space as a new sentence.
                    # this will also include the space in the split result; see https://docs.python.org/2/library/re.html#re.split
                    ,corpus)


if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', dest='input_file', default=None, help='Specify source data file')
    parser.add_option('-o', '--output_file', dest='output_file', default="output.txt", help="Specify output data file.")
    parser.add_option('-s', '--min_sentence_length', dest='sentence_length', default=10, help="Specify minimum sentence word length.")
    (opts, args) = parser.parse_args()

    with open(opts.input_file, "rb") as f:
        corpus = f.read()

    cleaned_corpus = clean_corpus(corpus)
    tokenized_corpus = tokenize_sentences(cleaned_corpus)
    cleaned_sentences = validate_sentences(tokenized_corpus, opts.sentence_length)

    with open(opts.output_file, "wb") as f:
        blob = ' '.join(cleaned_sentences)
        f.write(blob)