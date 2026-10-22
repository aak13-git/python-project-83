import psycopg2
from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, database_url):
        self.database_url = database_url

    def get_connection(self):
        return psycopg2.connect(self.database_url)

    def find_url(self, name):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT id, name, created_at FROM urls WHERE name = %s;", (name,))
                return cursor.fetchone()

    def find_url_by_id(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT id, name, created_at FROM urls WHERE id = %s;", (url_id,))
                return cursor.fetchone()

    def add_url(self, name):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id;",
                    (name,)
                )
                new_id = cursor.fetchone()[0]
                conn.commit()
                return new_id

    def get_all(self):
        query = """
            SELECT DISTINCT ON (urls.id) 
                   urls.id, 
                   urls.name, 
                   url_checks.created_at, 
                   url_checks.status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC, url_checks.id DESC;
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
