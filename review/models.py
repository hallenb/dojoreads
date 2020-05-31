from django.db import models
import re


class UserManager(models.Manager):
    def user_validator(self, data):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['name']) < 2:
            errors['name'] = 'Name must be at least 2 characters'
        if len(data['alias']) < 2:
            errors['alias'] = 'Name must be at least 2 characters'
        if len(data['pw']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if data['pw'] != data['confpw']:
            errors['confpw'] = 'Passwords must match'
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Invalid email address!"
        return errors



class User(models.Model):
    name = models.CharField(max_length=150)
    alias = models.CharField(max_length=150)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    author = models.ForeignKey(Author, related_name='book', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='review', on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
