from django.db import models
from .constants import RATING_CHOICES
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40, unique=True)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=36)
    description = models.TextField()
    image = models.ImageField(upload_to='book/', blank=True, null=True)
    category = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    reader = models.ManyToManyField(User, blank=True, related_name='books')

    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    body = models.TextField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name}"