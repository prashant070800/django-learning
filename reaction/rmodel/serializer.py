from rest_framework import serializers
from .models import Reaction

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'unicode_character']



# from rest_framework import serializers
# from django.core.exceptions import ValidationError
# from .models import Reaction
# import unicodedata

# def validate_unicode(value):
#     """
#     Validate if the given value is a valid Unicode character.
#     """
#     try:
#         if value.startswith("\\U") or value.startswith("\\u"):
#             value = value.encode().decode('unicode_escape')
#         unicodedata.name(value)  # Validate the Unicode character
#     except (ValueError, UnicodeDecodeError):
#         raise ValidationError(f"{value} is not a valid Unicode character.")
#     return value

# class ReactionSerializer(serializers.ModelSerializer):
#     unicode_character = serializers.CharField(
#         max_length=10, 
#         validators=[validate_unicode]
#     )

#     class Meta:
#         model = Reaction
#         fields = ['id', 'unicode_character']

