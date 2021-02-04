from django.urls import path, include
from rest_framework import routers
from .apiviews import BooksView
from .views import (BookListView, book_form_view,
                    SearchDateView, SearchTitleView,
                    SearchAuthorView, SearchLanguageView,
                    search_google_view)

app_name = 'books'

router = routers.DefaultRouter()
router.register('books', BooksView, basename='boo')

urlpatterns = [
    path('', BookListView.as_view(), name='books_list'),
    path('add/', book_form_view, name='add_book'),
    path('search/date/', SearchDateView.as_view(), name='search_date'),
    path('search/title/', SearchTitleView.as_view(), name='search_title'),
    path('search/authors/', SearchAuthorView.as_view(), name='search_author'),
    path('search/language/', SearchLanguageView.as_view(), name='search_language'),
    path('search/googleapi/', search_google_view, name='googleapi'),
    path('api/', include((router.urls, 'api'), namespace='api'), name='api')
]

#urlpatterns += router.urls

