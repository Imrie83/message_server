import argparse
from models import Users, Messages
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

USER = 'postgres'
PASSWORD = 'coderslab'
HOST = 'localhost'
DB = 'message_db'

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password - minimum 8 characters')
parser.add_argument('-n', '--new_pass', help='create new password')
parser.add_argument('-l', '--list', help='user list')
parser.add_argument('-d', '--delete', help='delete user')
parser.add_argument('-e', '--edit', help='edit user')

# display parser help
# parser.print_help()
# TODO Add exception handling
# TODO Add additionall functionality

def create_user(username, password):

    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    if len(password) < 8:
        return 'Password requires min. 8 characters!'
    else:
        new_user = Users(username, password)
        try:
            new_user.save_to_db(cursor)
        except UniqueViolation:
            return 'User already exist - Username must be UNIQUE'
        return new_user


def edit_password(username, password, new_pass=''):

    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    user = Users.load_user_by_name(cursor, username)

    if not user:
        return 'User does not exist in database'

    elif not user.hashed_password == password:
        return 'Password incorrect'

    elif len(new_pass) < 8:
        return 'New password too short - minimum 8 characters required'

    else:
        user.hashed_password = new_pass
        user.save_to_db(cursor)

    return 'Password changed successfully'


# Tests
# some_user = create_user('TANK3', 'password')
# print(some_user)
# print(some_user.username, some_user.user_id)


print(edit_password('TANK3', 'password'))
print(edit_password('TANK3', 'passwor'))
print(edit_password('TANK4', 'test'))
print(edit_password('TANK3', 'password', 'some_new_pass'))