from django.urls import path
from .views import *

urlpatterns = [
    path('',Index,name='index'),
    path('books/',BookView.as_view(),name='books'),
    path('books/<int:pk>',BookView.as_view(),name='book_detail'),
    path('authors/',AuthorView.as_view(),name='authors'),
    path('authors/<int:pk>',AuthorView.as_view(),name='author_detail'),
    path('logout/',Logout,name='logout'),
    path('bookinstances/add/',BookInstanceAddView.as_view(),name='bookinstance-add'),
    path('bookinstances/',BookInstancesView.as_view(),name='bookinstance'),
    path('register/',RegisterView,name='register'),
    path('borrow/new/',StaffBorrowedView.as_view(),name="borrow_book")
]
