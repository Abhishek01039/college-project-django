from django.contrib import admin
from .models import Stud, Book, PurchasedBook, Image, FeedBack
# Register your models here.
# admin.site.register(Stud)


admin.site.register(PurchasedBook)
# admin.site.register(Image)
# admin.site.register(FeedBack)
admin.site.site_header = "Book Sharing"
admin.site.site_title = "Book Sharing"


@admin.register(Stud)
class Student(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email')


@admin.register(Book)
class Book(admin.ModelAdmin):

    list_display = ('bookName', 'authorName',
                    'originalPrice', 'price', 'postedDate')


@admin.register(FeedBack)
class FeedBack(admin.ModelAdmin):
    list_display = ('studName', 'email', 'message')


@admin.register(Image)
class Image(admin.ModelAdmin):
    list_display = ('bookId', 'image')
