from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from accounts.utils import login_required_custom
from books.forms import BookModelForm
from books.models import Books


def book_list(request):
    search = request.GET.get('search', '')
    page = request.GET.get('page')
    books = Books.objects.all()  # Queryset list [<booq1>.
    if search:
        books = books.filter(Q(title__icontains=search) | Q(description__icontains=search))
    paginator = Paginator(books, 3)
    books = paginator.get_page(page)
    return render(request, 'books/list.html', {"books": books, 'search': search})


def book_detail(request, pk):
    book = Books.objects.filter(id=pk).first()
    return render(request, 'books/detail.html', {"book": book})


@login_required
def book_create_form(request):
    # form = BooksForm()
    form = BookModelForm()
    return render(request, 'books/create.html', {"form": form})


@login_required
def book_create(request):
    # data = request.POST
    # book = Books(title=data.get("title"), description=data.get("description"), price=data.get("price"))
    # book.save()
    # # Books.objects.create(title=data['title'], description=data['description'], price=data['price'])
    # return redirect('book_list')
    # form = BooksForm(request.POST)
    form = BookModelForm(request.POST)
    if form.is_valid():
        # data = form.cleaned_data
        # Books.objects.create(**data)
        form.save()
        return redirect('book_list')
    return render(request, 'books/create.html', {"form": form})


@login_required
def book_update_forme(request, pk=None):
    book = Books.objects.filter(id=pk).first()
    form = BookModelForm(instance=book)
    return render(request, 'books/update.html', {"form": form, "book": book})


@login_required
def book_update(request, pk=None):
    # Books.objects.filter(id=pk).update(title=request.POST.get("title"), description=request.POST.get("description"),
    #                                    price=request.POST.get("price"))
    book = Books.objects.filter(id=pk).first()
    form = BookModelForm(instance=book, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/update.html', {"form": form, "book": book})


@login_required_custom
def book_delete(request, pk=None):
    Books.objects.filter(id=pk).delete()
    return redirect('book_list')
