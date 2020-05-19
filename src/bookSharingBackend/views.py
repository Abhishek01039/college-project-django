from django.http import HttpResponse


def Index(request):
    return HttpResponse("Hello, Welcome to the Book Shearing")
