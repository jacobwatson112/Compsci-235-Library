import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left
from werkzeug.security import generate_password_hash
from library.domain.model import Publisher, Author, Book, SearchMethod, User, Review, ReadingCollection

from library.adapters.abstractrepository import AbstractRepository




class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = []
        self.__reviews = []
        self.__search = SearchMethod(self.__books, self.__reviews)
        self.__users = []
        self.__publishers = []
        self.__authors = []


    # returns all books in the repository
    @property
    def books(self) -> List[Book]:
        return self.__books

    # returns all the publishers in the repository
    @property
    def publishers(self) -> List[Publisher]:
        return self.__publishers

    # returns all authors in the repository
    @property
    def authors(self) -> List[Author]:
        return self.__authors

    # returns all reviews in repository
    @property
    def reviews(self) -> List[Review]:
        return self.__reviews

    # adds a review to the repository
    def add_review(self, review: Review):
        if isinstance(review, Review):
            self.__reviews.append(review)

    # gets review for a book from the repository
    def get_reviews(self, book: Book) -> List[Review]:
        self.__search.search_reviews_by_book(book)
        return self.__search.found_items

    # adds a user to the repository
    def add_user(self, user: User):
        if isinstance(user, User):
            self.__users.append(user)

    # gets a user based on the given user_name
    def get_user(self, user_name: str):
        return next((user for user in self.__users if user.user_name == user_name), None)

    # gets a user based on the given user_id
    def get_user_by_id(self, user_id: str):
        return next((user for user in self.__users if user.user_id == user_id), None)

    # adds a book to the repository
    def add_book(self, book):
        if isinstance(book, Book):
            self.__books.append(book)

    # gets a book based on the given book_id
    def get_book(self, book_id) -> Book:
        for book in self.__books:
            if book.book_id == int(book_id):
                return book
        return None

    def get_books_by_title(self, title: str):
        self.__search.search_by_title(title)
        return self.__search.found_items

    def get_authors_by_name(self, name: str):
        authors = []
        for author in self.__authors:
            if name.lower()  in author.full_name.lower():
                authors.append(author)
        return authors

    def get_tags_by_input(self, input: str):
        tags = set()
        for book in self.__books:
            for tag in book.tags:
                if input in tag:
                    tags.add(tag)
        return tags

    # returns the amount of books in the repository
    def get_num_books(self) -> int:
        return len(self.__books)

    # returns books with the given tag
    def get_books_by_tag(self, tag: str) -> List[Book]:
        self.__search.search_by_tag(tag)
        return self.__search.found_items

    # gets books written by an inputted author
    def get_books_by_author(self, author: Author) -> List[Book]:
        self.__search.search_by_author(author)
        return self.__search.found_items

    # gets books within a given publication year range
    def get_books_by_date_range(self, start: int, end: int) -> List[Book]:
        self.__search.search_by_date_range(start, end)
        return self.__search.found_items

    # gets books related to the given books.
    def get_related_books(self, book: Book) -> List[Book]:
        return self.__search.search_related_books(book)

    # gets books by publisher
    def get_books_by_publisher(self, publisher: Publisher) -> List[Book]:
        self.__search.search_books_by_publisher(publisher)
        return self.__search.found_items

    # adds an author to repository
    def add_author(self, author_input: Author):
        self.__authors.append(author_input)

    # gets an author from the repository with the given id
    def get_author(self, author_id) -> Author:
        return next((author for author in self.__authors if author.unique_id == author_id), None)

    # gets the number of authors in the repository
    def get_num_authors(self) -> int:
        return len(self.__authors)

    # adds the publisher to repository
    def add_publisher(self, publisher_input: Publisher):
        if isinstance(publisher_input, Publisher):
            self.__publishers.append(publisher_input)

    # gets a publisher from the repository based on the inputted name
    def get_publisher(self, publisher_name) -> Publisher:
        return next((publisher for publisher in self.__publishers if publisher.name == publisher_name), None)

    # gets the number of publishers in the repository
    def get_num_publishers(self) -> int:
        return len(self.__publishers)

    #following methods are only required by the database repository and is not needed by the memory repository.
    def add_entry(self, entry):
        pass

    def update_entry(self, entry):
        pass


