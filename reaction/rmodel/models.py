from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
import unicodedata

def validate_unicode(value):
    try:
        # Attempt to decode the string into a Unicode character if it's in the \UXXXXXXXX format
        if value.startswith("\\U") or value.startswith("\\u"):
            value = value.encode().decode('unicode_escape')
        # Validate the Unicode character
        unicodedata.name(value)
    except (ValueError, UnicodeDecodeError):
        raise ValidationError(f"{value} is not a valid Unicode character.")

class Reaction(models.Model):
    unicode_character = models.CharField(max_length=10, validators=[validate_unicode], unique=True)

    def __str__(self):
        return self.unicode_character
