import argparse
from models import Users, Messages
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

USER = 'postgres'
PASSWORD = 'coderslab'
HOST = 'localhost'
DB = 'message_db'

# TODO Add exception handling
# TODO Add additionall functionality
# TODO create class to connecto to database!


def display_messages(username, password):

    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    user = Users.load_user_by_name(cursor, username)

    if not user:
        return 'User does not exist'

    elif not user.hashed_password == password:
        return 'Incorrect Password'

    else:
        messages = Messages.load_messages_by_sender_id(cursor, user.user_id)
        if not messages:
            return 'No messages from this user'
        else:
            for message in messages:
                print(message)


# TODO: Set parser help on incorrect argument

if __name__ == '__main__':

    display_messages('test 5', 'asgdfs a3245')
    print(display_messages('test', 'aewstfgasdf'))

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-u', '--username', help='username')
    # parser.add_argument('-p', '--password', help='password - minimum 8 characters')
    # parser.add_argument('-t', '--to', help='send message TO')
    # parser.add_argument('-l', '--list', help='user list', action='store_true')
    # parser.add_argument('-s', '--send', help='delete user', action='store_true')
    #
    # args = parser.parse_args()
    #
    # # TODO: clean argument parsing!
    # if args.list:
    #     list_all_users()
    # if args.username and args.password and not args.edit and not args.delete:
    #     print(create_user(args.username, args.password))
    # if args.username and args.password and args.edit and args.new_pass:
    #     print(edit_password(args.username, args.password, args.new_pass))
    # if args.username and args.password and args.delete:
    #     print(delete_user(args.username, args.password))