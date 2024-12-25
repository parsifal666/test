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
    def get_all_persons():
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM persons")
                return cursor.fetchall()

    @staticmethod
    def get_one_person(person_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM persons WHERE id = %s", (person_id,))
                return cursor.fetchone()
