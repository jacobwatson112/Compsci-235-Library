import abc
from typing import List

from library.domain.model import Publisher, Author, Book, SearchMethod, User, Review, ReadingCollection

repo_instance = None


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def books(self) -> List[Book]:
        # returns all books in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def publishers(self) -> List[Publisher]:
        # returns all the publishers in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def authors(self) -> List[Author]:
        # returns all authors in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def reviews(self) -> List[Review]:
        # returns all reviews in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        # adds a review to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self, book: Book) -> List[Review]:
        # returns reviews of a given book.
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        # adds a user to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str):
        # gets a user based on the given user_name
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        # adds a book to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book_id: int) -> Book:
        # gets a book based on the given book_id
        raise NotImplementedError

    @abc.abstractmethod
    def get_num_books(self) -> int:
        # returns the amount of books in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_tag(self, tag: str) -> List[Book]:
        # returns books with the given tag
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author(self, author: Author) -> List[Book]:
        # gets books written by an inputted author
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_date_range(self, start: int, end: int) -> List[Book]:
        # gets books within a given publication year range
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_title(self, title: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_related_books(self, book: Book) -> List[Book]:
        # gets books related to the given books.
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_publisher(self, publisher: Publisher) -> List[Book]:
        # gets books by publisher
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author_input: Author):
        # adds an author to repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, author_id) -> Author:
        # gets an author from the repository with the given id
        raise NotImplementedError

    @abc.abstractmethod
    def get_num_authors(self) -> int:
        # gets the number of authors in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher_input: Publisher):
        # adds the publisher to repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher(self, publisher_name) -> Publisher:
        # gets a publisher from the repository based on the inputted name
        raise NotImplementedError

    @abc.abstractmethod
    def get_num_publishers(self) -> int:
        # gets the number of publishers in the repository
        raise NotImplementedError


def populate():
    user = repo_instance.get_user("samuel")
    reading_list = ReadingCollection(user, "currently reading")
    user.add_reading_list(reading_list)
    books = []
    try:
        books = repo_instance.books()[:5]
    except TypeError:
        books = repo_instance.books[:5]
    for i in books:
        reading_list.add_entry(i, "Reading", 146)
        # print(i)


def add_users(filename):
    print("REPO", repo_instance)
    with open(filename) as f:
        for line in f.readlines():
            user_id, user_name, password = line.split(",")
            user = User(user_name, password.strip(), user_id)
            repo_instance.add_user(user)
