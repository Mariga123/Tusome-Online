from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView
from django.utils import timezone
from .models import Book, Author, Identifier, ImageLinks, LANG_CHOICES
from .forms import (BookForm, AuthorForm,
                    IdentifierForm, ImageForm)
from django.conf import settings
from operator import itemgetter
import requests
import json
# Create your views here.


class BookListView(ListView):
    model = Book
    template_name = 'books/index.html'
    context_object_name = 'books'
    extra_context = {'languages': LANG_CHOICES}
    paginate_by = 9


class SearchDateView(BookListView):
    def get_queryset(self):
        date_one = self.request.GET.get('date_one')
        date_two = self.request.GET.get('date_two')
        date_one = int(date_one) if date_one else 0
        date_two = int(date_two) if date_two else timezone.now().year
        return Book.objects.filter(publishedDate__range=[date_one, date_two])


class SearchTitleView(BookListView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(title__icontains=query)


class SearchLanguageView(BookListView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(language=query)


class SearchAuthorView(BookListView):
    model = Author

    def get_queryset(self):
        query = self.request.GET.get('q')
        authors = Author.objects.filter(name__icontains=query)
        if authors:
            books = authors[0].books.all()
            for author in authors[1:]:
                books = books.union(author.books.all())
            return books
        else:
            return []


def book_form_view(request):

    if request.method == 'POST':

        book_form = BookForm(data=request.POST)
        image_form = ImageForm(data=request.POST)
        author_form = AuthorForm(data=request.POST)
        isbn_10_form = IdentifierForm(data=request.POST)

        if (book_form.is_valid() and author_form.is_valid() and
            isbn_10_form.is_valid() and image_form.is_valid()):

            book = Book.objects.create(
                            title=book_form.cleaned_data['title'],
                            publishedDate=book_form.cleaned_data['publishedDate'],
                            pageCount=book_form.cleaned_data['pageCount'],
                            language=book_form.cleaned_data['language'],
                            imageLinks=image_form.save()
                            )

            book.authors.add(author_form.save())
            id10 = Identifier.objects.create(type='ISBN_10',
                                             identifier=isbn_10_form.cleaned_data['identifier'])
            book.industryIdentifiers.add(id10)
            id13 = Identifier.objects.create(type='ISBN_13',
                                             identifier=book_form.cleaned_data['isbn_13'])
            book.industryIdentifiers.add(id13)
            book.save()

    else:
        book_form = BookForm()
        image_form = ImageForm()
        author_form = AuthorForm()
        isbn_10_form = IdentifierForm()
    return render(request, 'books/book_form.html', {'book_form': book_form,
                                                    'image_form': image_form,
                                                    'author_form': author_form,
                                                    'isbn_10_form': isbn_10_form,
                                                    'languages': LANG_CHOICES})


def search_google_view(request):

    key = getattr(settings, 'GOOGLE_API_KEY', None)
    url = getattr(settings, 'GOOGLE_API_URL', None)

    query = request.GET['Keyword'] if request.method == 'GET' else request.POST['Keyword']

    params = {"q": query, 'key': key}
    r = requests.get(url=url, params=params)
    jsn = r.json()
    books = jsn['items']
    books_info = [book['volumeInfo'] for book in books]

    if request.method == 'POST':
        boxes = [int(num) for num in request.POST.getlist('boxes')]
        if boxes:
            if len(boxes) > 1:
                books_to_save = [book['volumeInfo'] for book in itemgetter(*boxes)(books)]
            else:
                books_to_save = [books[boxes[0]]['volumeInfo']]
            for book in books_to_save:

                authors = book.get('authors')
                identifiers = book.get('industryIdentifiers')
                images = book.get('imageLinks')
                if images:
                    images_obj = ImageLinks.objects.create(
                        smallThumbnail=images.get('smallThumbnail'),
                        thumbnail=images.get('thumbnail'))
                else:
                    images_obj = ImageLinks.objects.create(
                        smallThumbnail='',
                        thumbnail='')

                book = Book.objects.create(
                    title=book.get('title'),
                    publishedDate=book.get('publishedDate'),
                    pageCount=int(book.get('pageCount', 1)),
                    language=book.get('language'),
                    imageLinks=images_obj )

                for author in authors:
                    a = Author.objects.create(name=author)
                    book.authors.add(a)
                for element in identifiers:
                    type_data = element.get('type')
                    identify_data = element.get('identifier')
                    identifier_obj = Identifier.objects.create(
                        type=type_data,
                        identifier=identify_data)
                    book.industryIdentifiers.add(identifier_obj)

                book.save()
            return redirect('books:books_list')
        else:
            return HttpResponse('No books selected')
    else:
        return render(request, 'books/results.html', {'results': books_info, 'query': query})



