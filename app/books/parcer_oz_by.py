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

from books.models import BooksModel, BookSales, AuthorModel


def parse_ozby():
    # books_url = 'https://oz.by/books/'
    books_url = 'https://oz.by/books/bestsellers?page=2'

    html_page = requests.get(books_url).text
    soup = BeautifulSoup(html_page, 'html.parser')
    print('title:', soup.title.text)

    item_title = soup.find_all('p', attrs={'class': 'item-type-card__title'})
    author_all = soup.find_all('p', attrs={'class': 'item-type-card__info'})
    # print(len(item_title), len(author_all))

    for title, author in zip(item_title, author_all):
        book_isbn = str(random.randint(10 ** 10, 12 ** 10))
        author_parse = author.text.split(',')
        authors = [a.strip() for a in author_parse[:-1]]
        print(title.text, authors, book_isbn)

        book = BooksModel(title=title.text, isbn=book_isbn)
        book.save()

        for i in range(3):  # random 3 book sale
            sold_today = random.randint(0, 100)
            month = random.randint(1, 2)
            if month == 1:
                day = random.randint(1, 31)
            else:
                day = random.randint(1, 28)
            day_of_sale = date(2020, month, day)

            book_sale = BookSales(book=book, sales=sold_today, sold_day=day_of_sale)
            book_sale.save()

        for _author in authors:
            if _author:
                try:
                    book_author = AuthorModel.objects.get(author_name=_author)
                    book.book_author.add(book_author)
                except:
                    book_author = AuthorModel(author_name=_author)
                    book_author.save()
                    book.book_author.add(book_author)


if __name__ == "__main__":
    parse_ozby()
