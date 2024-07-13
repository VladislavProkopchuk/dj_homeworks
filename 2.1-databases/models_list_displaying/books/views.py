from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from itertools import groupby

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, template, context)


def show_books(request, pub_date):
    template = 'books/books_date_list.html'
    # groups = Book.objects\
    #     .values('pub_date')\
    #     .annotate(dcount=Count('pub_date'))\
    #     .order_by()
    books = Book.objects.order_by('pub_date')
    books_grouped = {}
    for key, group_items in groupby(books, key=lambda x: x.pub_date):
        key = key.strftime('%Y-%m-%d')
        books_grouped[key] = []
        for item in group_items:
            books_grouped[key].append(item)
    books = tuple(books_grouped.values())
    dates = tuple(books_grouped.keys())
    paginator = Paginator(books, 1)
    page_num = dates.index(pub_date) + 1
    page = paginator.page(page_num)
    next_page = None
    prev_page = None
    if page.has_next():
        next_page = dates[page.next_page_number()-1]
    if page.has_previous():
        prev_page = dates[page.previous_page_number()-1]
    context = {
        'books': page.object_list[0],
        'dates': dates,
        'page': page,
        'next_page': next_page,
        'prev_page': prev_page,
    }
    return render(request, template, context)
