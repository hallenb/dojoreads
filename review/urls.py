from django.urls import path
from.import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('addReview', views.add_review),
    path('logout', views.logout),
    path('addbook', views.addbook),
    path('books/<int:num>', views.book_desc),
    path('newReview/<int:num>', views.new_review),
    path('user/<int:num>', views.user_review)
]