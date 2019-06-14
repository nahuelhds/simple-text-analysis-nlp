#!/usr/bin/python3
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import sys
import getopt


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["input=", "output="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    if len(opts) < 2:
        print('test.py -i <inputfile> -o <outputfile>')
    else:
        for opt, arg in opts:
            if opt == '-h':
                print('test.py -i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--input"):
                input = arg
            elif opt in ("-o", "--output"):
                output = arg

        generateWordCloud(input, output)


if __name__ == "__main__":
    main(sys.argv[1:])


def generateWordCloud(input, output):
