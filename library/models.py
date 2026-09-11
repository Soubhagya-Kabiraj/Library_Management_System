from django.db import models
from datetime import date

class Author(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    birth_date=models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_book(self):
        return Book.objects.filter(author=self)
    
class Publisher(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state_province=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    website=models.URLField()

    def __str__(self):
        return self.name
    
    def formated_adress(self):
        return f"{self.address} {self.city} {self.country} {self.state_province}"
    
class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    publication_date=models.DateField()
    isbn=models.CharField(max_length=15)
    publisher=models.ManyToManyField(Publisher)

    def __str__(self):
        return self.title
    
    def book_age(self):
        today=date.today()
        return today.year-self.publication_date.year