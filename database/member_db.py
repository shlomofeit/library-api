# from library_logging import logger

class MemberDB:
    def __init__(self, conn):
        self.conn = self.conn

    def create_member(self, data: dict):
        cursor = self.conn.cursor()
        query = "INSERT INTO members (name, email, is_availble) VALUES (%s, %s, TRUE)"

        try:
            cursor.execute(query, [data["name"], data["email"]])

        except Exception as e:
            pass
            # logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()


    def get_all_members(self):
        cursor = self.conn.cursor(dictinary=True)
        query = "SELECT * FROM members"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result if result else None

        except Exception as e:
            pass
            # logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()    


    def get_member_by_id(self, id):
        cursor = self.conn.cursor(dictinary=True)
        query = "SELECT * FROM members WHERE id = %s"

        try:
            cursor.execute(query, [id])
            result = cursor.fetchall()
            return result if result else None

        except Exception as e:
            pass
            # logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()


    def update_member(self, id: int, data: dict):
        cursor = self.conn.cursor(dictinary=True)
        query_keys = ", ".join(f"{f} = %s" for f in data)
        query = f"UPDATE members SET ({query_keys}) WHERE id = %s"

        try:
            cursor.execute(query, [data.values()] + [id])

        except Exception as e:
            pass
            # logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()


    def deactivate_member(self, id: int):
        cursor = self.conn.cursor(dictinary=True)
        query = "UPDATE members SET is_active = FALSE WHERE id = %s"

        try:
            cursor.execute(query, [id])

        except Exception as e:
            pass
            # logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()

    def activate_member(self, id: int):
        cursor = self.conn.cursor(dictinary=True)
        query = "UPDATE members SET is_active = TRUE WHERE id = %s"

        try:
            cursor.execute(query, [id])

        except Exception as e:
            pass
            # logger.error("Adding the member failed. Error: %s", e)

        finally:
            cursor.close()


    def increment_borrows(self, member_id: id):
        cursor = self.conn.cursor(dictinary=True)
        query = "UPDATE members SET total_borrows=total_borrows+1 WHERE id = %s"

        try:
            cursor.execute(query, [member_id])
            result = cursor.fetchall()
            return result if result else None

        finally:
            cursor.close()


    def count_active_members(self):
        cursor = self.conn.cursor(dictinary=True)
        query = "SELECT COUNT(*) FROM members WHERE NOT is_active = FALSE"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result if result else None

        finally:
            cursor.close()


    def get_top_member(self):
        cursor = self.conn.cursor(dictinary=True)
        query = "SELECT * FROM members ORDER BY total_borrows ASC WHERE total_borrows = (SELECT MAX(total_borrows) FROM members)"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result if result else None

        finally:
            cursor.close()