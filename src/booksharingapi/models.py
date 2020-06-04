from __future__ import unicode_literals
from django_cleanup import cleanup
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete, post_delete
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Stud(models.Model):
    id = models.AutoField(primary_key=True)
    enrollmentNo = models.CharField(max_length=30, default='')
    firstName = models.CharField(max_length=20, default='')
    lastName = models.CharField(max_length=20, default='')
    email = models.EmailField(max_length=200, default='', unique=True)
    age = models.IntegerField(default=0)
    collegeName = models.CharField(max_length=200, default='')
    collegeYear = models.IntegerField(default=0)
    course = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=200, default='')
    contactNo = PhoneNumberField(
        null=False, blank=False, unique=True, default="")
    photo = models.FileField(upload_to='Student', blank=True, null=True)

    def __str__(self):
        return self.firstName


# @receiver(post_delete, sender=Stud)
# def mymodel_delete(sender, **kwargs):
#     instance = kwargs.get('instance')

@cleanup.ignore
class Book(models.Model):
    bookId = models.AutoField(primary_key=True)
    bookName = models.CharField(max_length=200)
    isbnNo = models.CharField(max_length=13)
    authorName = models.CharField(max_length=30)
    pubName = models.CharField(max_length=30)
    originalPrice = models.IntegerField()
    price = models.IntegerField()
    bookCatgName = models.CharField(max_length=200, default="")
    postedBy = models.ForeignKey(Stud, on_delete=models.CASCADE,related_name='student')
    postedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bookName

    class Meta:
        get_latest_by = 'postedDate'


# Receive the pre_delete signal and delete the file associated with the model instance.


class PurchasedBook(models.Model):
    purid = models.AutoField(primary_key=True)
    studId = models.ForeignKey(Stud, on_delete=models.CASCADE)
    bookName = models.CharField(max_length=200)
    price = models.IntegerField()
    isbnNo = models.CharField(max_length=13)

    def __str__(self):
        return self.bookName


class Image(models.Model):

    bookId = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='Book_Image', blank=True, null=True)
    image = models.FileField(upload_to='Book', blank=True, null=True)


class FeedBack(models.Model):
    fid = models.AutoField(primary_key=True)
    studName = models.CharField(max_length=20)
    email = models.EmailField(null=True, default="")
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.studName
