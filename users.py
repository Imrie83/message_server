import argparse
from models import Users
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
import crypto

# Variables required to connect to a database
USER = 'postgres'
PASSWORD = 'coderslab'
HOST = 'localhost'
DB = 'message_db'

# TODO Add exception handling
# TODO Add additional functionality
# TODO create class to connect to database!


def create_user(username, password):

    """
    Function creates a new user in database.

    The function does the following:
        - tries to connect to a database
        - checks the length of password
        - creates User object
        - tries to save User object
        - if user exist raises UniqueViolation exception

    :param str username: user name
    :param str password: new, not hashed password

    :rtype: str
    :return: Messages depending whether operation was successful or ended prematurely
    """

    # Connect to a database, return exception on connection errors
    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    # Check if length of password is min 8 characters long. If not return correct message
    if len(password) < 8:
        conn.close()
        return 'Password requires min. 8 characters!'
    else:
        new_user = Users(username, password)        # Create User object
        try:
            new_user.save_to_db(cursor)             # Try to save the user, if user exists return message
        except UniqueViolation:
            conn.close()
            return 'User already exist - Username must be UNIQUE'
        conn.close()
        return 'User created successfully'


def edit_password(username, password, new_pass):

    """
    Function allows to edit user password.

    The function does the following:
        - Creates User object with 'load_user_by_name method
        - If User object is empty - user does not exist in DB, returns correct message
        - If user exist check password input = hashed password, if no match - return correct message
        - If password correct check length of new password and hash it
        - Save new user object in to database

    :param str username: user name
    :param str password: password for the user account, not hashed
    :param str new_pass: a new password for the user account

    :rtype: str
    :return: Messages depending whether operation was successful or ended prematurely
    """

    # Try to connect to a database
    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    # Load User object using load_user_by_name method
    user = Users.load_user_by_name(cursor, username)

    # If User object is empty -> user does not exist, return correct message
    if not user:
        conn.close()
        return 'User does not exist in database'
    # If password passed from argument does not match stored password return correct message
    elif not crypto.check_password(password, user.hashed_password):
        conn.close()
        return 'Incorrect Password'
    # If new password too short return correct message
    elif len(new_pass) < 8:
        conn.close()
        return 'New password too short - minimum 8 characters required'
    else:
        user.hashed_password = crypto.hash_password(new_pass)   # Hash new password and add it to User object
        user.save_to_db(cursor)                                 # Save changes to database
    conn.close()
    return 'Password changed successfully'


def delete_user(username, password):

    """
    Function deletes user from database.

    The function does the following:
        - Creates User object with 'load_user_by_name method
        - If User object is empty - user does not exist in DB, returns correct message
        - If user exist check password input = hashed password, if no match - return correct message
        - If password correct delete user from databasse

    :param str username: user name
    :param str password: password for the user account, not hashed

    :rtype: str
    :return: Messages depending whether operation was successful or ended prematurely
    """

    # Try to connect to DB
    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    # Create User object
    user = Users.load_user_by_name(cursor, username)

    if not user:                                                        # Check if user exist
        conn.close()
        return 'User does not exist'
    elif not crypto.check_password(password, user.hashed_password):     # Check if password correct
        conn.close()
        return 'Incorrect Password'
    else:
        user.delete_user(cursor)                                        # Delete user
        conn.close()
        return 'User has been deleted.'


def list_all_users():

    """
    Function loads list of all users in DB.

    The function does the following:
        - Creates Users object containing a list of all users in DB
        - Iterates through list
        - For each element in list prints out user ID and Username

    :param str username: user name
    :param str password: password for the user account, not hashed

    :rtype: str
    :return: Messages depending whether operation was successful or ended prematurely
    """

    # Connecto to DB
    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    # Create Users object containing all users in DB
    users = Users.load_all_users(cursor)

    # TODO: create "table" displaying evenly spaced user details
    # Iterate through users list, for each user display user ID and Username
    for user in users:
        print(f'''ID: {user.user_id}
Username: {user.username}
{'-'*30}''')

    conn.close()


if __name__ == '__main__':

    # Initiate parser with it's arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password - minimum 8 characters')
    parser.add_argument('-n', '--new_pass', help='create new password')
    parser.add_argument('-l', '--list', help='user list', action='store_true')
    parser.add_argument('-d', '--delete', help='delete user', action='store_true')
    parser.add_argument('-e', '--edit', help='edit user', action='store_true')

    try:
        args = parser.parse_args()

        # If username and password only in arguments create user
        if args.username and args.password and not (args.edit or args.delete or args.list or args.delete):
            print(create_user(args.username, args.password))

        # If username, password, new pass and edit flags in arguments try to change password
        elif args.username and args.password and args.edit and args.new_pass and not (args.list or args.delete):
            print(edit_password(args.username, args.password, args.new_pass))

        # If username, password and delete flag - try to delete user
        elif args.username and args.password and args.delete and not (args.list or args.edit or args.new_pass):
            print(delete_user(args.username, args.password))
        if args.list:   # If -l or --list in arguments display list of users
            list_all_users()

    except Exception as e:     # if no correct arguments detected (errors out) display help
    except Exception as e:     # if no correct arguments detected (errors out) display help
        # print(e)
        # parser.print_help()

