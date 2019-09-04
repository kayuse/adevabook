from django.db import models


# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=150, null=False)
    isbn = models.CharField(max_length=20, null=False)
    country = models.CharField(max_length=100, null=False)
    number_of_pages = models.IntegerField(null=False)
    publisher = models.CharField(max_length=200, null=False)
    release_date = models.DateField(null=False)


class Author(models.Model):
    name = models.CharField(max_length=150)
    book = models.ForeignKey(Book, related_name="authors", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
