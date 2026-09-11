from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Book , Author , Publisher
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .forms import BookForm,AuthorForm,PublisherForm,BookFormWithoutAuthor,BookFormWithoutAuthorPublisher

#function based view for book list
def book_list(request):
    books=Book.objects.all()
    return render(request, 'library/book_list.html', {'books':books})

#class based view for book list
class BookListView(ListView):
    model = Book
    template_name = 'library/cbv_book_list.html'
    context_object_name = 'books'

#function based view for book detail
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/book_detail.html', {'book': book})

#class based view for book detail
class BookDetailView(DetailView):
    model= Book
    template_name = 'library/cbv_book_detail.html'
    context_object_name='book'

def author_list(request):
    authors=Author.objects.all()
    context={'authors':authors}
    return render(request, 'library/author_list.html', context)

def book_by_author(request,author_id):
    author=get_object_or_404(Author,id=author_id)
    books=Book.objects.filter(author=author)
    context={'author':author,'books':books}
    return render(request, 'library/book_by_author.html',context)

def add_book(request):
    if request.method=='POST':
        form=BookForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('book_list_fbv')
    else:
        form=BookForm()
    return render(request,'library/add_book.html',{'form':form})

def add_book_and_author(request):
    if request.method == "POST":
        book_form=BookFormWithoutAuthor(request.POST)
        author_form=AuthorForm(request.POST)
        if book_form.is_valid() and author_form.is_valid():
            author=author_form.save()
            book=book_form.save(commit=False)
            book.author=author
            book.save()
            book_form.instance=book
            book_form.save_m2m()
            return redirect('book_list_fbv')
    else:
        book_form=BookFormWithoutAuthor()
        author_form=AuthorForm()
    context={'book_form':book_form,'author_form':author_form}
    return render(request,'library/add_book_and_author.html',context)

def add_book_author_publisher(request):
    if request.method == "POST":
        book_form = BookFormWithoutAuthorPublisher(request.POST)
        author_form = AuthorForm(request.POST)
        publisher_form = PublisherForm(request.POST)
        if (
            book_form.is_valid()
            and author_form.is_valid()
            and publisher_form.is_valid()
        ):
            author = author_form.save()
            publisher = publisher_form.save()
            book = book_form.save(commit=False)
            book.author = author
            book.save()  
            book.publisher.add(publisher)
            return redirect('book_list_fbv')
    else:
        book_form = BookFormWithoutAuthorPublisher()
        author_form = AuthorForm()
        publisher_form = PublisherForm()
    context={'book_form': book_form,'author_form': author_form,'publisher_form': publisher_form,}
    return render(request,'library/add_book_author_publisher.html',context)
