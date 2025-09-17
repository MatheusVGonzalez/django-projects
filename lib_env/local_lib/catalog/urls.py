from django.urls import path
from .views import *

urlpatterns = [
    path('',Index,name='index'),
    path('books/',BookView.as_view(),name='books'),
    path('books/<int:pk>',BookView.as_view(),name='book_detail')
]
