from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.db import models
import uuid

class Genre(models.Model):
    """Models represeting a book genre"""
    name = models.CharField(max_length=200, unique=True,help_text="Enter a book genre (e.g Science Fiction )")
    def __str__(self):
        """String for representing the Model object"""
        return self.name
    def get_absolute_url(self):
        return reverse("genre_detail", args=[str(self.id)])
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message= "Genre already exist"
            ),
        ]
    
class Language(models.Model):
    name =  models.CharField(max_length=200)
    def __str__(self):
        return self.name
    class Meta:
        constraints=[
            UniqueConstraint(
                Lower('name'),
                name='insensitive_unique_language',
                violation_error_message="Language already exists"
            )
        ]

    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    summary = models.CharField(max_length=1000, help_text='Enter the book summary')
    isbn = models.CharField("ISBN", max_length=13, unique=True, help_text="Write the ISBN")
    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book')

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())
        
        
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this book instance")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (('m','Maintance'),('o','On Loan'),('a','Available'),('r','Reserved'),)
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'

    )
    class Meta:
        ordering = ['due_back']
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    fname = models.CharField('Firstname', max_length=100)
    lname = models.CharField('Lastname', max_length=100)

    dob = models.DateField('Date of birth', null=True, blank=True)
    def __str__(self):
        return f'{self.fname} {self.lname}'
    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.id)])
    class Meta:
        ordering = ['lname', 'fname']
    
    