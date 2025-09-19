from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .forms import *
from django.contrib import messages
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
    
class AuthorView(LoginRequiredMixin,generic.ListView):
    model = Author
    queryset = Author.objects.all()
    context_object_name = "author_list"
    template_name = "templates/author_list.html"

    def get_context_data(self, **kwargs):
        context = super(AuthorView,self).get_context_data(**kwargs)
        if(self.kwargs):
            context['selectedAuthor'] = Author.objects.filter(id=self.kwargs['pk']).first()
        return context  
    
def author_list(request):
    authors = Author.objects.all()
    selected_author_id = request.GET.get('author_id')
    selected_author = None
    books = []
    if selected_author_id:
        selected_author = Author.objects.get(id=selected_author_id)
        books = Book.objects.filter(author=selected_author)
    return render(request, 'catalog/author_list.html', {
        'author_list': authors,
        'selectedAuthor': selected_author,
        'books': books,
        'newVariable': 'List of Authors'
    })

def Logout(request):
    logout(request)
    return redirect("/")


class BookInstanceView(generic.CreateView):
    model = BookInstance
    form_class = BookInstanceForm
    template_name = "books/bookinstance_form.html"
    success_url = reverse_lazy("books")

    def form_valid(self, form):
        messages.success(self.request, "Book copy added.")
        return super().form_valid(form)
