from django.conf import settings
from django.db import models


class NumberSystem(models.Model):
    name = models.CharField(max_length=20, primary_key=True, blank=False)
    locale = models.CharField(max_length=5, default=settings.LANGUAGE_CODE)


class NumberSystemConversion(models.Model):
    system = models.ForeignKey(NumberSystem, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, db_index=True)
    synonyms = models.TextField(max_length=500, default='[]')
    value = models.BigIntegerField(default=0)

    @staticmethod
    def deserialize_synonyms(synonyms_field):
        return synonyms_field[1:-1].split(',')

    @staticmethod
    def serialize_synonyms(synonyms):
        return '[' + ','.join(synonyms) + ']'
