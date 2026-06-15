from database.db_connection import SetConnection
from library_logging import logger

class BookDB:

    SetConnection.connect()
    logger.debug("Starting BookDB...")
    conn = SetConnection.get_connection()

    @classmethod
    def create_book(cls, data: dict):
        logger.info("the create book function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "INSERT INTO books (title, author, genre, is_availble) VALUES (%s, %s, %s, TRUE)"
        values = [data["title"], data["author"], data["genre"]]

        try:
            logger.debug("query: %s, data: %s", query, values)
            cursor.execute(query, values)
            cls.conn.commit()
            logger.info("the book was created successfully")

            return {"message": f"book created successfully. title: {data["title"]}, author: {data['author']}, genre: {data['genre']}"}

        except Exception as e:
            logger.exception("error while creating a book. Error: %s", e)

            return {"message": f"error while creating a book: {e}"}

        finally:
            cursor.close()
            logger.info("the cursor closed")
    
    
    @classmethod
    def get_all_books(cls):
        logger.info("the get all books function was called")
        cursor = cls.conn.cursor(dictionary=True)
        query = f"SELECT * FROM books"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logger.info("all books from the table were successfully retrieved")

            if len(result) < 1:
                logger.warning("no books in the table")

            return result

        finally:
            cursor.close()
            logger.info("the cursor closed")


    @classmethod
    def get_book_by_id(cls, id: str):
        logger.info("the get book by id function was called")
        cursor = cls.conn.cursor(dictionary=True)
        query = "SELECT * FROM books WHERE id = %s"

        try:
            logger.debug("query: %s, values: %s", query, id)
            cursor.execute(query, [id])
            result = cursor.fetchall()

            logger.info("book by id from the table were successfully retrieved")

            if not result:
                logger.warning("Book with ID: %s does not exist", id)
                return

            return result

        finally:
            cursor.close()
            logger.info("the cursor closed")


    @classmethod
    def update_book(cls, id, data: dict):
        logger.info("the update book function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query_keys = ", ".join(f"{f} = %s" for f in data)
        query = f"UPDATE books SET {query_keys} WHERE id = %s"
        values = list(data.values()) + [id]

        try:
            logger.debug("query: %s, data: %s", query, values)
            cursor.execute(query, values)
            cls.conn.commit()
            
            result = cursor.rowcount
            logger.info("the book was updated successfully. number of details updated: %s", result)

                
            return result

        except Exception as e:
            logger.error("Updating the book failed. Error: %s", e)
            
            return {"message": f"error while updating a book: {e}"}

        finally:
            cursor.close()
            logger.info("the cursor closed")


    @classmethod
    def set_available(cls, id, val, member_id):
        logger.info("the set availble function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "UPDATE books SET is_availble = %s, borrowed_by_member_id = %s WHERE id = %s"
        values = [val, member_id, id]

        try:
            logger.debug("query: %s, data: %s", query, values)
            
            cursor.execute(query, values)
            cls.conn.commit()
            result = cursor.rowcount
            logger.info("the bavailblity was updated successfully to %s", result)

            return result if result else None

        finally:
            cursor.close()
            logger.info("the cursor closed")


    @classmethod
    def count_total_books(cls):
        logger.info("the function was called")

        cursor = cls.conn.cursor()
        query = "SELECT COUNT(*) FROM books"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logger.info("the amount of books in the table is: %s", result)
            
            return result if result else None

        finally:
            cursor.close()
            logger.info("the cursor closed")

    
    @classmethod
    def count_available_books(cls):
        logger.info("the function was called")

        cursor = cls.conn.cursor()
        query = "SELECT COUNT(*) FROM books WHERE is_availble = TRUE"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logger.info("the amount of availble books in the table is: %s", result)
            
            return result if result else None

        finally:
            cursor.close()
            logger.info("the cursor closed")


    @classmethod
    def count_borrowed_books(cls):
        logger.info("the function was called")

        cursor = cls.conn.cursor()
        query = "SELECT COUNT(*) FROM books WHERE borrowed_by_member_id IS NOT NULL"

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            logger.info("the amount of borrowed books in the table is: %s", result)
            
            return result if result else None

        finally:
            cursor.close()
            logger.info("the cursor closed")


    @classmethod
    def count_by_genre(cls):
        logger.info("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "SELECT genre, COUNT(*) AS COUNT FROM books GROUP BY genre"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logger.info("the amount of genre books in the table is: %s", result)

            return result if result else None

        finally:
            cursor.close()
            logger.info("the cursor closed")


    @classmethod
    def count_active_borrows_by_member(cls, member_id: int):
        logger.info("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) AS COUNT FROM books WHERE borrowed_by_member_id = %s"

        try:
            cursor.execute(query, [member_id])
            result = cursor.fetchall()
            logger.info("the amount of active borrows by member in the table is: %s", result)
            
            return result[0] if result else None

        finally:
            cursor.close()
            logger.info("the cursor closed")