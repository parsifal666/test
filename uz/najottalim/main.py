import psycopg2
from AppProperties import *

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

class Person:
    @staticmethod
    def find_all(conn):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM persons")
            return cursor.fetchall()

    @staticmethod
    def find_by_id(conn, person_id):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM persons WHERE id = %s", (person_id,))
            return cursor.fetchone()

conn = get_db_connection()
