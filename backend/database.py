"""Utility functions for the database."""
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from backend.config import CONFIG


def connect() -> (sqlalchemy.engine.Engine, sqlalchemy.MetaData):
    """
    Return a connection to the database.

    Required parameters for connection are specified within the config file.
    """
    url = "postgresql://{}:{}@{}:{}/{}"
    url = url.format(CONFIG.db.username, CONFIG.db.password,
                     CONFIG.db.host, CONFIG.db.port, CONFIG.db.database)

    con = sqlalchemy.create_engine(url, client_encoding="utf-8")

    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


Session = sessionmaker(bind=connect()[0])
