from django.contrib import admin
from .models import ReaderAccount, ReaderHistory, Transaction

admin.site.register(ReaderAccount)
admin.site.register(ReaderHistory)
admin.site.register(Transaction)
