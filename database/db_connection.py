from mysql import connector
from library_logging import logger

class SetConnection:

    conn = None

    @classmethod
    def connect(cls):

        logger.info("the function was called")
        logger.info("connecting...")

        cls.conn = connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "library_db"
    )
        
        with cls.conn.cursor(dictionary=True) as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS library_db; USE library_db")
            cursor.close()

        logger.info("connection to docker-mysql db successful")
        logger.debug('the connection to: {host = "localhost", user = "root", password = "<password>", database = "library_db"} successful')

        return cls.conn

    @classmethod    
    def get_connection(cls):
        if cls.conn.is_connected():
            logger.info("db is connect")
            return True

        logger.error("db is down. connecting...")

        cls.connect()
        cls.create_tables()

        if cls.conn:
            logger.info("db connected successful")

            return True
    
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
    gern ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
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
            