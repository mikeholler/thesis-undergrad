from sys import argv
import xml.sax
import MySQLdb


class WikiDumpRedirectContentHandler(xml.sax.ContentHandler):

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

        self.mapping = dict()
        self.fromPage = None
        self.toPage = None
        self.inTitle = False

    def startElement(self, name, attrs):
        if name == 'page':
            self.fromPage = None
            self.toPage = None
            self.inTitle = False

        elif name == 'title':
            self.inTitle = True

        elif name == 'redirect':
            self.toPage = attrs.getValue('title')

    def characters(self, content):
        if self.inTitle:
            self.fromPage = content

    def endElement(self, name):
        if name == 'page':
            self.mapping[self.fromPage.replace(' ', '_')] = None if self.toPage is None else self.toPage.replace(' ', '_')

        elif name == 'title':
            self.inTitle = False


def main():

    sax = WikiDumpRedirectContentHandler()

    try:
        with open(argv[1], 'r+') as source:
            xml.sax.parse(source, sax)

        redirectTargets = {k: sax.mapping[k] for k in sax.mapping if sax.mapping[k] is not None}

        db = MySQLdb.connect(host='localhost', user='thesis', passwd='thesis', db='thesis')

        for origin in redirectTargets:
            cursor = db.cursor()

            try:

                cursor.execute(
                    """UPDATE indexToWiki SET wikiTitle = %s WHERE indexTitle = %s""",
                    (redirectTargets[origin].encode('UTF-8'), origin.replace('_', ' ').encode('UTF-8'))
                )
                db.commit()

            except:
                db.rollback()

            # cursor = db.cursor()
            # cursor.execute(
            # )


        # for t in redirectTargets:
        #     print t.encode('UTF-8')

    except IndexError:
        print 'Need to provide a filename argument.'


if __name__ == '__main__':
    main()
