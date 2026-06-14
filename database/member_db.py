from db_connection import SetConnection
from library_logging import logger
from pydantic import BaseModel


class MemberDB:
    def __init__(self, conn):
        self.conn = self.conn

    def create_member(self, data: dict):
        cursor = self.conn.cursor()
        query = "INSERT INTO members (name, email, is_availble) VALUES (%s, %s, TRUE)"

        try:
            cursor.execute(query, [data["name"], data["email"]])

        except Exception as e:
            logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()