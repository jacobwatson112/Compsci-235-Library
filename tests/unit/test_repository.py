from pathlib import Path
import pytest

from utils import get_project_root

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import MemoryRepository
from library.adapters.abstractrepository import add_users
import library.adapters.abstractrepository as repo

@pytest.fixture
def create_books_150_books():
    books_file_name = '150.json'
    authors_file_name = 'output.json'
    reviews_file_name = "reviews.json"
    users_file_name = "users.txt"
    repo.repo_instance = MemoryRepository()
    # we use a method from a utils file in the root folder to figure out the root
    # this way testing code is always finding the right path to the data files
    root_folder = get_project_root()
    data_folder = Path("library/adapters/data")
    path_to_books_file = str(root_folder / data_folder / books_file_name)
    path_to_authors_file = str(root_folder / data_folder / authors_file_name)
    path_to_reviews_file = str(root_folder / data_folder / reviews_file_name)
    path_to_users_file = str(root_folder / data_folder / users_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file, path_to_reviews_file)
    add_users(path_to_users_file)
    reader.read_json_files(repo.repo_instance)




class TestRepository:

    # def test_getters(self, create_books_150_books):
    #     temp = create_books_150_books
    #     assert len(repo.repo_instance.books) == 153
    #     assert repo.repo_instance.get_num_authors() == 331
    #     assert len(repo.repo_instance.reviews) == 546
    #     book = repo.repo_instance.get_book(17277791)
    #     assert str(book) == "<Book X-Force: Phalanx Covenant, book id = 17277791>"
    #     assert len(repo.repo_instance.get_related_books(book)) == 20
    #     assert len(repo.repo_instance.get_books_by_date_range(2015,2015)) == 15
    #     assert len(repo.repo_instance.get_books_by_tag("magic")) == 9
    #     assert str(repo.repo_instance.get_user("samuel")) == "<User samuel>"
    #     print(repo.repo_instance.publishers)
    #     assert repo.repo_instance.get_num_publishers() == 112
    #     publisher = repo.repo_instance.get_publisher("Andrews McMeel Publishing")
    #     assert str(publisher) == "<Publisher Andrews McMeel Publishing>"
    #     assert len(repo.repo_instance.get_books_by_publisher(publisher)) == 2

    def test_books_entered(self, create_books_150_books):
        create_books_150_books
        assert len(repo.repo_instance.books) == 153

    def test_authors_entered(self, create_books_150_books):
        create_books_150_books
        assert repo.repo_instance.get_num_authors() == 331
        pass

    def test_reviews_entered(self, create_books_150_books):
        create_books_150_books
        assert len(repo.repo_instance.reviews) == 548
        pass

    def test_publishers_entered(self, create_books_150_books):
        assert repo.repo_instance.get_num_publishers() == 112
        create_books_150_books
        pass

    def test_get_user(self, create_books_150_books):
        create_books_150_books
        assert str(repo.repo_instance.get_user("samuel")) == "<User samuel>"
        pass

    def test_get_publisher(self,create_books_150_books):
        create_books_150_books
        publisher = repo.repo_instance.get_publisher("Andrews McMeel Publishing")
        assert str(publisher) == "<Publisher Andrews McMeel Publishing>"
        pass

    def test_get_author(self, create_books_150_books):
        create_books_150_books
        author = repo.repo_instance.get_author(12948)
        assert str(author) == "<Author Rumiko Takahashi, author id = 12948>"

    def test_get_authors_by_name(self, create_books_150_books):
        create_books_150_books
        authors = repo.repo_instance.get_authors_by_name("Tak")
        print(authors)
        assert len(authors) == 3

    def test_get_tags_by_input(self, create_books_150_books):
        create_books_150_books
        tags = repo.repo_instance.get_tags_by_input("magic")
        print(tags)
        assert len(tags) == 10

    def test_search_by_title(self, create_books_150_books):
        create_books_150_books
        assert len(repo.repo_instance.get_books_by_title("The")) == 40
        pass