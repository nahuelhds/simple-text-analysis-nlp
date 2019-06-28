#!/usr/bin/python3
import os
import sys
import getopt
import nltk

from os import path
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()


def wordCount(inputfilename, rank=False):
    # Read the whole text.
    text = open(path.join(dir, inputfilename)).read().split(' ')
    words = nltk.FreqDist(text)

    if(rank == False):
        words = sorted(words.items())
    else:
        words = words.most_common()

    basename = path.basename(path.splitext(inputfilename)[0])
    if(rank is True):
        filename = "count-rank.txt"
    else:
        filename = "count.txt"
    outputfilename = path.join(dir, "output", basename, filename)

    outputfolder = os.path.dirname(outputfilename)
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)

    outputfile = open(path.join(dir, outputfilename), "w+")

    outputfile.write("WORD,COUNT\n")
    with outputfile as outputfile:
        for word, count in words:
            outputfile.write("%s,%d\n" % (word, count))


def printCmd():
    print('count.py -i <inputfile> --rank')


def main(argv):
    input = ''
    rank = False
    try:
        opts, args = getopt.getopt(argv, "hi:r", [
            "input=",
            "rank"
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
            elif opt in ('-r', '--rank'):
                rank = True

        wordCount(input, rank)


if __name__ == "__main__":
    main(sys.argv[1:])
