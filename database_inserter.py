from database_connection import get_engine
from sqlalchemy import text

engine = get_engine()





def insert_values(table: str, values:list[tuple]):
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            values,
        )
        conn.commit()