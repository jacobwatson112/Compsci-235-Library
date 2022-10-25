import json
from typing import List

from library import MemoryRepository
from library.adapters.databaserepository import SqlAlchemyRepository
from library.domain.model import Publisher, Author, Book, SearchMethod, Review, Tag
import library.adapters.abstractrepository as repo

class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str, reviews_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__reviews_file_name = reviews_file_name
        # self.__dataset_of_books = []
        # self.__search = SearchMethod(self.__dataset_of_books)

    # @property
    # def search(self):
    #     return self.__search

    # @property
    # def dataset_of_books(self) -> List[Book]:
    #     return self.__dataset_of_books

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json

    def read_reviews_file(self) -> list:
        reviews_json = []
        with open(self.__reviews_file_name, encoding='UTF-8') as reviews_jsonfile:
            for line in reviews_jsonfile:
                review_entry = json.loads(line)
                reviews_json.append(review_entry)
        return reviews_json

    def read_json_files(self, repo=None):
        if repo is None:
            self.read_json_files_sql()
        elif isinstance(repo, MemoryRepository):
            self.read_json_files_mem(repo)

    def read_json_files_sql(self):
        # print("READING BITCH")
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()
        reviews_json = self.read_reviews_file()
        for book_json in books_json:
            publisher = repo.repo_instance.get_publisher(book_json['publisher'])
            if not publisher:
                publisher = Publisher(book_json['publisher'])
                repo.repo_instance.add_publisher(publisher)
            book_instance = Book(int(book_json['book_id']), book_json['title'])
            book_instance.publisher = publisher
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])
            if book_json['average_rating'] != "":
                book_instance.rating = float(book_json["average_rating"])
            if book_json["image_url"] != "":
                book_instance.image_url = book_json["image_url"]
            if book_json['popular_shelves'] != "":
                for tag in book_json['popular_shelves']:
                    #print("CHECKING TAG")
                    #repo.repo_instance.add_tag(tag['name'], book_instance)
                    book_instance.add_tag(repo.repo_instance.get_tag(tag['name']))

                # extract the author ids:
            list_of_authors_ids = book_json['authors']
            for author_id in list_of_authors_ids:
                numerical_id = int(author_id['author_id'])
                # We assume book authors are available in the authors file,
                # otherwise more complex handling is required.
                author_name = None
                for author_json in authors_json:
                    if int(author_json['author_id']) == numerical_id:
                        author_name = author_json['name']
                author = repo.repo_instance.get_author(numerical_id)
                if not author:
                    author = Author(numerical_id, author_name)
                    repo.repo_instance.add_author(author)
                book_instance.add_author(author)
            repo.repo_instance.add_book(book_instance)

        for review in reviews_json:
            book_instance = repo.repo_instance.get_book(review["book_id"])
            user = repo.repo_instance.get_user_by_id(review["user_id"])
            json_review = Review(user,book_instance, review["review_text"], review['rating'])
            #print(json_review.review_text)
            if user:
                user.add_review(json_review)
            repo.repo_instance.add_review(json_review)

    def read_json_files_mem(self, repo):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()
        reviews_json = self.read_reviews_file()
        for book_json in books_json:
            publisher = repo.get_publisher(book_json['publisher'])
            if not publisher:
                publisher = Publisher(book_json['publisher'])
                repo.add_publisher(publisher)
            book_instance = Book(int(book_json['book_id']), book_json['title'])
            book_instance.publisher = publisher
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])
            if book_json['average_rating'] != "":
                book_instance.rating = float(book_json["average_rating"])
            if book_json["image_url"] != "":
                book_instance.image_url = book_json["image_url"]
            if book_json['popular_shelves'] != "":
                temp_tags = set()
                for tag in book_json['popular_shelves']:
                    temp_tags.add(tag['name'])
                book_instance.tags = temp_tags
                # extract the author ids:
            list_of_authors_ids = book_json['authors']
            for author_id in list_of_authors_ids:
                numerical_id = int(author_id['author_id'])
                # We assume book authors are available in the authors file,
                # otherwise more complex handling is required.
                author_name = None
                for author_json in authors_json:
                    if int(author_json['author_id']) == numerical_id:
                        author_name = author_json['name']
                author = repo.get_author(numerical_id)
                if not author:
                    author = Author(numerical_id, author_name)
                    repo.add_author(author)
                book_instance.add_author(author)
            repo.add_book(book_instance)

        for review in reviews_json:
            book_instance = repo.get_book(review["book_id"])
            json_review = Review(None, book_instance, review["review_text"], review['rating'])
            user = repo.get_user_by_id(review["user_id"])
            if user:
                user.add_review(json_review)
            repo.add_review(json_review)



