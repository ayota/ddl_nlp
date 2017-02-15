import re
import optparse
import utils
from os import path
import io

def clean_line(line):
    '''
    cleans out all newlines, carriage returns, wikipedia headers, other fun stuff
    :param line: a string from a text file representing the line
    :type line: str
    :return: cleaned line string
    :rtype: str
    '''
    #line = line.decode(encoding='ascii', errors='ignore')  # force drop all non-ascii characters like copyright symbols
    line = re.sub(r'<.*?>', ' ', line)  # html tags
    line = re.sub(r'{.*?}', ' ', line)  # anything between brackets, from latex in medical abstracts
    line = re.sub(r'${.*?}', ' ', line)  # any line leading content between brackets, from latex in medical abstracts
    line = re.sub(r'={2,}.*?={2,}', ' ', line)  # wikipedia headers e.g. ===asdfkjlas===
    line = re.sub(r'%', ' percent ', line) # convert % symbol to its English word percent
    line = re.sub(r'\\x[a-zA-Z0-9]{2,}', ' ', line)  # escaped bytes in the decoded information
    line = re.sub(r'(\b([A-Za-z0-9]){1,1} ){2,}', ' ', line)  # copyright statements written like this: 2 0 1 6 E l s e i v e r L t d .
    line = re.sub(r'\s+', ' ', line)  # condense extra whitespace, tabs, newlines, other whitespace characters
    line = line.strip()
    return line


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

    usage = "usage: %prog [options] run_directory"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-o', '--output_file', dest='output_file', default="output.txt", help="Specify output data file.")
    parser.add_option('-s', '--min_sentence_length', dest='sentence_length', default=10, help="Specify minimum sentence word length.")
    (opts, args) = parser.parse_args()


    # specify the output file
    output_file = path.join(utils.PARENT_DIR, 'data', args[0], opts.output_file)
    # TODO: pulls entire directory of corpus data into a single string
    # probably want to stream this instead l8r
    corpus = utils.read_source(path.join(utils.PARENT_DIR, 'data', opts.run_directory))

    with io.open(output_file, "wb") as f:

        for line in corpus:
            cleaned_line = clean_line(line)
            tokenized_line = tokenize_sentences(cleaned_line)
            validated_line = validate_sentences(tokenized_line, opts.sentence_length)
            f.write(validated_line)

