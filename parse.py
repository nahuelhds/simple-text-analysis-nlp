#!/usr/bin/python3
import string
import os
import sys
import getopt

from decimal import Decimal
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from os import path

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()


def calculateCompoundRank(compound):
    decimalCompound = Decimal(compound)
    if(decimalCompound.compare(Decimal(0.75)) == 1):
        return 4
    elif(decimalCompound.compare(Decimal(0.5)) == 1):
        return 3
    elif(decimalCompound.compare(Decimal(0.25)) == 1):
        return 2
    elif(decimalCompound.compare(Decimal(0)) == 1):
        return 1
    elif(decimalCompound.compare(Decimal(0)) == 0):
        return 0
    elif(decimalCompound.compare(Decimal(-0.25)) == 1):
        return -1
    elif(decimalCompound.compare(Decimal(-0.5)) == 1):
        return -2
    elif(decimalCompound.compare(Decimal(-0.75)) == 1):
        return -3
    return -4


def createTokenizedFile(input, root=False):
    inputFilename = path.join(dir, input)
    basename = path.basename(path.splitext(input)[0])

    if(root == True):
        filename = basename + "-root.txt"
    else :
        filename = basename + ".txt"

    outputFilename = path.join(dir, "output", filename)

    inputFile = open(inputFilename, "r")
    text = inputFile.read()
    inputFile.close()

    # PROCESAMIENTO DE LAS PALABRAS
    # Ver: https://machinelearningmastery.com/clean-text-machine-learning-python/

    # 1. Separo en palabras (tokenizar) y las paso a minusculas
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]

    # 2. Reduccion de palabras a su raíz lingüística
    if(root):
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

def printCmd():
    print('parse.py -i <input> --root')

def main(argv):
    input = ''
    root = False
    try:
        opts, args = getopt.getopt(argv, "hi:r", [
            "input=",
            "root",
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
            elif opt in ('-r', '--root'):
                root = True

        tokenizedFilename = createTokenizedFile(
            input,
            root,
        )
        return tokenizedFilename


if __name__ == "__main__":
    main(sys.argv[1:])
