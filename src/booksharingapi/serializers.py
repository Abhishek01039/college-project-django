from django.conf.urls import url, include

from rest_framework import routers, serializers, viewsets
from .models import Stud, Book, PurchasedBook, Image, FeedBack
from rest_framework import serializers, fields, exceptions
from django.contrib.auth import authenticate

# class CategorySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Category
#         fields =['catgId','catgName']


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stud
        fields = ['id', 'enrollmentNo', 'firstName', 'lastName', 'email',
                  'age', 'collegeName', 'collegeYear', 'course', 'password', 'address', 'contactNo', 'photo']

    def create(self, validated_data):
        return Stud.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.enrollmentNo = validated_data.get(
            'enrollmentNo', instance.enrollmentNo)
        instance.firstName = validated_data.get(
            'firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.collegeName = validated_data.get(
            'collegeName', instance.collegeName)
        instance.collegeYear = validated_data.get(
            'collegeYear', instance.collegeYear)
        instance.course = validated_data.get('course', instance.course)
        instance.password = validated_data.get('password', instance.password)
        instance.address = validated_data.get('address', instance.address)
        instance.contactNo = validated_data.get(
            'contactNo', instance.contactNo)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance


class PurchasedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedBook
        fields = ('purid', 'studId', 'bookName', 'price', 'isbnNo')

    def create(self, validated_data):
        return PurchasedBook.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.purid = validated_data.get('purid', instance.purid)
        instance.studId = validated_data.get('studId', instance.studId)
        instance.bookName = validated_data.get('bookName', instance.bookName)
        instance.price = validated_data.get('price', instance.price)
        instance.isbnNo = validated_data.get('price', instance.isbnNo)
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('bookId', 'image')

    def create(self, validated_data):
        return Image.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.bookId = validated_data.get('bookId', instance.bookId)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name="booksharingapi:Stud")
    # user = StudentSerializer()
    Book_Image = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ('bookId', 'bookName', 'isbnNo', 'authorName', 'pubName',  'originalPrice', 'price',
                  'bookCatgName', 'postedBy', 'postedDate', 'Book_Image')

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.bookId = validated_data.get('bookId', instance.bookId)
        instance.bookName = validated_data.get('bookName', instance.bookName)
        instance.isbnNo = validated_data.get('isbnNo', instance.isbnNo)
        instance.authorName = validated_data.get(
            'authorName', instance.authorName)
        instance.pubName = validated_data.get('pubName', instance.pubName)
        instance.originalPrice = validated_data.get(
            'originalPrice', instance.originalPrice)
        instance.price = validated_data.get('price', instance.price)
        instance.bookCatgName = validated_data.get(
            'bookCatgName', instance.bookCatgName)
        instance.postedBy = validated_data.get('postedBy', instance.postedBy)
        instance.postedDate = validated_data.get(
            'postedDate', instance.postedDate)
        instance.save()
        return instance


class FeedBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBack
        fields = ('fid', 'studName', 'email', 'message')

    def create(self, validated_data):
        return FeedBack.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fid = validated_data.get('fid', instance.fid)
        instance.studName = validated_data.get('studName', instance.studName)
        instance.email = validated_data.get('email', instance.email)
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance
