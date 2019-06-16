#!/usr/bin/python3
import string
import os
import sys
import getopt

from os import path
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from decimal import Decimal

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


def createTokenizedFile(input, output, stem=False, sentiment=False):
    inputFilename = path.join(dir, "input", input)
    outputFilename = path.join(dir, "output", output)
    sentimentFilename = path.join(dir, "sentiment", output + ".csv")

    inputFile = open(inputFilename, "r")
    text = inputFile.read()
    inputFile.close()

    # ANALISIS DE SENTIMIENTOS DE CADA ORACION
    # Ver explicación del algoritmo VADER utilizado por NLTK
    # https://github.com/cjhutto/vaderSentiment
    if(sentiment):
        sentences = sent_tokenize(text)
        sentimentAnalizer = SentimentIntensityAnalyzer()

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
                    sentence,
                ))

    # PROCESAMIENTO DE LAS PALABRAS
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
    ouput = ''
    stem = False
    sentiment = False
    try:
        opts, args = getopt.getopt(argv, "hi:o:r:s", [
            "input=",
            "output=",
            "stem",
            "sentiment"
        ])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)
    if len(opts) < 1:
        print('test.py -i <inputfile>')
    else:
        for opt, arg in opts:
            if opt == '-h':
                print('test.py -i <input> -o <output> --root --sentiment')
                sys.exit()
            elif opt in ("-i", "--input"):
                input = arg.strip()
            elif opt in ("-o", "--output"):
                ouput = arg.strip()
            elif opt in ('-r', '--root'):
                stem = True
            elif opt in ('-s', '--sentiment'):
                sentiment = True

        tokenizedFilename = createTokenizedFile(
            input,
            ouput,
            stem,
            sentiment
        )
        return tokenizedFilename


if __name__ == "__main__":
    main(sys.argv[1:])
