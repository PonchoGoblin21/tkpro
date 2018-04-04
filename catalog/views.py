from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.d
def index(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_tolkien_books = Book.objects.filter(author__last_name__contains ='tolkien').count()
    num_genres = Genre.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
        		'num_instances':num_instances,
        		'num_instances_available':num_instances_available,
        		'num_authors':num_authors,
        		'num_tolkien_books':num_tolkien_books,
        		'num_genres':num_genres,
                'num_visits':num_visits},
    )

class BookListView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = Book
    paginate_by = 10

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = Author
    paginate_by = 10

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    model = Author

