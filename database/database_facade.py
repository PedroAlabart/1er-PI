from database.database_connection import get_session, get_engine
from database.table_creator import create_tables,drop_tables
from database.database_insertion import load_all



engine = get_engine()
session = get_session()

class DatabaseFacade:
    def __init__(self):
        self.engine = engine
        self.session = session

    def create_tables(self):
        create_tables(self.engine)

    def drop_tables(self):
        drop_tables(self.engine)

    def load_all_data(self):
        load_all()

        return self.session

    def run(self):
        """Run the entire database setup and data loading process."""
        self.drop_tables()
        self.create_tables()
        self.load_all_data()
        print("Database setup and data loading completed successfully.")

    def close_session(self):
        self.session.close()

db_fac = DatabaseFacade()
db_fac.run()