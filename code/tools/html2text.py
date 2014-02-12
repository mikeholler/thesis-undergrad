import BeautifulSoup

__author__ = 'mjholler'

from sys import argv
import os


def html2text(html):
    soup = BeautifulSoup.BeautifulSoup(html)

    # Remove all in-text citations.
    for reference in soup.findAll('sup', {'class': 'reference'}):
        reference.decompose()

    # Remove all template link references.
    for link in soup.findAll('a', {'class': 'new'}):
        try:
            if link['title'].startswith('Template:'):
                link.decompose()
        except IndexError:
            pass

    # Gather paragraphs.
    paragraphs = list()
    for paragraph in soup.findAll('p'):
        paragraphs.append(''.join(paragraph.findAll(text=True)).encode('utf8'))

    return '\n'.join(paragraphs)


def main():
    if len(argv) < 3:
        print 'Need to specify a source directory (containing html wiki files)'
        print 'and a destination directory.'
    sourceDir = argv[1]
    destDir = argv[2]

    os.mkdir(destDir)

    for sourceFilename in os.listdir(sourceDir):
        if os.path.isfile(os.path.join(sourceDir, sourceFilename)):
            outputFilename = '{}{}'.format(sourceFilename[:-5], '.txt')

            print '{} --> {}'.format(sourceFilename, outputFilename)

            with open(os.path.join(sourceDir, sourceFilename), 'r') as _input:
                text = html2text(_input.read())

            with open(os.path.join(destDir, outputFilename), 'w') as output:
                output.write(text)


if __name__ == "__main__":
    main()



