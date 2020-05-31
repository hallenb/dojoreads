from django.shortcuts import render, redirect
from django.contrib import messages
from review.models import User, Author, Book, Review
import bcrypt


def index(request):
    return render(request, 'index.html')

def books(request):
    if 'alias' in request.session:
        
        context = {
            'book': Book.objects.all(),
            'review': Review.objects.all().order_by("-id")[:3] 
        }
        return render(request, 'books.html', context)
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add_review(request):
    if 'alias' in request.session:
        context = {
            'author': Author.objects.all()
        }
        return render(request, 'addbook.html', context)
    return redirect('/')

def addbook(request):
    if request.method=="POST":
        print(request.POST)
        if request.POST['addauthor'] != "":
            Au = Author.objects.create(name=request.POST['addauthor'])
        else:
            Au_Obj = Author.objects.filter(name=request.POST['author'])
            Au = Au_Obj[0]
        print(Au)
        Bo = Book.objects.create(author=Au, title=request.POST['title'])
        Us = User.objects.get(id=request.session['id'])
        Review.objects.create(user=Us, book=Bo, review=request.POST['review'], rating=request.POST['rating'])
        return redirect('/addReview')

def book_desc(request, num):
    if 'alias' in request.session:
        context = {
            'book': Book.objects.get(id=num)
        }
        return render(request, 'review.html', context)
    return redirect('/')

def new_review(request, num):
    if request.method == "POST":
        user = User.objects.get(id=request.session['id'])
        book = Book.objects.get(id=num)
        Review.objects.create(user=user, book=book, review=request.POST['review'], rating=request.POST['rating'])
        return redirect('/books')
    return redirect('/')

def user_review(request, num):
    if 'alias' in request.session:
        context = {
            'user': User.objects.get(id=num)
        }
        return render(request, 'user.html', context)
    

def register(request):
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')

        hashed = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        New_User = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'].lower(), password=hashed.decode())

        request.session['alias'] = New_User.alias
        request.session['id'] = New_User.id 
        return redirect('/books')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        Logged_User = User.objects.filter(email=request.POST['email'])
        if len(Logged_User) > 0:
            Logged_User = Logged_User[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), Logged_User.password.encode()):
                request.session['alias'] = Logged_User.alias
                request.session['id'] = Logged_User.id 
                return redirect('/books')
            return redirect('/')
        return redirect('/')
    return redirect('/')