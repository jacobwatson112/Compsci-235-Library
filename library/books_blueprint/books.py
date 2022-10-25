from flask import Blueprint, render_template, url_for, session, request
from random import randrange

from werkzeug.utils import redirect

from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Book, Review
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, RadioField
from wtforms.validators import NumberRange, DataRequired
from wtforms.widgets import TextArea
import library.adapters.abstractrepository as repo

book_blueprint = Blueprint('book_blueprint', __name__)


class ReviewForm(FlaskForm):
    review = StringField("Enter your review here", widget=TextArea(), default="Enter your review here")
    rating = RadioField('Enter your rating here', choices=[(0, 'zero'), (1, 'one'),
                                                           (2, 'two'), (3, 'three'),
                                                           (4, 'four'), (5, 'five')], default=0)
    submit = SubmitField("Submit")


class ReadingListForm(FlaskForm):
    pages_read = IntegerField('Enter your pages read', default=0)
    status = RadioField('Enter your progress here', choices=[("Plan to read", 'Plan to read'),
                                                             ("Reading", 'Reading'),
                                                             ("Completed", 'Completed')])
    submit = SubmitField("Submit")


class SearchFrom(FlaskForm):
    search = StringField("Search", [DataRequired()])
    submit = SubmitField("Submit")


@book_blueprint.route('/')
def home():
    # some_book = create_some_book()
    search_form = SearchFrom()
    books = []
    user = session.get("user")
    best_book = repo.repo_instance.get_book(0)

    for i in range(0, 3):
        try:
            books.append(repo.repo_instance.books()[randrange(len(repo.repo_instance.books()) - 1)])
        except TypeError:
            books.append(repo.repo_instance.books[randrange(len(repo.repo_instance.books) - 1)])
    print(books[0].authors)
    return render_template('home_page.html', best_book=best_book, books=books, user=user, search_form=search_form)


@book_blueprint.route('/list', methods=["POST", "GET"])
def list_books():
    search_form = SearchFrom()
    user = session.get('user')
    tag = request.args.get("tag")
    publisher = repo.repo_instance.get_publisher(request.args.get("publisher"))
    author = request.args.get("author")
    if search_form.validate_on_submit():
        searched = str(search_form.search.data)
        books = repo.repo_instance.get_books_by_title(searched)
        authors = repo.repo_instance.get_authors_by_name(searched)
        tags = repo.repo_instance.get_tags_by_input(searched)
        authors_books = []
        tag_books = set()
        for author in authors:
            authors_books = authors_books + repo.repo_instance.get_books_by_author(author)
        for tag in tags:
            tag_books = tag_books.union(set(repo.repo_instance.get_books_by_tag(tag)))
        return render_template("books.html", books=books, authors_books=authors_books, user=user, title=f"Books "
                                                                                                        f"titles "
                                                                                                        f"containing "
                                                                                                        f"'{search_form.search.data}'", search_form=search_form, searched=searched, tag_books=tag_books)
    if tag:
        return render_template("books.html", books=repo.repo_instance.get_books_by_tag(tag), user=user,
                               title=f"Books with the tag {tag}", search_form=search_form)
    if publisher:
        return render_template("books.html", books=repo.repo_instance.get_books_by_publisher(publisher), user=user,
                               title=f"Books published by {publisher.name}", search_form=search_form)
    if author:
        author = repo.repo_instance.get_author(int(author))
        return render_template("books.html", books=repo.repo_instance.get_books_by_author(author), user=user,
                               title=f"Books by {author.full_name}", search_form=search_form)
    try:
        books = repo.repo_instance.books()
    except TypeError:
        books = repo.repo_instance.books
    return render_template('books.html', books=books, user=user, title="All Books", search_form=search_form)


@book_blueprint.route('/selected_book', methods=["GET", "POST"])
def selected_book():
    search_form = SearchFrom()
    user = session.get('user')
    current_book = repo.repo_instance.get_book(request.args.get("book"))
    tags = current_book.tags
    current_review = ReviewForm()
    form = ReadingListForm()
    in_reading_list = None
    if user:
        user_reading_list = repo.repo_instance.get_user(user).reading_list
        for book_entry in user_reading_list.book_entries:
            if current_book == book_entry.book:
                in_reading_list = book_entry
                break
    reviews = reversed(repo.repo_instance.get_reviews(current_book))
    return render_template('single_book.html', book=current_book, user=user, currentReview=current_review,
                           reviews=reviews, in_reading_list=in_reading_list, readingList=form, tags=tags,
                           related=repo.repo_instance.get_related_books(current_book), search_form=search_form)

@book_blueprint.route('/review_book', methods=["GET", "POST"])
def review_book():
    review_form = ReviewForm(request.form)
    user = session.get('user')
    book = request.args.get("book")
    current_book = repo.repo_instance.get_book(book)
    if review_form.validate_on_submit():
        print("SUBMITTED REVIEW")
        reviewInput = review_form.review.data
        rating = int(review_form.rating.data)
        reviewSubmit = Review(repo.repo_instance.get_user(user), current_book, reviewInput, rating)
        repo.repo_instance.add_review(reviewSubmit)
    return redirect(f'/selected_book?book={book}')

@book_blueprint.route('/add_entry', methods=["GET", "POST"])
def add_entry():
    reading_list_form = ReadingListForm(request.form)
    user = session.get('user')
    book = request.args.get("book")
    current_book = repo.repo_instance.get_book(book)
    in_reading_list = None
    if user:
        user_reading_list = repo.repo_instance.get_user(user).reading_list
        for book_entry in user_reading_list.book_entries:
            if current_book == book_entry.book:
                in_reading_list = book_entry
                break
    if reading_list_form.validate_on_submit():
        print("SUBMITTED READINGLIST")
        pages = int(reading_list_form.pages_read.data)
        status = reading_list_form.status.data
        if in_reading_list:
            print("ALREADY IN READING LIST UPDATE!!!")
            in_reading_list.update_status(status)
            in_reading_list.update_pages_read(pages)
            repo.repo_instance.update_entry(in_reading_list)
        else:
            repo.repo_instance.get_user(user).reading_list.add_entry(current_book, status, pages)
    return redirect(f'/selected_book?book={book}')

@book_blueprint.route('/readinglist')
def readinglist():
    search_form = SearchFrom()
    user = session.get('user')
    books = repo.repo_instance.get_user(user).reading_list
    return render_template("reading_lists.html", user=session.get("user"), books=books.book_entries, search_form=search_form)
