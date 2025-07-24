from database.models import Base
from sqlalchemy.engine import Engine


def create_tables(engine: Engine):
    """Creates tables in the database using SQLAlchemy."""
    Base.metadata.create_all(engine)

def drop_tables(engine: Engine):
    """Drops all tables in the database using SQLAlchemy."""
    Base.metadata.drop_all(engine)
