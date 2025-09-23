from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction

def Index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    num_visits = request.session.get("num_visits",0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_available':num_available,
        'num_authors':num_authors,
        'num_visits':num_visits
    }

    return render(request,'index.html',context)

class BookInstancesView(generic.ListView):
    model = BookInstance
    queryset = BookInstance.objects.all()
    context_object_name = "book_instances"
    template_name = "book_instances_list.html"

class BookView(generic.ListView):
    model = Book
    queryset = Book.objects.all()
    context_object_name = "book_list"
    template_name = "book_list.html"

    def get_context_data(self, **kwargs):
        context = super(BookView,self).get_context_data(**kwargs)
        if(self.kwargs):
            context['modalTitle'] = "Book Details"
            context['modalBody'] = Book.objects.filter(id=self.kwargs['pk']).first()
        return context  
    
class AuthorView(LoginRequiredMixin,generic.ListView):
    model = Author
    queryset = Author.objects.all()
    context_object_name = "author_list"
    template_name = "author_list.html"
    def get_context_data(self, **kwargs):
        context = super(AuthorView,self).get_context_data(**kwargs)
        if(self.kwargs):
            context['modalTitle'] = "Author Details"
            context['modalBody'] = Author.objects.filter(id=self.kwargs['pk']).first()
        return context

def Logout(request):
    logout(request)
    return redirect("/")

class BookInstanceAddView(generic.CreateView):
    model = BookInstance
    form_class = BookInstanceForm
    template_name = "books/bookinstance_form.html"
    success_url = reverse_lazy("bookinstance")

    def form_valid(self, form):
        messages.success(self.request,"Book copy added successfully.")
        return super().form_valid(form)

def RegisterView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            newUser = User.objects.create_user(form.cleaned_data['uname'],form.cleaned_data['email'],form.cleaned_data['password'])
            newUser.first_name = form.cleaned_data['fname']
            newUser.last_name = form.cleaned_data['lname']
            newUser.save()
            return redirect("/")
    context = {
        'form':form
    }
    return render(request,'register.html',context)

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
class StaffBorrowedView(LoginRequiredMixin, StaffRequiredMixin, generic.FormView):
    template_name = "borrow_book.html"
    form_class = StaffBorrowedForm
    # success_url = reverse_lazy("borrow_success")

    def form_valid(self, form):
        borrower = form.cleaned_data['borrower']
        copy = form.cleaned_data['copy']
        due_back = form.cleaned_data['due_back']

        with transaction.atomic():
            locked = BookInstance.objects.select_for_update().get(pk=copy.pk)
            if locked.status != 'a':
                form.add_error("Copy","That copy was taken a moment ago. Pick another one")
                return self.form_invalid(form) 
            
            locked.status = 'o'
            locked.borrower = borrower
            locked.due_back = due_back
            locked.save()

        return super().form_valid(form)
    