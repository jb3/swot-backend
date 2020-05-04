"""Utility functions for the database."""
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from backend.config import CONFIG


def connect() -> (sqlalchemy.engine.Engine, sqlalchemy.MetaData):
    """
    Return a connection to the database.

    Required parameters for connection are specified within the config file.
    """
    # When we use SQLite we don't need any of the PostgreSQL parameters
    if not CONFIG.db.use_sqlite:
        url = "postgresql://{}:{}@{}:{}/{}"
        url = url.format(
            CONFIG.db.username,
            CONFIG.db.password,
            CONFIG.db.host,
            CONFIG.db.port,
            CONFIG.db.database,
        )

        # Create a connection to PostgreSQL
        con = sqlalchemy.create_engine(url, client_encoding="utf-8")
    else:
        url = "sqlite:///swot.db"

        # Create a connection to SQLite
        con = sqlalchemy.create_engine(url)

    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


# Create a class which will allow for reuse of the database connection
Session = sessionmaker(bind=connect()[0])
