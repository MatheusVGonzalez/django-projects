from django.shortcuts import render
from django.views import generic
from .models import *

def Index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_available':num_available,
        'num_authors':num_authors,
    }

    return render(request,'index.html',context)

class BookView(generic.ListView):
    model = Book
    queryset = Book.objects.all()
    context_object_name = "book_list"
    template_name = "templates/book_list.html"

    def get_context_data(self, **kwargs):
        context = super(BookView,self).get_context_data(**kwargs)
        if(self.kwargs):
            context['selectedBook'] = Book.objects.filter(id=self.kwargs['pk']).first()
        return context  