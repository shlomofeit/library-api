from mysql import connector
# from library_logging import logger

class SetConnection:

    conn = None

    @classmethod
    def connect(cls):

        # logger.info("the function was called")
        # logger.info("connecting...")

        try:
            cls.conn = connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            port = 3306,
            database = "library_db"
        )

        except connector.errors.ProgrammingError:

            with cls.conn.cursor(dictionary=True) as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS library_db; USE library_db")
                cursor.close()
            cls.connect()

        # logger.info("connection to docker-mysql db successful")
        # logger.debug('the connection to: {host = "localhost", user = "root", password = "<password>", database = "library_db"} successful')

        return cls.conn

    @classmethod    
    def get_connection(cls):
        if cls.conn is not None:
            # logger.info("db is connect")
            return cls.conn

        # logger.error("db is down. connecting...")

        cls.connect()
        cls.create_tables()

        if cls.conn:
            # logger.info("db connected successful")

            return cls.conn
    
        # logger.error("failed to connect")
    
    @classmethod
    def create_tables(cls):

        cls.cursor = cls.conn.cursor()

        cls.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(50) NOT NULL,
    genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
    is_availble BOOLEAN NOT NULL,
    borrowed_by_member_id INT
);
        CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    is_active BOOLEAN NOT NULL,
    total_borrows INT NOT NULL DEFAULT 0
);
"""
        ) 

        cls.cursor.close()

    @classmethod
    def close_conn(cls):
        if cls.conn and cls.conn.is_connected():
            cls.conn.close()