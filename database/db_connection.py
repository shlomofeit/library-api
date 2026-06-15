from mysql import connector
from library_logging import logger

class SetConnection:

    conn = None

    @classmethod
    def connect(cls):
        logger.info("the function was called")
        logger.info("connecting...")

        try:
            logger.info("trying to connect to library_db...")

            cls.conn = connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            port = 3306,
            database = "library_db"
        )
            
            logger.info("connection successfully")

        except connector.errors.ProgrammingError:
            logger.info("library_db is not exist. creating database...")

            with cls.conn.cursor(dictionary=True) as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS library_db; USE library_db")
                cursor.close()
            cls.connect()

        logger.info("connection to library_db successful")
        logger.debug('the connection to: {host = "localhost", user = "root", password = "<password>", database = "library_db"} successful')

        return cls.conn

    @classmethod    
    def get_connection(cls):
        if cls.conn.is_connected():
            logger.info("db is connect")
            return cls.conn

        logger.error("db is down. connecting...")

        cls.connect()
        cls.create_tables()

        if cls.conn.is_connected():
            logger.info("db connected successful")

            return cls.conn
    
        logger.error("failed to connect")
    
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
        logger.info("created tables if there not exist successfully.")

    @classmethod
    def close_conn(cls):
        if cls.conn and cls.conn.is_connected():
            cls.conn.close()
            logger.info("connection was closed")