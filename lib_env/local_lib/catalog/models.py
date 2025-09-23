from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.conf import settings
from datetime import date
from django.db import transaction
import uuid;

class Genre(models.Model):
    name = models.CharField(max_length=200,help_text="Enter the genre")

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("genre_detail", args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive',
                violation_error_message="Genre already exists."
            )
        ]
class Language(models.Model):
    name = models.CharField('Language',max_length=100,unique=True,null=True)

    class Meta:
        constraints=[
            UniqueConstraint(
                Lower('name'),
                name='insensitive_unique_language',
                violation_error_message="Language already exists."
            )
        ]
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    language = models.ForeignKey(Language,on_delete=models.RESTRICT,null=True)
    summary = models.CharField(max_length=1000,help_text='Enter the book summary')
    isbn = models.CharField('ISBN',max_length=13,unique=True,help_text="Write the ISBN")
    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book.')

    def __str__(self):
        return self.title
    def get_info_data(self):
        output = {"ISBN":self.isbn,"Title":self.title,"Author":self.author,"Language":self.language,"Genre":self.display_genre(),"Book Summary":self.summary}
        return output.items()
    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this book instance")
    book = models.ForeignKey(Book,on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)
    LOAN_STATUS = (('m','Maintance'),('o','On Loan'),('a','Available'),('r','Reserved'),)
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
        ordering = ['due_back']
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
    
    @transaction.atomic
    def borrow(self,user,due_date):
        locked = BookInstance.objects.select_for_update().get(pk=self.pk)
        if locked.status != 'a':
            raise ValueError("This copy is no longer available.")
        locked.status = 'o'
        locked.borrower = user
        locked.due_back = due_date
        locked.save()
        return locked
    
    
class Author(models.Model):
    fname = models.CharField('Firstname',max_length=100)
    lname = models.CharField('Lastname',max_length=100)
    dob = models.DateField('Date of birth',null=True,blank=True)
    def __str__(self):
        return f'{self.fname} {self.lname}'
    def get_info_data(self):
        listOfBooks = Book.objects.filter(author=self)
        output = {'Firstname':self.fname,'Lastname':self.lname,'Date of birth':self.dob,'collection':{'List of Books':listOfBooks}.items()}
        return output.items()
    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.id)])
    class Meta:
        ordering = ['lname','fname']
    
class Page(models.Model):
    VISIBILITY = [
        ('a',"Always"),
        ('anon','Anonymous users only'),
        ('auth','Authenticated users only'),
        ('staff','Staff only')
    ]
    label = models.CharField("Menu label",max_length=200)
    url = models.CharField("URL",max_length=200,null=True)
    is_published = models.BooleanField(default=False)
    nav_order = models.PositiveSmallIntegerField(default=0)
    visibility = models.CharField(max_length=10,choices=VISIBILITY,default='a')

    class Meta:
        ordering = ["nav_order"]

    def __str__(self):
        return self.label
    
    