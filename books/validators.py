from django.core.exceptions import ValidationError
import re


def validate_numeric(value):
    if not value.isnumeric():
        raise ValidationError('Numbers only')


def validate_date(value):
    pass