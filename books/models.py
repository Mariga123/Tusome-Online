from django.db import models
from django.conf.locale import LANG_INFO
from .validators import validate_numeric, validate_date


LANG_CHOICES = [(key, value.get('name')) for key, value in LANG_INFO.items() if value.get('name')]


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Identifier(models.Model):
    CHOICES = (('ISBN_13', 'ISBN 13'), ('ISBN_10', 'ISBN 10'))
    type = models.CharField(max_length=7, choices=CHOICES)
    identifier = models.CharField(max_length=60, validators=[validate_numeric])

    class Meta:
        unique_together = ['type', 'identifier']

    def __str__(self):
        return '{}: {}'.format(self.type, self.identifier)


class ImageLinks(models.Model):
    smallThumbnail = models.URLField(blank=True, default='')
    thumbnail = models.URLField(blank=True, default='')


class Book(models.Model):
    CHOICES = LANG_CHOICES
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author,
                                     related_name='books',
                                     blank=True,
                                     default='Not avaiable')
    publishedDate = models.CharField(max_length=10,
                                     help_text='Enter date in format: "YYYY-MM-DD"',
                                     validators=[validate_date])
    industryIdentifiers = models.ManyToManyField(Identifier, related_name='book')
    pageCount = models.PositiveIntegerField()
    imageLinks = models.OneToOneField(ImageLinks, on_delete=models.CASCADE, blank=True)
    language = models.CharField(max_length=7, choices=CHOICES, null=True)

    def __str__(self):
        all_authors = ",".join([a.name for a in self.authors.all()])
        return '"{}" by {}'.format(self.title, all_authors)

    class Meta:
        ordering = ['-publishedDate', 'title']
