from django.db import models


# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=150, null=False)
    isbn = models.CharField(max_length=20, null=False)
    country = models.CharField(max_length=100, null=False)
    number_of_pages = models.IntegerField(null=False)
    publisher = models.IntegerField(null=False)
    release_date = models.DateTimeField(null=False)


class Author(models.Model):
    name = models.CharField(max_length=150)
    book = models.CharField(Book)
