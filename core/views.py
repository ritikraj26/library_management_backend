from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

from rest_framework.decorators import api_view

from .serializers import BookSerializer
from .models import Book

import json

@csrf_exempt
@api_view(["GET", "POST"])
def book_list(request, page=1):
    if request.method == "GET":
        books = Book.objects.all()
        paginator = Paginator(books, 10)
        page_obj = paginator.get_page(page)
        serializer = BookSerializer(page_obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        authors = data.get("authors")
        publication_date = data.get("publication_date")
        isbn = data.get("isbn")
        description = data.get("description")
        try:
            book = Book.objects.create(
                title=title,
                authors=authors,
                publication_date=publication_date,
                isbn=isbn,
                description=description
            )
            serializer = BookSerializer(book)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def book_view(request, isbn):
    if request.method == "GET":
        try:
            book = Book.objects.get(isbn=isbn)
            serializer = BookSerializer(book)
            return JsonResponse(serializer.data, safe=False)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book does not exist"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    elif request.method == "PUT":
        try:
            book = Book.objects.get(isbn=isbn)

            data = json.loads(request.body)
            title = data.get("title", book.title)
            authors = data.get("authors", book.authors)
            publication_date = data.get("publication_date", book.publication_date)
            description = data.get("description", book.description)

            book.title = title
            book.authors = authors
            book.publication_date = publication_date
            book.isbn = isbn
            book.description = description
            book.save()

            serializer = BookSerializer(book)
            return JsonResponse(serializer.data, safe=False)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book does not exist"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    elif request.method == "DELETE":
        try:
            book = Book.objects.get(isbn=isbn)
            book.delete()
            return JsonResponse({"message": "Book deleted"})
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book does not exist"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid request method"})


@csrf_exempt
@api_view(["POST","GET"])
def sign_up(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        user = User.objects.filter(username=username)
        if user:
            return JsonResponse({"error": "User already exists"})

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse({"message": "User created"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return HttpResponse("Sign up page")



@csrf_exempt
@api_view(["POST", "GET"])
def sign_in(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "User signed in"})
        else:
            return JsonResponse({"error": "Invalid credentials"})
    else:
        return HttpResponse("Sign in page")


@csrf_exempt
@api_view(["POST", "GET"])
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "User signed out"})
    else:
        return HttpResponse("Sign out page")