import base64
import os
import json
import socket
import smtplib
import random
import graphene
from mimetypes import guess_extension
from django.shortcuts import render, HttpResponse
from django.contrib.auth import login as django_login, logout as django_logout
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from graphene_django import DjangoObjectType
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes
from .models import Stud, Book, PurchasedBook, Image, FeedBack
from .serializers import StudentSerializer, BookSerializer, PurchasedBookSerializer, ImageSerializer, FeedBackSerializer, BookModelMutation
from bookSharingBackend.schema import schema

# from .permissions import IsOwnerOrReadOnly

# Create your views here.


def index(request):
    return HttpResponse("Hello")


def room(request, room_name):
    return render(request, 'index.html', {
        'room_name': room_name
    })


class webSocket(APIView):
    def get(self):
        pass


class StudentList(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication,
    #                           BasicAuthentication, TokenAuthentication]

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_class = (FileUploadParser, MultiPartParser, JSONParser)
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        student = Stud.objects.all()
        serializer = StudentSerializer(student, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        # print(request.data)
        # request.data['photo'] = ContentFile(base64.b64decode(
        #     request.data['photo']), name=request.data['enrollmentNo']+'.'+'jpg')
        student = Stud.objects.filter(
            email=request.data['email']).values()
        # print(student)
        serializer = StudentSerializer(student, many=True)

        #     return Response("HEllo")
        # return Response("exist")

        if serializer.data == []:
            data = {}
            # data['enrollmentNo'] = request.data['enrollmentNo']
            data['firstName'] = request.data['firstName']
            data['lastName'] = request.data['lastName']
            data['email'] = request.data['email']
            data['age'] = int(request.data['age'])
            # data['course'] = request.data['course']
            data['password'] = request.data['password']
            # data['collegeName'] = request.data['collegeName']
            # data['collegeYear'] = int(request.data['collegeYear'])
            data['address'] = request.data['address']
            data['contactNo'] = request.data['contactNo']
            # extn = request.data['photo'].split(';')[0].split('/')[1]
            if request.data['photo'] != "":
                data['photo'] = ContentFile(base64.b64decode(request.data['photo']), name=request.data['email']+'.'+request.data['extansion'])

            serializer = StudentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Student already Exist")


class StudentDetail(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication,
    #                           BasicAuthentication, TokenAuthentication]
    # def getStudent(self, enrollmentNo):
    #     student = Stud.objects.filter(
    #         enrollmentNo=enrollmentNo)
    #     return student

    def get_object(self, pk):
        return Stud.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        # print(snippet)
        serializer = StudentSerializer(student)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        student = self.get_object(pk)
        # print(student)
        if os.path.isfile(student.photo.path):
            os.remove(student.photo.path)
        student.delete()
        return Response("Success", status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, formate=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # student.save()
            return Response("success", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookLatestList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.order_by('-postedDate')[:5]

    serializer_class = BookSerializer


class HomeList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()[6:11]

    serializer_class = BookSerializer

# To create a GraphQL schema for it you simply have to write the following:
# class Query(graphene.ObjectType):
#     users = graphene.List(Book)

#     def resolve_users(self, info):
#         return Book.objects.all()

# schema = graphene.Schema(query=Query)


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class BookMutation(APIView):

    def get(self, request):
        query = '''
            
            query hello{
              allIngredients{
                edges{
                  node{
                    id
                    bookId
                    bookName
                    isbnNo
                    authorName
                    pubName
                    originalPrice
                    price
                    bookCatgName  
                    postedBy{
                      id
                      firstName
                      lastName
                      email
                      age
                    }
                  }
                }
              }
            }

         '''
        result = schema.execute(query)
        return Response(result.data)


# curl -X GET http://127.0.0.1:8000/booksharing/book/ -H 'Authorization: Token c19a600c77f8633a0f79c737b1851bbbb4f5e661' | json_pp
class BookList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes=[TokenAuthentication,SessionAuthentication,BasicAuthentication]

    # parser_class = (FileUploadParser, MultiPartParser, JSONParser)
    """
    List all snippets, or create a new snippet.
    """
    # def getPerson(self):
    #     stud=Stud.objects.filter(pk=book['postedBy'])
    #     return stud

    # def get(self, request, format=None):
    # serializer_context = {
    #     'request': request,
    # }
    queryset = Book.objects.all()
    # print(queryset)
    # serializer = BookSerializer(
    #     book, many=True, context=serializer_context)
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # print(book)
    serializer_class = BookSerializer
    # return Response(serializer_class)

    def post(self, request, format=None):

        # print(request.data['bookName'])
        bookJsonEncode = json.dumps(request.data)
        bookImages = bookJsonEncode.pop('Book_Image')
        bookImagesExtn = bookJsonEncode.pop('extn')
        # request.data['photo'] = data
        serializer = BookSerializer(data=bookJsonEncode)
        if serializer.is_valid():
            serializer.save()
            count = 0
            for bookImage in bookImages:
                image = {}
                image['id'] = serializer.data
                image['image'] = ContentFile(base64.b64decode(
                    bookImage['photo']), name=bookJsonEncode['bookName']+'.'+bookImagesExtn[count])
                count = count+1
                imageSerializer = ImageSerializer(data=image)
                if imageSerializer.is_valid():
                    imageSerializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):

        return Book.objects.get(pk=pk)

    def get_bookImage(self, pk):
        return Image.objects.filter(bookId=pk)

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        # print(snippet)
        serializer = BookSerializer(book)
        # print(serializer.data)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        image = self.get_bookImage(pk)
        # print(image)
        for bookImage in image:
            if os.path.isfile(bookImage.image.path):
                os.remove(bookImage.image.path)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, formate=None):
        book = self.get_object(pk)

        # count = 0
        # for image in images:
        #     newImage = request.data['image'][count]
        #     # newImage = ContentFile(base64.b64decode(
        #     #     newImage), name=book['bookName']+'.'+bookImagesExtn[count])
        #     if(image['image'] != newImage):
        #         image.delete()
        #         if os.path.isfile(image['image'].path):
        #             os.remove(image['image'].path)
        #     else:
        #         serializer = ImageSerializer(data=newImage)
        #         if serializer.is_valid():
        #             serializer.save()
        #         return Response("Image updated successfully")
        #     count += 1

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Success", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchasedBookList(APIView):
    permission_classes = [IsAuthenticated]

    parser_class = (FileUploadParser, MultiPartParser, JSONParser)
    """
    List all snippets, or create a new snippet.
    """

    def getBookObj(self, pk):
        book = Book.objects.get(pk=pk)
        return book

    def getStudObj(self, contactNo):
        stud = Stud.objects.get(contactNo=contactNo)
        return stud

    def getStudObjValues(self, contactNo):
        stud = Stud.objects.filter(contactNo=contactNo).values()
        return stud

    def get(self, request, format=None):
        purchasedBook = PurchasedBook.objects.all()
        serializer = PurchasedBookSerializer(purchasedBook, many=True)
        # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

        return Response(serializer.data)

    def post(self, request, format=None):

        book = self.getBookObj(request.data['bookId'])
        stud = self.getStudObjValues(request.data['contactNo'])

        # bookSerializer=BookSerializer(book,many=True)
        # print(len(stud))
        if len(stud) != 0:
            #     print("Not NUll")
            # else:
            #     print ("Null")
            # if studSerializer.data != []:
            purchasedBook = {}
            student = self.getStudObj(request.data['contactNo'])
            studSerializer = StudentSerializer(student)
            # print(studSerializer)
            # print()
            purchasedBook['studId'] = studSerializer.data['id']
            purchasedBook['bookName'] = book.bookName
            purchasedBook['price'] = book.price
            purchasedBook['isbnNo'] = book.isbnNo
            # print()
            purchasedBookSerializer = PurchasedBookSerializer(
                data=purchasedBook)
            print(purchasedBookSerializer)
            if purchasedBookSerializer.is_valid():
                purchasedBookSerializer.save()
                book.delete()
                return Response("Success", status=status.HTTP_201_CREATED)
            else:
                return Response(purchasedBookSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Student doesn't exist with this contact Number")

        # print(base64.urlsafe_b64decode(request.data['image']))
        # print(request.data['image'][0])
        # name = request.data['name'].split(';base64,')

        # print(base64.b64decode(request.data['image']))
        # data = ContentFile(base64.b64decode(request.data['image']),name=request.data['name']+'.'+'jpg')
        # print(data)
        # getData={}
        # getData['name']=request.data['name']
        # getData['image']=data
        # serializer = StudentSerializer(data=getData)
        # # permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

        # # print(request.data['image'])
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchasedBookDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):

        return PurchasedBook.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        purchasedBook = self.get_object(pk)
        # print(snippet)
        serializer = PurchasedBookSerializer(purchasedBook)
        # print(serializer.data)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        purchasedBook = self.get_object(pk)
        purchasedBook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @permission_classes((permissions.AllowAny,))
class LogIn(APIView):
    permission_classes = [IsAuthenticated]

    def getStudent(self, email, password):
        student = Stud.objects.filter(
            email=email, password=password).values()
        return student

    def post(self, request):
        # student=Stud.objects.filter(enrollmentNo=request.data['enrollmentNo'],password=request.data['password'])
        student = self.getStudent(
            request.data['email'], request.data['password'])
        # print(student)
        serializer = StudentSerializer(student, many=True)
        # if serializer.is_valid():
        # serializer.save()

        if serializer.data != []:

            return Response(student, status=status.HTTP_201_CREATED)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("Enter valid username and password", status=status.HTTP_400_BAD_REQUEST)


class GetPurchasedByStud(APIView):
    permission_classes = [IsAuthenticated]

    def getStudentId(self, studId):
        id = PurchasedBook.objects.filter(studId=studId)
        return id

    def post(self, request):
        purchasedbook = self.getStudentId(
            request.data['studId'])
        # print(purchasedbook)
        serializer = PurchasedBookSerializer(purchasedbook, many=True)
        # if serializer.is_valid():
        # serializer.save()
        if serializer.data != []:

            return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("No Purchased Book", status=status.HTTP_400_BAD_REQUEST)


class BookImageList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser, MultiPartParser, JSONParser)
    """
    List all snippets, or create a new snippet.
    """

    # def get(self, request, format=None):
    #     image = Image.objects.all()
    #     serializer = ImageSerializer(image, many=True)
    #     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #     return Response(serializer.data)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, format=None):
        # data = ContentFile(base64.b64decode(
        #     request.data['photo']), name=request.data['enrollmentNo']+'.'+'jpg')
        # print(data)
        # print("hello")
        # print(request.data['bookName'])
        bookJsonEncode = json.dumps(request.data)
        bookImages = bookJsonEncode.pop('Book_Image')

        # request.data['photo'] = data
        serializer = BookSerializer(data=bookJsonEncode)
        if serializer.is_valid():
            serializer.save()

            for bookImage in bookImages:
                image = {}
                image['id'] = serializer.data
                image['image'] = ContentFile(base64.b64decode(
                    bookImage['photo']), name=bookJsonEncode['bookName']+'.'+'jpg')

                imageSerializer = ImageSerializer(data=image)
                if imageSerializer.is_valid():
                    imageSerializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookImageDetail(APIView):
    permission_classes = [IsAuthenticated]
    # def getStudent(self, enrollmentNo):
    #     student = Stud.objects.filter(
    #         enrollmentNo=enrollmentNo)
    #     return student

    def get_object(self, pk):
        return Image.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        # print(snippet)
        serializer = ImageSerializer(image)
        # print(serializer.data)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, formate=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedBackList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # parser_class = (FileUploadParser, MultiPartParser, JSONParser)
    """
    List all snippets, or create a new snippet.
    """
    # def getPerson(self):
    #     stud=Stud.objects.filter(pk=book['postedBy'])
    #     return stud

    # def get(self, request, format=None):
    # serializer_context = {
    #     'request': request,
    # }

    queryset = FeedBack.objects.all()
    # print(queryset)
    # serializer = BookSerializer(
    #     book, many=True, context=serializer_context)
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # print(book)
    serializer_class = FeedBackSerializer
    # return Response(serializer_class)

    def post(self, request, format=None):

        # print(request.data['bookName'])
        # bookJsonEncode = json.dumps(request.data)
        # bookImages = bookJsonEncode.pop('Book_Image')

        # request.data['photo'] = data
        serializer = FeedBackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response("Success", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedBackDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):

        return FeedBack.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        feedBack = self.get_object(pk)
        # print(snippet)
        serializer = FeedBackSerializer(feedBack)
        # print(serializer.data)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        feedBack = self.get_object(pk)
        feedBack.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, formate=None):
        feedBack = self.get_object(pk)
        serializer = FeedBackSerializer(feedBack, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Success", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookImageById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        image = Image.objects.all()
        serialize = ImageSerializer(image, many=True)
        return Response(serialize.data)


class BookPost(APIView):
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser, MultiPartParser, JSONParser)

    def post(self, request, format=None):
        # print("Hello")

        # bookJsonEncode = json.dumps(request.data,separators=(",","/"))
        bookImages = request.data.pop('Book_Image')
        # list(bookImages)
        # print(request.data)
        # request.data['photo'] = data
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            for bookImage in bookImages:
                # print("hello")
                image = {}
                image['bookId'] = serializer.data['bookId']
                image['image'] = ContentFile(base64.b64decode(
                    bookImage), name=request.data["bookName"]+'.'+'jpg')

                imageSerializer = ImageSerializer(data=image)
                if imageSerializer.is_valid():
                    imageSerializer.save()
            return Response("success", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookByPosted(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        book = Book.objects.filter(postedBy=pk)
        serializer = BookSerializer(book, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def getStudObj(self, password, pk):
        stud = Stud.objects.get(password=password, pk=pk)
        return stud

    def getStudObjValues(self, password, pk):
        stud = Stud.objects.filter(password=password, pk=pk).values()
        return stud

    def post(self, request, pk):

        stud = self.getStudObjValues(request.data['password'], pk)
        if len(stud) != 0:
            # pass
            student = self.getStudObj(request.data['password'], pk)
            data = {}
            data['password'] = request.data['newpassword']
            serializer = StudentSerializer(student, data=data)
            # print(serializer)
            # return Response("sucess")
            if serializer.is_valid():
                serializer.save()
                return Response("success", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Enter Right Old Password")


class UpdateStudentPhoto(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Stud.objects.get(pk=pk)

    def put(self, request, pk, formate=None):
        student = self.get_object(pk)

        print(student.photo)
        if student.photo:
            if os.path.isfile(student.photo.path):
                # student.photo.delete()
                os.remove(student.photo.path)
        studentPhoto = {}
        studentPhoto['photo'] = ContentFile(base64.b64decode(
            request.data['photo']), name=request.data['studentName']+'.'+request.data['extansion'])
        serializer = StudentSerializer(student, data=studentPhoto)
        if serializer.is_valid():
            serializer.save()

            return Response("success", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response("hello")


class PurchasedBookByUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        purchasedBook = PurchasedBook.objects.filter(studId=pk)
        serializer = PurchasedBookSerializer(purchasedBook, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookImageUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def get_Image_obj(self, pk):
        bookImage = Image.objects.filter(bookId=pk)
        return bookImage

    def put(self, request):
        bookImage = self.get_Image_obj(request.data['bookId'])
        if bookImage:
            count = int(request.data['count'])
            # print(type(count))
            bookImage = list(bookImage)
            print(bookImage[count])
            bookImageData = {}

            bookImageData['bookId'] = request.data['bookId']
            # bookImageData['image'] = request.data['image']
            bookImageData['image'] = ContentFile(base64.b64decode(
                request.data['image']), name=request.data['bookName']+'.'+request.data['extansion'])
            serializer = ImageSerializer(bookImage[count], data=bookImageData)
            if serializer.is_valid():
                serializer.save()
                return Response("Success", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Image with this book is not found", status=500)


class AddImageList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        extn = request.data['extn']
        images = request.data['Book_Image']
        count = 0
        for image in images:
            img = {}
            img['bookId'] = request.data['bookId']
            img['image'] = ContentFile(base64.b64decode(
                image), name=request.data['bookName']+'.'+extn[count])
            count += 1
            imageSerializer = ImageSerializer(data=img)
            if imageSerializer.is_valid():
                imageSerializer.save()

        return Response("Success", status=status.HTTP_200_OK)
        # return Response(imageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        value = random.randrange(10000, 99999)
        message = 'Subject: {}\n\n{}'.format(
            "OTP", "From Book Shearing")+"\n" + "OTP is :" + str(value)
        print(message)
        mailserver = smtplib.SMTP('smtp.gmail.com')
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login('abhishekghaskata1999@gmail.com',
                         'ABHI01039@FlutterAI')
        mailserver.sendmail("abhishekghaskata1999@gmail.com",
                            request.data['email'], message)
        return Response(value, status=status.HTTP_200_OK)
        # subject = "This is first email"
        # message = "This is message"
        # from_email = settings.EMAIL_HOST_USER
        # recipient_list = request.data['email']
        # to_list = ["bociwin947@oriwijn.com", recipient_list]
        # socket.getaddrinfo('127.0.0.1', 8080)
        # send_mail(subject, message, from_email, to_list, fail_silently=False)


class UpdatePassword(APIView):
    def get_object(self, pk):
        return Stud.objects.get(email=pk)

    def put(self, request):

        student = self.get_object(request.data['email'])

        if student != None:
            # print(student)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("success", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Email doesn't exist", status=status.HTTP_400_BAD_REQUEST)
