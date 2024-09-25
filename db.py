import mysql.connector
from mysql.connector import errorcode

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='123456',
                database='cs_tournament_management_system'
            )
            self.cursor = self.conn.cursor()
            self.create_tables_if_not_exists()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist. Creating database...")
                self.create_database()
            else:
                print(err)
                exit(1)

    def create_database(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='123456'
            )
            self.cursor = self.conn.cursor()
            self.run_sql_script('setup.sql', 'utf-8')
            self.conn.database = 'cs_tournament_management_system'
            self.create_tables_if_not_exists()
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    def run_sql_script(self, script_path, encoding):
        with open(script_path, 'r', encoding=encoding) as file:
            sql_script = file.read()
        commands = sql_script.split(';')
        for command in commands:
            if command.strip():
                self.cursor.execute(command)
        self.conn.commit()

    def create_tables_if_not_exists(self):
        self.run_sql_script('setup.sql', 'utf-8')

    def verify_admin(self, username, password):
        self.cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        result = self.cursor.fetchone()
        return result is not None

    def start_transaction(self):
        self.conn.start_transaction()

    def commit_transaction(self):
        if self.conn.in_transaction:
            self.conn.commit()

    def rollback_transaction(self):
        if self.conn.in_transaction:
            self.conn.rollback()
