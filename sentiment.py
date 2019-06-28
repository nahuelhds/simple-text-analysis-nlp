#!/usr/local/bin/python3
import string
import os
import sys
import getopt

from decimal import Decimal
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
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


def analyzeSentiment(input):
    inputFilename = path.join(dir, input)
    basename = path.basename(path.splitext(input)[0])
    sentimentFilename = path.join(dir, "output", basename, "sentiment.csv")

    inputFile = open(inputFilename, "r")
    text = inputFile.read()
    inputFile.close()

    # ANALISIS DE SENTIMIENTOS DE CADA ORACION
    # Ver explicación del algoritmo VADER utilizado por NLTK
    # https://github.com/cjhutto/vaderSentiment
    sentences = sent_tokenize(text)
    sentimentAnalizer = SentimentIntensityAnalyzer()

    # Creo la carpeta si no existe
    outputFolder = os.path.dirname(sentimentFilename)
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    # Genero el archivo
    sentimentFile = open(sentimentFilename, "w+")

    sentimentFile.write(
        "TYPE,COMPOUND,POSITIVE,NEGATIVE,NEUTRAL,SENTENCE\n")
    with sentimentFile as sentimentFile:
        for sentence in sentences:
            score = sentimentAnalizer.polarity_scores(sentence)
            sentimentFile.write("%d,%f,%f,%f,%f,\"%s\"\n" % (
                calculateCompoundRank(score['compound']),
                score['compound'],
                score['pos'],
                score['neg'],
                score['neu'],
                " ".join(sentence.split("\n")),
            ))


def printCmd():
    print('sentiment.py -i <inputfile>')


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

        analyzeSentiment(input)


if __name__ == "__main__":
    main(sys.argv[1:])
