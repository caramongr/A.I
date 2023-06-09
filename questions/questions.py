import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dict = {}

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), encoding="utf-8") as ofile:
            dict[file] = ofile.read()

    return dict

    #raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    words = nltk.word_tokenize(document.lower())

    stopwords = set(nltk.corpus.stopwords.words('english'))
    punctuation = set(string.punctuation)
    removed = set()

    n = len(words)

    for i in range(0, n):
        word = words[i]

        if word in stopwords or word in punctuation:
            removed.add(word)

    return [word for word in words if word not in removed]
    #raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs_values = dict()

    for document in documents.keys():
        for word in documents[document]:
            if word in idfs_values.keys():
                idfs_values[word] += 1
            else:
                idfs_values[word] = 1

    len_documents = len(documents.keys())
    for word in idfs_values.keys():
        frequency = idfs_values[word]
        idf = math.log(len_documents/frequency)
        idfs_values[word] = idf

    return idfs_values
    #raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    tf_idfs = []

    for file in files:
        tf_idf = 0
        for q in query:
            if q in files[file]:
                tf_idf += idfs[q] * files[file].count(q)
        if tf_idf == 0:
            continue
        tf_idfs.append((file, tf_idf))

    tf_idfs.sort(key=lambda x: x[1])

    return [x[0] for x in tf_idfs[:n]]
    #raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_idfs = []
    for sentence in sentences:
        idf = 0
        matches = 0
        for q in query:
            if q in sentences[sentence]:
                idf += idfs[q]
                matches += 1

        query_density = float(matches)/len(sentences[sentence])

        sentences_idfs.append((sentence, idf, query_density))

    sentences_idfs.sort(key=lambda x: (x[1], x[2]), reverse=True)

    return [x[0] for x in sentences_idfs[:n]]

    #raise NotImplementedError


if __name__ == "__main__":
    main()
