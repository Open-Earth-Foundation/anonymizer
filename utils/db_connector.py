import os
import psycopg

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


def connect_to_db():
    # Database connection parameters
    conn_params = {
        "host": DATABASE_HOST,
        "port": DATABASE_PORT,
        "dbname": DATABASE_NAME,
        "user": DATABASE_USER,
        "password": DATABASE_PASSWORD,
    }

    try:
        # Establish a connection to the database
        return psycopg.connect(**conn_params)

    except psycopg.Error as e:
        print(f"Database error: {e}")
        return []
