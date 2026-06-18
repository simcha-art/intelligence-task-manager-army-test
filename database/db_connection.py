"""
DB_connection

This class response to connect to docker container and to the DB in it.

methods:
get_connection() ---> returns an active connection to the database (mysql)
create_database() ---> create the database if not exists
create_tables() -> create the tablse mission and agent if they are not exists



"""
import mysql.connector

class DB_connection:
    # def __init__(self):
    #     self.get_connection()
    #     self.create_database()
    #     self.create_tables()

    def get_connection(self):
        self.conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1234"
        )

    def create_database(self):
        with self.conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
            cursor.execute("USE Intelligence_db")


    def create_tables(self):
        agents_table = """
            CREATE TABLE IF NOT EXISTS agents(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            specialty VARCHAR(150) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            completed_missions INT DEFAULT 0,
            failed_missions INT DEFAULT 0,
            agent_rank ENUM('Junior', 'Senior', 'Commander')
            )
            """

        missions_table = """
            CREATE TABLE IF NOT EXISTS missions(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(150) NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(100) NOT NULL,
            difficulty INT CHECK (difficulty BETWEEN 1 AND 10) NOT NULL,
            importance INT CHECK (importance BETWEEN 1 AND 10) NOT NULL,
            status ENUM('NEW', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'NEW',
            risk_level VARCHAR(30) NOT NULL,
            assigned_agent_id INT DEFAULT NULL
            )
            """
        with self.conn.cursor() as cursor:
            cursor.execute(agents_table)
            cursor.execute(missions_table)



DB_conn = DB_connection()