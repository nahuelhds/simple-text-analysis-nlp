

import sys
import getopt

from os import path
from parse import createTokenizedFile
from count import wordCount
from summary import textSummarization
from cloud import makeWordCloud
from sentiment import analyzeSentiment

def printCmd():
    print("all.py -i <inputfile> -m <maskfile>")

def main(argv):
    input = None
    mask = None
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
                input = arg.strip()
            elif opt in ("-m", "--mask"):
                mask = arg.strip()

        basename = path.basename(path.splitext(input)[0])

        if(mask is None):
            maskCloud = path.join(path.dirname(input), basename + ".png")
        else:
            maskCloud = mask

        # Tokenization
        tokenizedFile = createTokenizedFile(
            input,
            False
        )

        # Root
        tokenizedRootFile = createTokenizedFile(
            input,
            True
        )
        # Sentiment
        analyzeSentiment(
            input,
        )

        files = [tokenizedFile, tokenizedRootFile]

        for file in files:

            # Count
            wordCount(file, False)

            # Count ranked
            wordCount(file, True)

            # Cloud without mask
            makeWordCloud(file)

            if path.exists(maskCloud):
                # Cloud with mask
                makeWordCloud(file, maskCloud)

        # Text summarization
        textSummarization(input)


if __name__ == "__main__":
    main(sys.argv[1:])
