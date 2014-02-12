import os
from sys import argv
import requests
import BeautifulSoup

__author__ = 'mjholler'

"""
Print page links from "All Pages" wiki page.

python printPageLinks.py output/ "http://localhost/thesisWiki/index.php?title=Special:AllPages&from=3%27_UTR&to=Hormone" \
"http://localhost/thesisWiki/index.php?title=Special:AllPages&from=Hormones&to=Sympatric_speciation" \
"http://localhost/thesisWiki/index.php?title=Special:AllPages&from=Synapsid&to=Xylem"
"""


SLASH_REPLACEMENT = '(SLASH)'


def main():

    titleToUrl = dict()

    outputDir = argv[1]

    os.mkdir(argv[1])

    for url in argv[2:]:

        r = requests.get(url)

        page = BeautifulSoup.BeautifulSoup(r.text)
        table = page.find('table', attrs={'class': 'mw-allpages-table-chunk'})

        for node in table.findAll('a'):

            try:
                if node['class'] == 'mw-redirect':
                    print 'Ignored:', node['title']
                    continue
            except KeyError:
                pass

            titleToUrl[node['title']] = 'http://localhost{}'.format(node['href'])

    for title in titleToUrl:

        r = requests.get(titleToUrl[title])

        if r.ok:

            filepath = os.path.join(outputDir, title.replace(' ', '_').replace('/', SLASH_REPLACEMENT) + '.html').encode('utf8')

            with open(filepath, 'w') as outputFile:

                try:
                    outputFile.write(r.text.encode('utf8'))
                except UnicodeEncodeError:
                    print 'Error encoding text:', title.encode('utf8')
                    continue

            print 'Visited:', title.encode('utf8')

        else:
            print 'Request failed ({}):'.format(r.status_code), title

    print 'Done.'

if __name__ == '__main__':
    main()
