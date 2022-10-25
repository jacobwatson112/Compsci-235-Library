from datetime import date, datetime

import pytest

import library.adapters.abstractrepository as repo
from library.adapters.databaserepository import SqlAlchemyRepository
from library.domain.model import Publisher, Author, Book, ReadingCollection, BookEntry, Review, User, BooksInventory, SearchMethod, Tag


def test_repository_can_add_a_user(populate150books):
    populate150books()

    user = User('dave', '123456789')
    repo.repo_instance.add_user(user)

    repo.repo_instance.add_user(User('Martin', '123456789'))

    user2 = repo.repo_instance.get_user('dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(populate150books):
    populate150books()

    user = repo.repo_instance.get_user('caleb')
    assert user == User('caleb', 'admin456')


def test_repository_does_not_retrieve_a_non_existent_user(populate150books):
    populate150books()

    user = repo.repo_instance.get_user('Notcaleb')
    assert user is None

def test_repository_can_retrieve_book_count(populate150books):
    populate150books()

    number_of_articles = repo.repo_instance.get_num_books()

    # dont test this lmao
    # Check that the query returned 153 books.
    assert number_of_articles == 153


def test_repository_can_add_book(populate20books):
    populate20books()

    book = Book(
        69,
        "what does the meth function do"
    )
    repo.repo_instance.add_book(book)

    assert repo.repo_instance.get_book(69) == book


def test_repository_can_retrieve_book(populate150books):
    populate150books()

    book = repo.repo_instance.get_book(0)

    # Check that the book has the expected title.
    assert book.title == 'Ninja: Get Good, My Ultimate Guide to Gaming'

    # Check that the book has this review as expected.
    comment_one = repo.repo_instance.get_reviews(book)

    assert comment_one[0].review_text == "Absolutely poggers, never missed a shot in my lyfe after reading this, ty ty"


def test_repository_does_not_retrieve_a_non_existent_book(populate20books):
    populate20books()

    book = repo.repo_instance.get_book(21)
    assert book is None


def test_repository_can_retrieve_books_by_something(populate150books):
    populate150books()

    tags = repo.repo_instance.get_books_by_tag('yaoi')

    # Check that the query returned 5 books.
    assert len(tags) == 5

    authors = repo.repo_instance.get_authors_by_name('Xi Jinping')

    # Check that the query returned 1 book.
    assert len(authors) == 1


    publisher = repo.repo_instance.get_publisher('Marvel')
    books = repo.repo_instance.get_books_by_publisher(publisher)

    # Check that the query returned 15 books.
    assert len(books) == 15

    # date = repo.repo_instance.get_books_by_date_range(2019, 2019)
    #
    # # Check that the query returned 15 books.
    # assert len(date) == 1


# the code below is stolen from brother zAM


def test_construction(populate150books):
        populate150books()

        publisher1 = Publisher("Avatar Press")
        assert str(publisher1) == "<Publisher Avatar Press>"

        publisher2 = Publisher("  ")
        assert str(publisher2) == "<Publisher N/A>"

        publisher3 = Publisher("  DC Comics ")
        assert str(publisher3) == "<Publisher DC Comics>"

        publisher4 = Publisher(42)
        assert str(publisher4) == "<Publisher N/A>"

def test_comparison(populate150books):
    populate150books()

    publisher1 = Publisher("Avatar Press")
    publisher2 = Publisher("DC Comics")
    publisher3 = Publisher("Avatar Press")
    publisher4 = Publisher("")
    assert str(publisher4) == "<Publisher N/A>"
    assert publisher1 == publisher3
    assert publisher1 != publisher2
    assert publisher3 != publisher2
    assert publisher2 != publisher3


def test_authors_entered(populate150books):
    populate150books()
    assert repo.repo_instance.get_num_authors() == 331
    pass

def test_reviews_entered(populate150books):
    populate150books()
    assert len(repo.repo_instance.reviews()) == 548
    pass

def test_publishers_entered(populate150books):
    populate150books()

    assert repo.repo_instance.get_num_publishers() == 112
    pass

def test_get_user(populate150books):
    populate150books()
    assert str(repo.repo_instance.get_user("samuel")) == "<User samuel>"
    pass

def test_get_publisher(populate150books):
    populate150books()
    publisher = repo.repo_instance.get_publisher("Andrews McMeel Publishing")
    assert str(publisher) == "<Publisher Andrews McMeel Publishing>"
    pass

def test_get_author(populate150books):
    populate150books()
    author = repo.repo_instance.get_author(12948)
    assert str(author) == "<Author Rumiko Takahashi, author id = 12948>"

def test_get_authors_by_name(populate150books):
    populate150books()
    authors = repo.repo_instance.get_authors_by_name("Tak")
    print(authors)
    assert len(authors) == 3

def test_get_tags_by_input(populate150books):
    populate150books()
    tags = repo.repo_instance.get_tags_by_input("magic")
    print(tags)
    assert len(tags) == 10

def test_search_by_title(populate150books):
    populate150books()
    assert len(repo.repo_instance.get_books_by_title("The")) == 40
    pass