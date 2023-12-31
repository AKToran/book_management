from typing import Any
from .models import ReaderAccount, Transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class ReaderAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            ReaderAccount.objects.create(reader = user)
        return user

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        min_amount = 500

        if amount < min_amount:
            raise forms.ValidationError(f"Minimum deposit amount is {min_amount}$")
        return amount
    
