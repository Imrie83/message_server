from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

# Define database user, password, host and database name required for connection
USER = 'postgres'
PASSWORD = 'coderslab'
HOST = 'localhost'
DB_NAME = 'message_db'


# Function connecting to database and executing query - does not return anything.
def execute_db(sql, db=''):   # takes sql query and database name as arguments

    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=db)
        conn.autocommit = True      # Set autocommit to true
        cursor = conn.cursor()
        cursor.execute(sql)         # Execute query
        conn.close()                # Close connection

    except OperationalError as e:   # Catch errors connecting to database
        print(f'Connection Error: {e}')


# Define SQL queries to create a DB and two required tables
create_db_sql = f"CREATE DATABASE {DB_NAME};"

creat_users_sql = """CREATE TABLE Users(
id serial PRIMARY KEY NOT NULL,
username varchar(255) UNIQUE ,
hashed_password varchar(80)
);
"""

create_messages_sql = """CREATE TABLE Messages(
id serial PRIMARY KEY NOT NULL,
from_id int,
to_id int,
creation_date timestamp,
text varchar(255),
FOREIGN KEY (from_id) REFERENCES users(id),
FOREIGN KEY (to_id) REFERENCES users(id)
);
"""

try:
    execute_db(create_db_sql)   # Create database
except DuplicateDatabase as e:  # Catch exception if exists
    print(f'Database already exist', e)

try:
    execute_db(creat_users_sql, DB_NAME)    # Create table
except DuplicateTable as e:                 # Catch exception if exists
    print(f'Database already exist', e)

try:
    execute_db(create_messages_sql, DB_NAME)    # Create table
except DuplicateTable as e:                     # Catch exception if exists
    print(f'Database already exist', e)
