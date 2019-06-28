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

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()


def makeWordCloud(inputfile, maskfile=None):
    # Read the whole text.
    text = open(path.join(dir, inputfile)).read()

    # read the mask image
    # taken from
    # http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
    image_mask = None
    width = 800
    height = 800
    if(maskfile is not None):
        image_mask = np.array(Image.open(path.join(dir, maskfile)))

    stopWords = set(stopwords.words('spanish'))

    wc = WordCloud(
        background_color="white",
        max_words=2000,
        mask=image_mask,
        stopwords=stopWords,
        contour_width=3,
        contour_color='steelblue',
        width=width,
        height=height
    )

    # generate word cloud
    wc.generate(text)

    # store to file
    basename = path.basename(path.splitext(inputfile)[0])
    
    if(maskfile is None):
        filename = "cloud.png"
    else :
        filename = "cloud-mask.png"
    
    outputFilename = path.join(dir, "output", basename, filename)
    outputFolder = os.path.dirname(outputFilename)
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    wc.to_file(outputFilename)


def printCmd():
    print('cloud.py -i <input> -m <mask>')


def main(argv):
    inputfile = ''
    maskfile = None
    try:
        opts, args = getopt.getopt(argv, "hi:m:", [
            "input=",
            "mask=",
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
                inputfile = arg.strip()
            elif opt in ("-m", "--mask"):
                maskfile = arg.strip()

        return makeWordCloud(inputfile, maskfile)


if __name__ == "__main__":
    main(sys.argv[1:])
