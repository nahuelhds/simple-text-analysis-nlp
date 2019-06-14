#!/usr/bin/python3
import os
import sys
import getopt

from os import path
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

def createTokenizedFile(input):
    inputFilename = path.join(dir, "text", input)
    tokenizedFilename = path.join(dir, "tokenized", input)
    data = open(inputFilename, "r").read()
    stopWords = set(stopwords.words('spanish'))
    words = word_tokenize(data)
    wordsFiltered = []

    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)

    tokenizedText = " ".join(str(x) for x in wordsFiltered)
    tokenizedFile = open(tokenizedFilename, "w+")
    tokenizedFile.write(tokenizedText)
    return tokenizedFilename


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

        tokenizedFilename = createTokenizedFile(input)
        return tokenizedFilename

if __name__ == "__main__":
    main(sys.argv[1:])
