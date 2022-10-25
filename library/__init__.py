"""Initialize Flask app."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from flask import Flask, render_template
import library.adapters.abstractrepository as repo
from library.adapters.abstractrepository import add_users, populate
from library.adapters.repository import MemoryRepository
from library.adapters import databaserepository
from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.orm import map_model_to_tables, metadata


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    reader = BooksJSONReader("library/adapters/data/150.json",
                             "library/adapters/data/output.json",
                             "library/adapters/data/reviews.json")
    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = MemoryRepository()
        add_users("library/adapters/data/users.txt")
        reader.read_json_files(repo.repo_instance)
        repo.populate()
    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        #print("database", database_echo)
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = databaserepository.SqlAlchemyRepository(session_factory)
        if app.config["TESTING"] == "True" or len(database_engine.table_names()) == 0:
            #print("Repopulating Database")
            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())
            map_model_to_tables()

            add_users("library/adapters/data/users.txt")
            populate()
            reader.read_json_files()
            print("Finished populating")
        else:
            map_model_to_tables()


    with app.app_context():
        from .books_blueprint import books
        from .user_blueprint import user
        app.register_blueprint(books.book_blueprint)
        app.register_blueprint(user.user_blueprint)
    return app

# library/adapters/data/book_authors_excerpt.json
# library/adapters/data/comic_books_excerpt.json
# library/adapters/data/extra_data/comic_excerpt.json
# library/adapters/data/extra_data/output.json
