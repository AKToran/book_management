from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reader/', include('reader.urls')),
    path('book/', include('book.urls')),
    path('', views.home, name='home'),
    path('category/<slug:category_slug>/', views.home, name='sort_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)