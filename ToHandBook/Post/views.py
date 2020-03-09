from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from .models import Book
from Message.models import Message


# Create your views here.

def index(request):
    user_view = request.user
    search_txt = request.GET.get('inputSearch', '')
    print(search_txt)
    what_book = request.GET.get('what_book', '')
    books = Book.objects.filter(name_book__icontains = search_txt, status = True)
    if what_book:
        books = books.filter(type_post = what_book)
    return render(request, 'index.html', context={
        'search_txt': search_txt,
        'what_book': what_book,
        'booktype': Book.type_for,
        'books': books,
        'user_view': user_view,
    })

def my_login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    return render(request, template_name='login.html', context=context)

def my_logout(request):
    logout(request)
    return redirect('login')

def my_register(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username = username) :
            context['error1'] = 'ชื่อซ้ำ'
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(email = email) :
            context['error2'] = 'emailซ้ำ'
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User.objects.create_user(username,email,password,first_name = first_name,last_name = last_name)
        if user:
            login(request, user)
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='register.html', context=context)

def create_post(request):
    if request.method == 'POST':
        try:
            upload_file = request.FILES['picfile']
            fs = FileSystemStorage()
            name = fs.save(upload_file.name, upload_file)
            url = fs.url(name)
        except MultiValueDictKeyError:
            upload_file = False
            url = '\media\default.PNG'
        print(url)
        book = Book.objects.create(
            create_by = request.user,
            name_book = request.POST.get('book_name'),
            type_post = request.POST.get('type_post'),
            price = request.POST.get('price'),
            picture = url,
        )
        if book:
            return redirect('index')

    return render(request, 'create_post.html', context={})

def view_post(request, book_id):
    book_view = Book.objects.get(pk = book_id)
    comment_text = Message.objects.filter(post_id_id = book_id)
    return render(request, 'view_post.html', context={
        'book_view' : book_view,
        'book_id': book_id,
        'comment_text':comment_text,
    })

def sold_out(request, book_id):
    book = Book.objects.get(pk=book_id)
    print(book.status)
    book.status = False
    print(book.status)
    book.save()
    if book.status == False:
        return redirect('index')
    return render(request, 'view_post.html', context={})

def comment(request, book_id):
    if request.method == 'POST':
        book_view = Book.objects.get(pk = book_id)
        comment = Message.objects.create(
            message = request.POST.get('inputext'),
            post_id = book_view,
            create_by = request.user,
        )
        comment_text = Message.objects.filter(post_id_id = book_id)
        return render(request, 'view_post.html', context={
            'book_view' : book_view,
            'book_id': book_id,
            'comment_text':comment_text,
        })
