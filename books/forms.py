from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Author, Book, Identifier, ImageLinks
from .validators import validate_numeric


class BookForm(forms.ModelForm):
    isbn_13 = forms.CharField(max_length=60, validators=[validate_numeric], required=True, label='ISBN 13')

    class Meta:
        model = Book
        exclude = ['authors', 'industryIdentifiers', 'imageLinks']
        widgets = {'publishedData': AdminDateWidget()}


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        labels = {'name': 'Author'}


class IdentifierForm(forms.ModelForm):
    class Meta:
        model = Identifier
        fields = ['identifier']
        labels = {'identifier': 'ISBN 10'}


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageLinks
        fields = '__all__'
        labels = {'smallThumbnail': 'Small thumbnail',
                  'thumbnail:': 'Thumbnail'}
