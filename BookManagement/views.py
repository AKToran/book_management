from django.shortcuts import render
from book.models import Book, Category

def home(request, category_slug = None):
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        print(category)
        books = Book.objects.filter(category=category)
    else:
        books = Book.objects.all()
    
    categories = Category.objects.all()
    return render(request, 'home.html', {'books': books, 'categories': categories})