from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

# Create your views here.
def index(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_tolkien_books = Book.objects.filter(author__last_name__contains ='tolkien').count()
    num_genres = Genre.objects.count()

    
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
        		'num_instances':num_instances,
        		'num_instances_available':num_instances_available,
        		'num_authors':num_authors,
        		'num_tolkien_books':num_tolkien_books,
        		'num_genres':num_genres},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author