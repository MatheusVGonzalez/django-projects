from django.urls import path
from .views import *

urlpatterns = [
    path('',Index,name='index'),
    path('books/',BookView.as_view(),name='books'),
    path('books/<int:pk>',BookView.as_view(),name='book_detail'),
    path('authors/',author_list ,name='authors'), 
    path('authors/<int:pk>',AuthorView.as_view(),name='author_detail')
]
