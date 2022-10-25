import random
from datetime import date
from typing import List
from sqlalchemy import desc, asc, delete, select, func
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.adapters.abstractrepository import AbstractRepository
from library.adapters.orm import tags_table, books_authors_table, books_tags_table
from library.domain.model import Book, User, Author, Publisher, Review, Tag


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def close(self):
        self.__session.close()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def books(self) -> List[Book]:
        return self._session_cm.session.query(Book).all()

    def publishers(self) -> List[Publisher]:
        return self._session_cm.session.query(Publisher).all()

    def authors(self) -> List[Author]:
        return self._session_cm.session.query(Author).all()

    def reviews(self) -> List[Review]:
        return self._session_cm.session.query(Review).all()

    def tags(self):
        return self._session_cm.session.query(Tag).all()

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            try:
                scm.commit()
            except:
                scm.rollback()
            #print('added Review', review)

    def get_reviews(self, book: Book) -> List[Review]:
        print(f"BOOK_ID FOR REVIEWS {book.book_id}")
        reviews = None
        try:
            reviews = self._session_cm.session.query(Review).filter(Review._Review__book == book).all()

        except NoResultFound:
            pass
        return reviews

    def add_user(self, user: User):
        # print("adding", user)
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()
            #print("this piece of shit", self.get_user(user.user_name))


    def get_user(self, user_name: str):
        #print(f"Getting {user_name}")
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            #print("He aint there bitch")
            pass
        #print(f"Did i find the fucker {user_name}? is he {user}?")
        return user

    def get_user_by_id(self, user_id: str):
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_id == user_id).one()
            #print(f"FOUND THAT PIECE OF SHIT {user_id}")
        except NoResultFound:
            pass
        return user

    def add_book(self, book: Book):
        #print(f"adding book {book}")
        with self._session_cm as scm:
            scm.session.add(book)
            try:
                scm.commit()
            except:
                scm.rollback()

    def get_book(self, book_id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_id).one()
        except NoResultFound:
            pass
        return book

    def get_num_books(self) -> int:
        return self._session_cm.session.query(Book).count()

    def get_books_by_tag(self, tag: str) -> List[Book]:
        if isinstance(tag, Tag):
            tag = tag.tag
        books = None
        try:
            books = self._session_cm.session.query(Book).join(books_tags_table).join(Tag).filter(Tag._Tag__tag == tag).all()
        except NoResultFound:
            pass
        return books

    def get_books_by_author(self, author: Author) -> List[Book]:
        books = None
        try:
            #books = self._session_cm.session.query(books_authors_table).join(Author).join(Book).filter(Author._Author__unique_id == author.unique_id).all()
            books = self._session_cm.session.query(Book).join(books_authors_table).join(Author).filter(Author._Author__unique_id == author.unique_id).all()
        except NoResultFound:
            pass
        return books

    def get_books_by_title(self, title: str):
        books = None
        try:
            books = self._session_cm.session.query(Book).filter(Book._Book__title.like("%{}%".format(title))).all()
        except NoResultFound:
            pass
        return books

    def get_books_by_date_range(self, start: int, end: int) -> List[Book]:
        return self._session_cm.session.query(Book).filter(start <= Book._Book__release_year <= end)

    def get_related_books(self, book: Book) -> List[Book]:
        the_book = self.get_books_by_tag('read-it')[0]
        rec_books = random.sample(self.books(), 19)
        rec_books.append(the_book)
        return reversed(rec_books)



    def get_books_by_publisher(self, publisher: Publisher) -> List[Book]:
        books = None
        try:
            books = self._session_cm.session.query(Book).join(Publisher).filter(Publisher._Publisher__name == publisher.name).all()
        except NoResultFound:
            pass
        return books

    def add_author(self, author_input: Author):
        with self._session_cm as scm:
            scm.session.add(author_input)
            try:
                scm.commit()
            except:
                scm.rollback()

    def get_author(self, author_id) -> Author:
        author = None
        try:
            author = self._session_cm.session.query(Author).filter(Author._Author__unique_id == author_id).one()
        except NoResultFound:
            pass
        return author

    def get_authors_by_name(self, name):
        authors = None
        try:
            authors = self._session_cm.session.query(Author).filter(Author._Author__full_name.like("%{}%".format(name))).all()
        except NoResultFound:
            pass
        return authors

    def get_num_authors(self) -> int:
        return self._session_cm.session.query(Author).count()

    def add_publisher(self, publisher_input: Publisher):
        pass

    def get_publisher(self, publisher_name) -> Publisher:
        publisher = None
        try:
            publisher = self._session_cm.session.query(Publisher).filter(
                Publisher._Publisher__name == publisher_name).one()
        except NoResultFound:
            pass
        return publisher

    def get_num_publishers(self) -> int:
        return self._session_cm.session.query(Publisher).count()

    def get_users(self):
        return self._session_cm.session.query(User).all()

    def get_tag(self, tag):
        to_return = self._session_cm.session.query(Tag).filter(tags_table.c.tag == tag).one_or_none()
        if to_return:
            return to_return
        return Tag(tag)

    def get_tags_by_input(self, tag):
        tags = None
        try:
            tags = self._session_cm.session.query(Tag).filter(Tag._Tag__tag.like("%{}%".format(tag))).all()
            # books = self._session_cm.session.query(Book).filter().all()
        except NoResultFound:
            pass
        return tags

    # I have no idea how to not get multiple tags
    def add_tag(self, tag:str, book):
        check_tag = self.get_tag(tag)
        if check_tag is None:
            check_tag = Tag(tag)
        #print(f"adding {check_tag}")
        #book.add_tag(check_tag)
        with self._session_cm as scm:
            scm.session.merge(check_tag)
            scm.commit()

    def add_entry(self, entry):
        with self._session_cm as scm:
            scm.session.add(entry)
            scm.commit()

    def update_entry(self, entry):
        with self._session_cm as scm:
            scm.session.merge(entry)
            scm.commit()

    def get_entry(self, book_id):
        pass













