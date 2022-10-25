from datetime import datetime
from typing import List, Set
import random
import os
import library.adapters.abstractrepository as repo


class Publisher:

    def __init__(self, publisher_name: str):
        # This makes sure the setter is called here in the initializer/constructor as well.
        self.__name = "N/A"
        if isinstance(publisher_name, str):
            # Make sure leading and trailing whitespace is removed.
            publisher_name = publisher_name.strip()
            if publisher_name != "":
                self.__name = publisher_name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, publisher_name: str):
        self.__name = "N/A"
        if isinstance(publisher_name, str):
            # Make sure leading and trailing whitespace is removed.
            publisher_name = publisher_name.strip()
            if publisher_name != "":
                self.__name = publisher_name

    def __repr__(self):
        return f'<Publisher {self.name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.name == self.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


class Author:

    def __init__(self, author_id: int, author_full_name: str):
        if not isinstance(author_id, int):
            raise ValueError

        if author_id < 0:
            raise ValueError

        self.__unique_id = author_id

        # Uses the attribute setter method.
        self.full_name = author_full_name

        # Initialize author colleagues data structure with empty set.
        # We use a set so each unique author is only represented once.
        self.__authors_this_one_has_worked_with = set()

    @property
    def unique_id(self) -> int:
        return self.__unique_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, author_full_name: str):
        if isinstance(author_full_name, str):
            # make sure leading and trailing whitespace is removed
            author_full_name = author_full_name.strip()
            if author_full_name != "":
                self.__full_name = author_full_name
            else:
                raise ValueError
        else:
            raise ValueError

    def add_coauthor(self, coauthor):
        if isinstance(coauthor, self.__class__) and coauthor.unique_id != self.unique_id:
            self.__authors_this_one_has_worked_with.add(coauthor)

    def check_if_this_author_coauthored_with(self, author):
        return author in self.__authors_this_one_has_worked_with

    def __repr__(self):
        return f'<Author {self.full_name}, author id = {self.unique_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id == other.unique_id

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __hash__(self):
        return hash(self.unique_id)


class Book:

    def __init__(self, book_id: int, book_title: str):
        if not isinstance(book_id, int):
            raise ValueError

        if book_id < 0:
            raise ValueError

        self.__book_id = book_id

        # use the attribute setter
        self.title = book_title

        self.__description = None
        self.__publisher = None
        self.__authors = []
        self.__release_year = None
        self.__ebook = None
        self.__num_pages = 0
        # !!!new attributes, remember to check for implementation
        # "image_url" is key in the json file for image_url
        self.__image_url = None
        # "average_rating" is the key in the json file for rating
        self.__rating = None
        # "popular_shelves" is the key in the json file for tags
        self.__tags = []

    @property
    def book_id(self) -> int:
        return self.__book_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, book_title: str):
        if isinstance(book_title, str):
            book_title = book_title.strip()
            if book_title != "":
                self.__title = book_title
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        if isinstance(release_year, int) and release_year >= 0:
            self.__release_year = release_year
        else:
            raise ValueError

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.__description = description.strip()

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    @property
    def authors(self) -> List[Author]:
        return self.__authors

    def add_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            return

        self.__authors.append(author)

    def add_tag(self, tag):
        if not isinstance(tag, Tag):
            return
        if tag in self.__tags:
            return
        self.__tags.append(tag)
        # tag.tag_book(self)

    # new properties and methods check for implementation
    @property
    def image_url(self) -> str:
        return self.__image_url

    @image_url.setter
    def image_url(self, url: str):
        self.__image_url = url

    @property
    def rating(self) -> float:
        return self.__rating

    @rating.setter
    def rating(self, rating: float):
        if isinstance(rating, float) and 0 < rating < 5:
            self.__rating = rating

    @property
    def tags(self) -> Set[str]:
        return self.__tags

    @tags.setter
    def tags(self, tags: Set[str]):
        self.__tags = tags

    def remove_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            self.__authors.remove(author)

    @property
    def ebook(self) -> bool:
        return self.__ebook

    @ebook.setter
    def ebook(self, is_ebook: bool):
        if isinstance(is_ebook, bool):
            self.__ebook = is_ebook

    @property
    def num_pages(self) -> int:
        return self.__num_pages

    @num_pages.setter
    def num_pages(self, num_pages: int):
        if isinstance(num_pages, int) and num_pages >= 0:
            self.__num_pages = num_pages

    def __repr__(self):
        return f'<Book {self.title}, book id = {self.book_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.book_id == other.book_id

    def __lt__(self, other):
        return self.book_id < other.book_id

    def __hash__(self):
        return hash(self.book_id)


class ReadingCollection:

    def __init__(self, user, name: str):
        if isinstance(name, str):
            self.__name = name
        self.__book_entries = []
        self.__user = user

    @property
    def book_entries(self):
        return self.__book_entries

    def add_entry(self, book: Book, status: str, pages_read: int):
        entry = BookEntry(self, book, status, pages_read)
        repo.repo_instance.add_entry(entry)
        self.__book_entries.append(entry)

    def __repr__(self):
        return f'<Reading List for {self.__user.user_name}>'


class BookEntry:

    def __init__(self, reading_list, book: Book, status: str, pages_read):
        self.__book = book
        self.__status = status
        self.__pages_read = 0
        self.__reading_list = reading_list
        if isinstance(pages_read, int) and pages_read < book.num_pages:
            self.__pages_read = pages_read
        elif isinstance(pages_read, int) and pages_read == book.num_pages:
            self.__pages_read = pages_read
            self.__status = "Completed"

    @property
    def book(self):
        return self.__book

    @property
    def status(self):
        return self.__status

    @property
    def pages_read(self):
        return self.__pages_read

    def update_status(self, status):
        if isinstance(status, str):
            self.__status = status

    def update_pages_read(self, pages_read):
        if isinstance(pages_read, int) and pages_read < self.__book.num_pages:
            self.__pages_read = pages_read
        elif isinstance(pages_read, int) and pages_read == self.__book.num_pages:
            self.__pages_read = pages_read
            self.__status = "Completed"

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def __repr__(self):
        return f'<Entry {self.__status} {self.__book.title} in {self.__reading_list}>'


class Review:

    def __init__(self, user, book: Book, review_text: str, rating: int):
        if isinstance(book, Book):
            self.__book = book
        else:
            self.__book = None

        if isinstance(review_text, str):
            self.__review_text = review_text.strip()
        else:
            self.__review_text = "N/A"

        if isinstance(rating, int) and rating >= 0 and rating <= 5:
            self.__rating = rating
        else:
            raise ValueError

        self.__timestamp = datetime.now()
        self.__user = user

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return other.book == self.book and other.review_text == self.review_text \
               and other.rating == self.rating and other.timestamp == self.timestamp

    def __repr__(self):
        if self.__user:
            return f'<Review of book {self.book}, by {self.__user}>'
        else:
            return ""


class User:

    def __init__(self, user_name: str, password: str, user_id=""):
        if user_name == "" or not isinstance(user_name, str):
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()

        if password == "" or not isinstance(password, str) or len(password) < 7:
            self.__password = None
        else:
            self.__password = password
        if user_id != "":
            self.__user_id = user_id
        else:
            self.__user_id = os.urandom(32)
        self.__read_books = []
        self.__reviews = []
        self.__pages_read = 0
        # reading list
        self.__reading_list = ReadingCollection(self, "reading list")

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def password(self) -> str:
        return self.__password

    @property
    def read_books(self) -> List[Book]:
        return self.__read_books

    @property
    def reviews(self):
        return self.__reviews

    @property
    def pages_read(self) -> int:
        return self.__pages_read

    @property
    def reading_list(self):
        return self.__reading_list

    def add_reading_list(self, reading_list: ReadingCollection):
        self.__reading_list = reading_list

    def read_a_book(self, book: Book):
        if isinstance(book, Book):
            self.__read_books.append(book)
            if book.num_pages is not None:
                self.__pages_read += book.num_pages

    def add_review(self, review: Review):
        if isinstance(review, Review):
            # Review objects are in practice always considered different due to their timestamp.
            self.__reviews.append(review)

    def __repr__(self):
        return f'<User {self.user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user_name == self.user_name

    def __lt__(self, other):
        return self.user_name < other.user_name

    def __hash__(self):
        return hash(self.user_name)


class BooksInventory:

    def __init__(self):
        self.__books = {}
        self.__prices = {}
        self.__stock_count = {}

    def add_book(self, book: Book, price: int, nr_books_in_stock: int):
        self.__books[book.book_id] = book
        self.__prices[book.book_id] = price
        self.__stock_count[book.book_id] = nr_books_in_stock

    def remove_book(self, book_id: int):
        self.__books.pop(book_id)
        self.__prices.pop(book_id)
        self.__stock_count.pop(book_id)

    def find_book(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__books[book_id]
        return None

    def find_price(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__prices[book_id]
        return None

    def find_stock_count(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__stock_count[book_id]
        return None

    def search_book_by_title(self, book_title: str):
        for book_id in self.__books.keys():
            if self.__books[book_id].title == book_title:
                return self.__books[book_id]
        return None


class SearchMethod:

    def __init__(self, books, reviews):
        self.__dataset_of_books = books
        self.__dataset_of_reviews = reviews
        self.__found_items = []

    # returns all the found items by the search method
    @property
    def found_items(self):
        return self.__found_items

    # function will search for related tags.
    def search_by_tag(self, tag: str):
        self.__found_items = []
        for book in self.__dataset_of_books:
            if tag in book.tags:
                self.__found_items.append(book)

    # function will search for books relating to an author
    def search_by_author(self, author: Author):
        self.__found_items = []
        for book in self.__dataset_of_books:
            if author in set(book.authors):
                self.__found_items.append(book)

    # function will search for books within a given publication year range.
    def search_by_date_range(self, older_date: int, newer_date: int):
        self.__found_items = []
        for book in self.__dataset_of_books:
            if isinstance(book.release_year, int) and newer_date <= book.release_year <= older_date:
                self.__found_items.append(book)

    # function will return a set of books that relate to a given book.
    def search_related_books(self, book: Book):
        related_books = set()
        self.search_by_tag("read-it")
        book = self.found_items[0]
        for tag in book.tags:
            self.search_by_tag(tag)
            related_books = related_books.union(set(self.found_items))
        rec_books = random.sample(related_books, 19)
        rec_books.append(book)
        return reversed(rec_books)

    # deal with the implementation later
    def search_by_title(self, title: str):
        self.__found_items = []
        for book in self.__dataset_of_books:
            if book.title.lower().find(title.lower()) != -1:
                self.__found_items.append(book)

    def search_books_by_author(self, author: Author):
        self.__found_items = []
        for book in self.__dataset_of_books:
            if author in book.authors:
                self.__found_items.append(book)

    def search_books_by_publisher(self, publisher: Publisher):
        self.__found_items = []
        for book in self.__dataset_of_books:
            if publisher == book.publisher:
                self.__found_items.append(book)

    def search_reviews_by_book(self, book: Book):
        self.__found_items = []
        for review in self.__dataset_of_reviews:
            if review.book == book:
                self.__found_items.append(review)


class Tag:

    def __init__(self, tag):
        self.__tag = tag
        self.__tagged_books = []

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def tagged_books(self) -> str:
        return self.__tagged_books

    def tag_book(self, book):
        book.add_tag(self)
        self.__tagged_books.append(book)

    def __hash__(self):
        return hash(self.__tag)

    def __repr__(self):
        return f'{self.__tag}'

    def __eq__(self, other):
        return self.__tag == other.__tag
