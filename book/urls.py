from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:id>', views.BookDetailView.as_view(), name='book_detail'),
    path('borrow/<int:id>', views.borrow_book, name='borrow'),
    
]