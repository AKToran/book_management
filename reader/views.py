from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ReaderAccount, ReaderHistory, Transaction
from book.models import Book
from .forms import ReaderAccountForm, TransactionForm
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404

class ReaderAccountView(FormView):
    form_class = ReaderAccountForm
    success_url = reverse_lazy('profile')
    template_name = 'reader/create_account.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context

class ReaderLoginView(LoginView):
    template_name = 'reader/create_account.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

class ReaderLogoutView(LoginRequiredMixin, LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')

@login_required
def reader_profile(request):
    reader = request.user
    history = ReaderHistory.objects.filter(reader=reader)
    return render(request, 'reader/profile.html', {'history': history, 'reader': reader})

class ReaderTransactionView(LoginRequiredMixin, FormView):
    template_name = 'reader/transaction.html'
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=['balance']
        )
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.amount = amount  
        transaction.save()

        user = self.request.user
        message = render_to_string('reader/deposit_mail.html', {
            'user': user,
            'amount': amount
        })
        subject = "Money Deposit"
        send_mail = EmailMultiAlternatives(subject, '', to=[user.email])
        send_mail.attach_alternative(message, "text/html")
        send_mail.send()
        return super().form_valid(form)

def return_book(request, b_id, h_id):
    book = Book.objects.get(id=b_id)
    request.user.account.balance += book.price
    request.user.account.save()

    history = get_object_or_404(ReaderHistory, id=h_id)
    history.returned = True
    history.save()
    return redirect('profile')



