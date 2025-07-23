from database_connection import get_engine
from sqlalchemy import text

engine = get_engine() # Gest engine from config.py

# The being statement is used to start a transaction block.
# Different to the engine.connect() method, which creates a connection to the database, and needs an explicit commit/rollback
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )