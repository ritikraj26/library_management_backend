from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Book


class BookEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_books(self):
        Book.objects.create(
            title="Book 1",
            authors="Author 1",
            publication_date="2024-01-01",
            isbn="1234567890123",
            description="Description 1"
        )
        Book.objects.create(
            title="Book 2",
            authors="Author 2",
            publication_date="2024-01-02",
            isbn="1234567890124",
            description="Description 2"
        )
        response = self.client.get("/api/books/")
        print(response)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertEqual(len(data), 2)

    def test_create_book(self):
        response = self.client.post(
            "/api/books/",
            {
                "title": "Book 1",
                "authors": "Author 1",
                "publication_date": "2024-01-01",
                "isbn": "1234567890123",
                "description": "Description 1"
            },
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Book 1")
        self.assertEqual(data["authors"], "Author 1")
        self.assertEqual(data["publication_date"], "2024-01-01")
        self.assertEqual(data["isbn"], "1234567890123")
        self.assertEqual(data["description"], "Description 1")

    def test_single_book(self):
        book = Book.objects.create(
            title="Book 1",
            authors="Author 1",
            publication_date="2024-01-01",
            isbn="1234567890123",
            description="Description 1"
        )
        response = self.client.get(f"/api/books/{book.isbn}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Book 1")
        self.assertEqual(data["authors"], "Author 1")
        self.assertEqual(data["publication_date"], "2024-01-01")
        self.assertEqual(data["isbn"], "1234567890123")
        self.assertEqual(data["description"], "Description 1")

    def test_update_book(self):
        book = Book.objects.create(
            title="Book 1",
            authors="Author 1",
            publication_date="2024-01-01",
            isbn="1234567890123",
            description="Description 1"
        )
        response = self.client.put(
            f"/api/books/{book.isbn}/",
            {
                "title": "Book 2",
                "authors": "Author 2",
                "publication_date": "2024-01-02",
                "description": "Description 2"
            },
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Book 2")
        self.assertEqual(data["authors"], "Author 2")
        self.assertEqual(data["publication_date"], "2024-01-02")
        self.assertEqual(data["isbn"], "1234567890123")
        self.assertEqual(data["description"], "Description 2")

    def test_delete_book(self):
        book = Book.objects.create(
            title="Book 1",
            authors="Author 1",
            publication_date="2024-01-01",
            isbn="1234567890123",
            description="Description 1"
        )
        response = self.client.delete(f"/api/books/{book.isbn}/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Book.objects.filter(isbn=book.isbn).exists())


class UserEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_sign_in(self):
        response = self.client.post(
            "/api/sign_in/",
            {
                "username": "testuser",
                "password": "testpassword"
            },
            format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_sign_up(self):
        response = self.client.post(
            "/api/sign_up/",
            {
                "username": "newuser",
                "password": "newpassword",
                "email": "new@email.com",
                "first_name": "New",
                "last_name": "User"
            },
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "User created")
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_sign_out(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/sign_out/")
        self.assertEqual(response.status_code, 200)


