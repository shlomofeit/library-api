from database.db_connection import SetConnection
from mysql import connector
from library_logging import logger


class MemberDB:

    SetConnection.connect()
    logger.debug("Starting MemberDB...")
    conn = SetConnection.get_connection()

    @classmethod
    def create_member(cls, data: dict):
        logger.debug("the function was called")

        cursor = cls.conn.cursor()
        query = "INSERT INTO members (name, email, is_active) VALUES (%s, %s, TRUE)"

        try:
            logger.debug("query: %s, data: %s", query, data["name"], data["email"])

            cursor.execute(query, [data["name"], data["email"]])
            cls.conn.commit()

        except Exception:
            logger.error("Adding the member failed. Error: %s", e)
            raise connector.errors.IntegrityError

        finally:
            cursor.close()


    @classmethod
    def get_all_members(cls):
        logger.debug("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "SELECT * FROM members"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logger.info("all members from the table were successfully retrieved")

            if len(result) < 1:
                logger.warning("no members in the table")

            return result if result else None

        except Exception as e:
            logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()    


    @classmethod
    def get_member_by_id(cls, id):
        logger.debug("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "SELECT * FROM members WHERE id = %s"

        try:
            logger.debug("query: %s, data: %s", query, id)

            cursor.execute(query, [id])
            result = cursor.fetchall()

            return result if result else None

        except Exception as e:
            logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()

    @classmethod
    def update_member(cls, id: int, data: dict):
        logger.debug("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query_keys = ", ".join(f"{f} = %s" for f in data)
        query = f"UPDATE members SET {query_keys} WHERE id = %s"
        values = list(data.values()) + [id]

        try:
            logger.debug("query: %s, data: %s", query, values)

            cursor.execute(query, values)
            cls.conn.commit()

        except Exception as e:
            logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()


    @classmethod
    def deactivate_member(cls, id: int):
        logger.debug("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "UPDATE members SET is_active = FALSE WHERE id = %s"

        try:
            logger.info("the user (%s) became deactivate successfully", id)

            cursor.execute(query, [id])
            cls.conn.commit()

        except Exception as e:
            logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()


    @classmethod
    def activate_member(cls, id: int):
        logger.debug("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "UPDATE members SET is_active = TRUE WHERE id = %s"

        try:
            logger.info("the user (%s) became activate successfully", id)
            cursor.execute(query, [id])
            cls.conn.commit()

        except Exception as e:
            logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()


    @classmethod
    def increment_borrows(cls, member_id: id):
        logger.debug("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "UPDATE members SET total_borrows=total_borrows+1 WHERE id = %s"

        try:
            logger.info("the user's total amount increased by 1")

            cursor.execute(query, [member_id])
            cls.conn.commit()

            result = cursor.rowcount

            return result

        finally:
            cursor.close()


    @classmethod
    def count_active_members(cls):
        logger.debug("the function was called")

        cursor = cls.conn.cursor()
        query = "SELECT COUNT(*) FROM members WHERE NOT is_active = FALSE"

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            logger.info("the amount of active members is: %s", result)

            return result if result else None

        finally:
            cursor.close()


    @classmethod
    def get_top_member(cls):
        logger.debug("the function was called")

        cursor = cls.conn.cursor(dictionary=True)
        query = "SELECT * FROM members WHERE total_borrows = (SELECT MAX(total_borrows) FROM members)"


        try:
            cursor.execute(query)
            result = cursor.fetchall()
            
            logger.info("the top members is: %s", result)
            
            return result if result else None

        finally:
            cursor.close()