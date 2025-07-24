# SoyHenry - Accenture PI Project

This repository contains all the code, notebooks, and documentation for the Data Engineering and Analytics project.

---

## 🔗 Connection Structure

- **database_connection.py**: Handles database connection using SQLAlchemy ORM.
- **database_insertion.py**: Functions to insert data from CSV files into the database.
- **models.py**: SQLAlchemy models representing the database tables.
- **table_creator.py**: Functions to create tables in the database.
- **database_facade.py**: Centralizes database operations for easier usage.

More details about the database module can be found in [`database/README.md`](database/README.md).

---

## 🧪 Tests Structure
- **test_database_connection.py**: Tests the database connection.

---

## 📈 Avances Structure

### Avance 1

- **1er_avance_EDA.ipynb & EDA_helper.py**  
  Data cleaning and exploratory analysis.  
  Checks for duplicates, foreign key integrity, price consistency, and more.

- **preguntas_de_negocio.ipynb**  
  Answers business questions, highlights questions that cannot be answered with the current data, and proposes new metrics.

### Avance 2

- **2do_avance.ipynb**  
  Theoretical data modeling, including schema design, normalization, Slowly Changing Dimensions (SCD) and dimensional modeling concepts.

### Avance 3 (in progress)

La carpeta Ecommerce cuenta con la info de dbt.
Tiene modelos de las tablas
Y un modelo llamado agg_user_expenses que muestra a los usuarios ordenados por gastos total y tambien muestra su promedio de gastos

---

## 🚀 How to Use

1. Run pip install `requirements.txt`
2. Configure your database connection in `config.py`.
3. Run `1er_avance_EDA.py` to create and populate all tables.
4. Explore and analyze the data using the provided notebooks.