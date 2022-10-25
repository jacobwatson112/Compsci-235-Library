from pathlib import Path

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from library import BooksJSONReader
from library.adapters import databaserepository, abstractrepository
from library.adapters.abstractrepository import add_users, populate
from library.adapters.orm import metadata, map_model_to_tables

from utils import get_project_root

TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "library" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///not-test-devesb-base.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    abstractrepository.repo_instance = databaserepository.SqlAlchemyRepository(session_factory)
    database_mode = True
    abstractrepository.populate()
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def populate150books():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    abstractrepository.repo_instance = databaserepository.SqlAlchemyRepository(session_factory)
    database_mode = True

    books_file_name = '150.json'
    authors_file_name = 'output.json'
    reviews_file_name = "reviews.json"

    # we use a method from a utils file in the root folder to figure out the root
    # this way testing code is always finding the right path to the data files
    root_folder = get_project_root()
    data_folder = Path("library/adapters/data")
    path_to_books_file = str(root_folder / data_folder / books_file_name)
    path_to_authors_file = str(root_folder / data_folder / authors_file_name)
    path_to_reviews_file = str(root_folder / data_folder / reviews_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file, path_to_reviews_file)
    reader.read_json_files()

    users_file_name = "users.txt"
    root_folder = get_project_root()
    data_folder = Path("library/adapters/data")
    path_to_users_file = str(root_folder / data_folder / users_file_name)

    abstractrepository.add_users(path_to_users_file)
    abstractrepository.populate()
    yield session_factory
    metadata.drop_all(engine)


@pytest.fixture
def populate20books():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    abstractrepository.repo_instance = databaserepository.SqlAlchemyRepository(session_factory)
    database_mode = True

    books_file_name = 'comic_books_excerpt.json'
    authors_file_name = 'book_authors_excerpt.json'
    reviews_file_name = "reviews.json"

    # we use a method from a utils file in the root folder to figure out the root
    # this way testing code is always finding the right path to the data files
    root_folder = get_project_root()
    data_folder = Path("library/adapters/data")
    path_to_books_file = str(root_folder / data_folder / books_file_name)
    path_to_authors_file = str(root_folder / data_folder / authors_file_name)
    path_to_reviews_file = str(root_folder / data_folder / reviews_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file, path_to_reviews_file)
    reader.read_json_files()

    users_file_name = "users.txt"
    root_folder = get_project_root()
    data_folder = Path("library/adapters/data")
    path_to_users_file = str(root_folder / data_folder / users_file_name)

    abstractrepository.add_users(path_to_users_file)
    abstractrepository.populate()
    yield session_factory
    metadata.drop_all(engine)



@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)