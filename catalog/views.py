from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime

from .forms import RenewBookForm

# Create your views here.d
@login_required
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

"""
Generic class-based view listing books on loan to current user. 
"""
class BookListView(LoginRequiredMixin, generic.ListView):
    login_url = settings.LOGIN_URL
    model = Book
    paginate_by = 10

"""
Generic class-based view listing books on loan to current user. 
"""
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = settings.LOGIN_URL
    model = Book

"""
Generic class-based view listing books on loan to current user. 
"""
class AuthorListView(LoginRequiredMixin, generic.ListView):
    login_url = settings.LOGIN_URL
    model = Author
    paginate_by = 10

"""
Generic class-based view listing books on loan to current user. 
"""
class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = settings.LOGIN_URL
    model = Author

"""
Generic class-based view listing books on loan to current user. 
"""
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedBooks(generic.ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all_borrowed_books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Author
    fields = '__all__'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Author
    success_url = reverse_lazy('authors')