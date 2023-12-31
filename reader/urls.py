from django.urls import path
from . import views

urlpatterns = [
    path('create-account/', views.ReaderAccountView.as_view(), name='create-account'),
    path('login/', views.ReaderLoginView.as_view(), name='login'),
    path('logout/', views.ReaderLogoutView.as_view(), name='logout'),
    path('profile/', views.reader_profile, name='profile'),
    path('deposit/', views.ReaderTransactionView.as_view(), name='deposit'),
    path('return/<int:b_id>/<int:h_id>/', views.return_book, name='return'),
    
]
 