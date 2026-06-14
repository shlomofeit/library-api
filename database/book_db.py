from db_connection import SetConnection
from library_logging import logger
from pydantic import BaseModel


class BookDB:
    def __init__(self, conn):
        self.conn = self.conn

    def create_book(self, data: dict):
        cursor = self.conn.cursor()
        query = "INSERT INTO books (title, author, gern, is_availble) VALUES (%s, %s, %s, TRUE)"

        try:
            cursor.execute(query, [data["title"], data["author"], data["gern"]])

        except Exception as e:
            logger.error("Adding the book failed. Error: %s", e)

        finally:
            cursor.close()

    def get_all_books(self):
        query = f"SELECT * FROM books"

    