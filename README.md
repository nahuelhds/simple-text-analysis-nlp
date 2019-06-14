# word_cloud

## Command-line usage

The `wordcloud_cli` tool can be used to generate word clouds directly from the command-line:

    $ wordcloud_cli --text mytext.txt --imagefile wordcloud.png

If you're dealing with PDF files, then `pdftotext`, included by default with many Linux distribution, comes in handy:

    $ pdftotext mydocument.pdf - | wordcloud_cli --imagefile wordcloud.png

In the previous example, the `-` argument orders `pdftotext` to write the resulting text to stdout, which is then piped to the stdin of `wordcloud_cli.py`.

Use `wordcloud_cli --help` so see all available options.
