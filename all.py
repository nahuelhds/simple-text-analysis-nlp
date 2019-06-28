

import sys
import getopt

from os import path
from parse import createTokenizedFile
from count import wordCount
from summary import textSummarization
from cloud import makeWordCloud
from sentiment import analyzeSentiment

def printCmd():
    print("all.py -i <inputfile> -m <maskfile> -r|--root")

def main(argv):
    input = None
    mask = None
    root = False
    try:
        opts, args = getopt.getopt(argv, "hi:m:r", [
            "input=",
            "mask=",
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
            elif opt in ("-m", "--mask"):
                mask = arg.strip()
            elif opt in ('-r', '--root'):
                root = True

        basename = path.basename(path.splitext(input)[0])

        if(mask is None):
            maskCloud = path.join(path.dirname(input), basename + ".png")
        else:
            maskCloud = mask

        files = []
        
        # Sentiment
        analyzeSentiment(
            input,
        )

        # Tokenization para generacion de conteos y nubes
        tokenizedFile = createTokenizedFile(
            input,
            False
        )

        files.append(tokenizedFile)

        if(root == True):
            # Root
            tokenizedRootFile = createTokenizedFile(
                input,
                True
            )
            files.append(tokenizedRootFile)

        for file in files:

            # Conteo
            wordCount(file, False)

            # Conteo ordenado de mayor a menor
            wordCount(file, True)

            # Nube
            makeWordCloud(file)

            if path.exists(maskCloud):
                # Nube con mascara
                makeWordCloud(file, maskCloud)

        # Sumarizacion
        textSummarization(input)


if __name__ == "__main__":
    main(sys.argv[1:])
