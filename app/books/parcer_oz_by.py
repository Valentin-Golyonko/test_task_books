import os
import random
import sys
from datetime import date

import django
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from books.models import BooksModel, BooksSalesModel


def parse_ozby():
    books_url = 'https://oz.by/books/bestsellers?page=2'

    html_page = requests.get(books_url).text
    soup = BeautifulSoup(html_page, 'html.parser')
    print('title:', soup.title.text)

    item_title = soup.find_all('p', attrs={'class': 'item-type-card__title'})
    author_all = soup.find_all('p', attrs={'class': 'item-type-card__info'})
    # print(len(item_title), len(author_all))

    for title, author in zip(item_title, author_all):
        sold_today = random.randint(0, 100)
        month = random.randint(1, 2)
        if month == 1:
            day = random.randint(1, 31)
        else:
            day = random.randint(1, 28)
        day_of_sale = date(2020, month, day)
        book_isbn = str(random.randint(10 ** 10, 12 ** 10))

        author_parse = author.text.split(',')
        authors = [a.strip() for a in author_parse[:-1]]

        print(title.text, authors, sold_today, day_of_sale, book_isbn)

        for _author in authors:
            book = BooksModel(
                title=title.text,
                author=_author,
                isbn=book_isbn
            )
            book.save()

            book_sale = BooksSalesModel(
                book=book,
                sales=sold_today,
                sold_day=day_of_sale,
            )
            book_sale.save()


def test_parse():
    book = BooksModel(title="НИ СЫ. Будь уверен в своих силах и не позволяй сомнениям мешать тебе двигаться вперед",
                      author="Джен Синсеро, 2018",
                      sales=30,
                      sold_day=date(2020, 1, 12),
                      isbn='111111111111111')
    book.save()


if __name__ == "__main__":
    parse_ozby()
    # test_parse()
