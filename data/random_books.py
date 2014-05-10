import requests
from bs4 import BeautifulSoup
from time import sleep

with open('books.tsv', 'w') as f:
    r = requests.get('http://www.bookbookgoose.com/v1/get_books?n=100&rand=0.15975621389225125')
    #soup = BeautifulSoup(r.text)
    #title, author = soup.find(id='book_title').text, soup.find(id='book_author').text
    for book in r.json():
        author, title = book[0].encode('utf8'), book[1].encode('utf8')
        print title, author
        if author and title:
            f.write('{0}\t{1}\n'.format(title, author))