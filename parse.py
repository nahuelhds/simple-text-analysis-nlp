#!/usr/bin/python3
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import string
import os
import sys
import getopt

from os import path
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()


def createTokenizedFile(input, output, stem=False):
    inputFilename = path.join(dir, "input", input)
    outputFilename = path.join(dir, "output", output)

    inputFile = open(inputFilename, "r")
    text = inputFile.read()
    inputFile.close()

    # PROCESAMIENTO DEL TEXTO
    # Ver: https://machinelearningmastery.com/clean-text-machine-learning-python/

    # 1. Separo en palabras (tokenizar) y las paso a minusculas
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]

    # 2. Reduccion de palabras a su raíz lingüística
    if(stem):
        porter = PorterStemmer()
        tokens = [porter.stem(word) for word in tokens]

    # 3. Remuevo puntuaciones y todo lo no alfanumérico
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]

    # 4. Filtro las stopwords en español
    stop_words = set(stopwords.words('spanish'))
    words = [w for w in words if not w in stop_words]

    # GUARDADO DEL ARCHIVO FINAL
    outputText = " ".join(str(x) for x in words)
    outputFile = open(outputFilename, "w+")
    outputFile.write(outputText)
    return outputFilename


def main(argv):
    input = ''
    outputfile = ''
    stem = False
    try:
        opts, args = getopt.getopt(argv, "hi:o:s", [
            "input=",
            "output=",
            "stem"
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
                outputfile = arg.strip()
            elif opt in ('-s', '--stem'):
                stem = True

        tokenizedFilename = createTokenizedFile(input, outputfile, stem)
        return tokenizedFilename


if __name__ == "__main__":
    main(sys.argv[1:])
