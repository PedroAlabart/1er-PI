from database.database_connection import get_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def test_database_connection():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            assert result == 1
    except SQLAlchemyError as e:
        assert False, f"Database connection failed: {e}"


engine = get_engine()
