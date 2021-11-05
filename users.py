import argparse
from models import Users
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
import crypto

USER = 'postgres'
PASSWORD = 'coderslab'
HOST = 'localhost'
DB = 'message_db'

# TODO Add exception handling
# TODO Add additionall functionality
# TODO create class to connecto to database!
# TODO close connections in functions!


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
        return 'User created successfully'


def edit_password(username, password, new_pass=''):

    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    # TODO Figure out password checks
    user = Users.load_user_by_name(cursor, username)
    if not user:
        return 'User does not exist in database'

    elif not crypto.check_password(password, user.hashed_password):
        return 'Incorrect Password'

    elif len(new_pass) < 8:
        return 'New password too short - minimum 8 characters required'

    else:
        user.hashed_password = crypto.hash_password(new_pass)
        user.save_to_db(cursor)

    return 'Password changed successfully'


def delete_user(username, password):

    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    user = Users.load_user_by_name(cursor, username)

    if not user:
        return 'User does not exist'

    elif not crypto.check_password(password, user.hashed_password):
        return 'Incorrect Password'

    else:
        user.delete_user(cursor)
        return 'User has been deleted.'


def list_all_users():

    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    users = Users.load_all_users(cursor)

    # TODO: create "table" displaying evenly spaced user details
    for user in users:
        print(f'''ID: {user.user_id}
Username: {user.username}
{'-'*30}''')


# TODO: Set parser help on incorrect argument

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password - minimum 8 characters')
    parser.add_argument('-n', '--new_pass', help='create new password')
    parser.add_argument('-l', '--list', help='user list', action='store_true')
    parser.add_argument('-d', '--delete', help='delete user', action='store_true')
    parser.add_argument('-e', '--edit', help='edit user', action='store_true')
    args = parser.parse_args()

    # TODO: clean argument parsing!
    if args.list:
        list_all_users()
    if args.username and args.password and not args.edit and not args.delete:
        print(create_user(args.username, args.password))
    if args.username and args.password and args.edit and args.new_pass:
        print(edit_password(args.username, args.password, args.new_pass))
    if args.username and args.password and args.delete:
        print(delete_user(args.username, args.password))


# # Tests
# # TODO: Learn how to write proper unittests...
# some_user = create_user('TANK99', 'password_2')
# try:
#     print(some_user)
#     print(some_user.username, some_user.user_id)
# except Exception as e:
#     print(e)
#
# print(edit_password('TANK3', 'password'))
# print(edit_password('TANK3', 'passwor'))
# print(edit_password('TANK4', 'test'))
# print(edit_password('TANK3', 'password', 'some_new_pass'))
# print(delete_user('TANK99', 'pass'))
# print(delete

