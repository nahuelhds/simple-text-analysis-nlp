#!/usr/bin/env python
import os
import sys
import getopt
import numpy as np
import matplotlib.pyplot as plt

from os import path
from PIL import Image
from nltk.corpus import stopwords
from wordcloud import WordCloud


def makeWordCloud(inputfile, maskfile, outputfile):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    text = open(path.join(d, "output", inputfile)).read()

    # read the mask image
    # taken from
    # http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
    image_mask = np.array(Image.open(path.join(d, "mask", maskfile)))

    stopWords = set(stopwords.words('spanish'))

    wc = WordCloud(background_color="white", max_words=2000, mask=image_mask,
                   stopwords=stopWords, contour_width=3, contour_color='steelblue')

    # generate word cloud
    wc.generate(text)

    # store to file
    wc.to_file(path.join(d, "wordcloud", outputfile))


def printHelp():
    print('test.py -i <inputfile> -m <maskfile> -o <outputfile>')


def main(argv):
    inputfile = ''
    maskfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:m:o:", [
            "inputfile=",
            "maskfile=",
            "output=file"
        ])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

    if len(opts) < 1:
        printHelp()
        sys.exit()
    else:
        for opt, arg in opts:
            if opt == '-h':
                printHelp()
                sys.exit()
            elif opt in ("-i", "--inputfile"):
                inputfile = arg.strip()
            elif opt in ("-m", "--maskfile"):
                maskfile = arg.strip()
            elif opt in ("-o", "--outputfile"):
                outputfile = arg.strip()

        return makeWordCloud(inputfile, maskfile, outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
