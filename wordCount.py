#!/usr/bin/python3
import os
import sys
import getopt
import nltk

from os import path
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()


def wordCount(inputfile):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    text = open(path.join(d, "tokenized", inputfile)).read().split(' ')
    commonWords = nltk.FreqDist(text).items()
    with open(path.join(d, "rank", inputfile), "w+") as rankFile:
        for word, count in commonWords:
            rankFile.write("%s (%d)\n" % (word, count))


def main(argv):
    input = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["input="])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)
    if len(opts) < 1:
        print('test.py -i <inputfile>')
    else:
        for opt, arg in opts:
            if opt == '-h':
                print('test.py -i <inputfile>')
                sys.exit()
            elif opt in ("-i", "--input"):
                input = arg.strip()

        print(wordCount(input))


if __name__ == "__main__":
    main(sys.argv[1:])
