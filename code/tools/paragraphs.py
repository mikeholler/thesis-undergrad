import BeautifulSoup

with open('detroit.html', 'r+') as f:
	html = f.read()

def getParagraphs(html):
    soup = BeautifulSoup.BeautifulSoup(html)

    for reference in soup.findAll('sup', {'class': 'reference'}):
        reference.decompose()

    for paragraph in soup.findAll('p'):
	    print
	    print ''.join(paragraph.findAll(text=True)).encode('utf8')

getParagraphs(html)



