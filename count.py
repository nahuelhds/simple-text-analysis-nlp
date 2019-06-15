#!/usr/bin/python3
import os
import sys
import getopt
import nltk

from os import path
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()


def wordCount(inputfile, outputfile, rank=0):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    text = open(path.join(d, "output", inputfile)).read().split(' ')
    words = nltk.FreqDist(text)

    if(rank == 0):
        words = words.items()
    else:
        words = words.most_common(rank)

    with open(path.join(d, "wordcount", outputfile), "w+") as output:
        for word, count in words:
            output.write("%s (%d)\n" % (word, count))


def main(argv):
    input = ''
    output = ''
    rank = 0
    try:
        opts, args = getopt.getopt(argv, "hi:o:r:", [
            "input=",
            "output=",
            "rank="
        ])
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
            elif opt in ("-o", "--output"):
                output = arg.strip()
            elif opt in ('-r', '--rank'):
                rank = int(arg.strip())

        print(wordCount(input, output, rank))


if __name__ == "__main__":
    main(sys.argv[1:])
