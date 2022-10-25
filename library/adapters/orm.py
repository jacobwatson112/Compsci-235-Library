from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, Boolean, text
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', String(32), unique=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('pages_read', Integer, server_default=text('0'), nullable=False)

)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True),
    Column('author', String(255), nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('publisher', String(255), nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024)),
    Column('publisher_id', ForeignKey('publishers.id')),
    Column('release_year', Integer),
    Column('ebook', Boolean),
    Column('num_pages', Integer),
    Column('image_url', String(1024)),
    Column('rating', Integer)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('book_id', ForeignKey('books.id')),
    Column('review', String(1024)),
    Column('rating', Integer),
    Column('timestamp', DateTime)
)

tags_table = Table(
    'tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tag', String(255))
)

books_authors_table = Table(
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book', ForeignKey('books.id')),
    Column('author', ForeignKey('authors.id'))
)
#not needed remove later
books_reviews_table = Table(
    'book_reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('review_id', ForeignKey('reviews.id'))
)

books_tags_table = Table(
    'book_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('tag_id', ForeignKey('tags.id'))
)

reading_lists_table = Table(
    'reading_lists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', ForeignKey('users.id')),
    Column('reading_list_name', String(255), nullable=False),
    # Column('book_entry_id', ForeignKey('book_entry.id'))
)

book_entry_table = Table(
    'book_entry', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reading_list', ForeignKey('reading_lists.id')),
    Column('book.id', ForeignKey('books.id')),
    Column('status', String(255), nullable=False),
    Column('pages_read', Integer, nullable=False)
)


def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        # didnt map the __read_books
        '_User__reviews': relationship(model.Review),
        '_User__pages_read': users_table.c.pages_read,
        '_User__reading_list': relationship(model.ReadingCollection, backref='_ReadingCollection__user', uselist=False)
    })

    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.id,
        '_Author__full_name': authors_table.c.author
        # didnt map the co-author stuff
    })

    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.publisher
    })

    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__publisher': relationship(model.Publisher),
        '_Book__authors': relationship(model.Author, secondary=books_authors_table),
        '_Book__release_year': books_table.c.release_year,
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__image_url': books_table.c.image_url,
        '_Book__rating': books_table.c.rating,
        '_Book__tags': relationship(model.Tag, secondary=books_tags_table, back_populates="_Tag__tagged_books")
    })

    mapper(model.ReadingCollection, reading_lists_table, properties={
        '_ReadingCollection__name': reading_lists_table.c.reading_list_name,
        '_ReadingCollection__book_entries': relationship(model.BookEntry, backref="_BookEntry__reading_list")
    })

    mapper(model.BookEntry, book_entry_table, properties={
        '_BookEntry__book': relationship(model.Book),
        '_BookEntry__status': book_entry_table.c.status,
        '_BookEntry__pages_read': book_entry_table.c.pages_read
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__book': relationship(model.Book),
        # '_Review__user': relationship(model.User),
        '_Review__review_text': reviews_table.c.review,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp
    })

    mapper(model.Tag, tags_table, properties={
        '_Tag__tag': tags_table.c.tag,
        '_Tag__tagged_books': relationship(model.Book, secondary=books_tags_table, back_populates="_Book__tags")
    })
