from database.db_connection import SetConnection
# from library_logging import logger

class BookDB:
    def __init__(self, conn):
        self.conn = conn

    def create_book(self, data: dict):
        cursor = self.conn.cursor(dictionary=True)
        query = "INSERT INTO books (title, author, genre, is_availble) VALUES (%s, %s, %s, TRUE)"

        try:
            cursor.execute(query, [data["title"], data["author"], data["gern"]])

        except Exception as e:
            # logger.error("Adding the book failed. Error: %s", e)
            pass

        finally:
            cursor.close()

    def get_all_books(self):
        cursor = self.conn.cursor(dictionary=True)
        query = f"SELECT * FROM books"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result

        finally:
            cursor.close()

    def get_book_by_id(self, id: int):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM books WHERE id = %S"

        try:
            cursor.execute(query, [id])
            result = cursor.fetchall()
            return result if result else None

        finally:
            cursor.close()

    def update_book(self, id: int, data: dict):
        cursor = self.conn.cursor(dictionary=True)
        query_keys = ", ".join(f"{f} = %s" for f in data)
        query = f"UPDATE books SET {query_keys} WHERE id = %s"

        try:
            cursor.execute(query, [data.values()] + [id])

        except Exception as e:
            # logger.error("Updating the book failed. Error: %s", e)
            pass

        finally:
            cursor.close()


    def set_available(self, id, val, member_id):
        cursor = self.conn.cursor(dictionary=True)
        query = "UPDATE books SET (is_availble = %s, borrowed_by_member_id = %s) WHERE id = %s"

        try:
            cursor.execute(query, [val, member_id, id])
            result = cursor.fetchall()
            return result if result else None

        finally:
            cursor.close()


    def count_total_books(self):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) FROM books"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result if result else None

        finally:
            cursor.close()

    
    def count_available_books(self):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) FROM books WHERE is_availble = TRUE"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result if result else None

        finally:
            cursor.close()


    def count_borrowed_books(self):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) FROM books WHERE borrowed_by_member_id IS NOT NULL"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result if result else None

        finally:
            cursor.close()


    def count_by_genre(self):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT genre, COUNT(*) FROM books GROUP BY genre"

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            return result if result else None

        finally:
            cursor.close()


    def count_active_borrows_by_member(self, member_id: int):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) FROM books WHERE borrowed_by_member_id = %S"

        try:
            cursor.execute(query, [member_id])
            result = cursor.fetchall()
            
            return result if result else None

        finally:
            cursor.close()