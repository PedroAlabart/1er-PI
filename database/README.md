# Database Module

This folder contains utilities for managing the database in the SoyHenry - Accenture PI project.

## Files

- **database_connection.py**: Handles the creation of the SQLAlchemy engine and session.
- **database_facade.py**: Orchestrates the main database operations (connect, create tables, insert data).
- **models.py**: Contains the ORM models for the tables, based on the DDL query from the shared drive.
- **table_creator.py**: Functions to create tables in the database using the models.
- **database_insertion.py**: Functions to insert data into the tables from CSV files.

## Data Source

The data for the tables is sourced from CSV files located in the shared folder.

## Insert Module

This module is built around an abstract class called `CSVLoader`, which contains the core logic to map CSV files to their corresponding database tables.

Based on this class, specific subclasses such as `UsuarioLoader`, `ProductoLoader`, etc., are created to handle particular table mappings and loading logic.


## Usage Flow

The recommended workflow is:

1. **Connect to the database** using `database_connection.py`.
2. **Create tables** using the classes defined in `models.py` and the functions in `table_creator.py`.
3. **Insert data** into the tables using the functions in `database_insertion.py` and the CSV files.

All these steps can be orchestrated from `database_facade.py` for a streamlined


