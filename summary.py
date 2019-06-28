# Source: https://nlpforhackers.io/textrank-text-summarization/

import os
import numpy as np
import sys
import getopt

from nltk.cluster.util import cosine_distance
from nltk.corpus import brown, stopwords
from nltk.tokenize import sent_tokenize
from operator import itemgetter
from os import path

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stopwords=None):
    # Create an empty similarity matrix
    S = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue

            S[idx1][idx2] = sentence_similarity(
                sentences[idx1], sentences[idx2], stopwords)

    # normalize the matrix row-wise
    for idx in range(len(S)):
        S[idx] /= S[idx].sum()

    return S


def pagerank(A, eps=0.0001, d=0.85):
    P = np.ones(len(A)) / len(A)
    while True:
        new_P = np.ones(len(A)) * (1 - d) / len(A) + d * A.T.dot(P)
        delta = abs(new_P - P).sum()
        if delta <= eps:
            return new_P
        P = new_P


def textrank(sentences, top_n=5, stopwords=None):
    S = build_similarity_matrix(sentences, stopwords)
    sentence_ranks = pagerank(S)

    # Sort the sentence ranks
    ranked_sentence_indexes = [item[0] for item in sorted(
        enumerate(sentence_ranks), key=lambda item: -item[1])]
    selected_sentences = sorted(ranked_sentence_indexes[:top_n])
    summary = itemgetter(*selected_sentences)(sentences)
    return summary


def textSummarization(input):
    inputFilename = path.join(dir, input)
    basename = path.basename(path.splitext(input)[0])
    outputFilename = path.join(dir, "output", basename, "summary.txt")

    inputFile = open(inputFilename, "r")
    text = inputFile.read()
    inputFile.close()

    sentences = sent_tokenize(text)

    # Creo la carpeta si no existe
    outputFolder = os.path.dirname(outputFilename)
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    # Genero el archivo
    outputFile = open(outputFilename, "w+")

    with outputFile as outputFile:
        for idx, sentence in enumerate(textrank(sentences, top_n=3, stopwords=stopwords.words('spanish'))):
            outputFile.write("%s. %s\n" % ((idx + 1), sentence))


def printCmd():
    print('sentiment.py -i <input>')


def main(argv):
    input = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", [
            "input=",
        ])
    except getopt.GetoptError:
        printCmd()
        sys.exit(2)
    if len(opts) < 1:
        printCmd()
        sys.exit()
    else:
        for opt, arg in opts:
            if opt == '-h':
                printCmd()
                sys.exit()
            elif opt in ("-i", "--input"):
                input = arg.strip()

        return textSummarization(input)


if __name__ == "__main__":
    main(sys.argv[1:])
