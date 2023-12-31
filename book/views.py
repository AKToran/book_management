from django.shortcuts import redirect
from django.views.generic import DetailView
from .models import Book
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from reader.models import ReaderHistory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class BookDetailView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'book/details.html'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.name = self.request.user.username
            review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews = book.reviews.all()
        review_form = ReviewForm()
        reader = self.request.user
        # print(reader)
        book = Book.objects.get(id=book.id)
        # for r in book.reader.all():
        #     print(r)
        if reader in book.reader.all():
            context['review_form'] = review_form
        context['reviews'] = reviews
        
        
        return context

@login_required
def borrow_book(request, id):
    book = Book.objects.get(id=id)
    reader = request.user
    balance = reader.account.balance
    if balance > book.price:
        history = ReaderHistory.objects.create(reader=reader)
        history.books.set([book])
        history.save()  

        reader.account.balance = balance - book.price
        reader.account.save(update_fields=['balance']) 

        book.reader.set([reader])
        book.save()
        
        message = render_to_string('book/borrow_mail.html', {
            'user': reader,
            'book': book.title
        })
        subject = "Book Borrowed"
        send_mail = EmailMultiAlternatives(subject, '', to=[reader.email])
        send_mail.attach_alternative(message, "text/html")
        send_mail.send()
    else: 
        return redirect('deposit')
    
    return redirect('profile')
