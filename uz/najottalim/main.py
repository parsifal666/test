import psycopg2


class Descriptor:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    def validate(self, value):
        pass


class StringField(Descriptor):
    def __init__(self, name=None, max_length=255):
        super().__init__(name)
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, str) or len(value) > self.max_length:
            raise ValueError(f"{self.name} must be a string with max length {self.max_length}.")


class IntegerField(Descriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"{self.name} must be an integer.")


class User:
    id = IntegerField()
    name = StringField(max_length=100)
    email = StringField(max_length=150)

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def save_to_db(self, connection):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (id, name, email) VALUES (%s, %s, %s) "
                "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, email = EXCLUDED.email;",
                (self.id, self.name, self.email)
            )
        connection.commit()


def setup_database(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(150) UNIQUE
            );
        """)
    connection.commit()


if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password="sriv2008",
        host="localhost",
        port="5432"
    )
    setup_database(conn)
    User(id=2, name="sanjar", email="sanjar@example.com").save_to_db(conn)
    conn.close()
