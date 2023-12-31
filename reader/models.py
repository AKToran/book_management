from django.db import models
from django.contrib.auth.models import User
from book.models import Book

class ReaderAccount(models.Model):
    reader = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return f"{self.reader}'s account"

class Transaction(models.Model):
    account = models.ForeignKey(ReaderAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)

class ReaderHistory(models.Model):
    books = models.ManyToManyField(Book)
    reader = models.ForeignKey(User, related_name='history', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)

