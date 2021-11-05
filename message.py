import argparse
from models import Users, Messages
from psycopg2 import connect, OperationalError


USER = 'postgres'
PASSWORD = 'coderslab'
HOST = 'localhost'
DB = 'message_db'

# TODO Add exception handling
# TODO Add additional functionality
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
        conn.close()
        return 'User does not exist'
    elif not user.hashed_password == password:
        conn.close()
        return 'Incorrect Password'
    else:
        messages = Messages.load_messages_by_sender_id(cursor, user.user_id)
        conn.close()
    return messages


def send_message(sender, password, receiver, message):

    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    sender = Users.load_user_by_name(cursor, sender)
    receiver = Users.load_user_by_name(cursor, receiver)

    if not sender:
        conn.close()
        return 'User does not exist'
    elif not sender.hashed_password == password:
        conn.close()
        return 'Incorrect Password'
    else:
        if not receiver:
            conn.close()
            return 'Recipient does not exist'
        elif len(message) > 255:
            return "Message can't be longer than 255 characters"
        else:
            to_send = Messages(sender.user_id, receiver.user_id)
            to_send.text = message
            to_send.save_to_db(cursor)
            conn.close()
            return 'Message sent successfully'


# TODO: Set parser help on incorrect argument

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='User name')
    parser.add_argument('-p', '--password', help='password - minimum 8 characters')
    parser.add_argument('-t', '--to', help='send message TO')
    parser.add_argument('-l', '--list', help='list of messages', action='store_true')
    parser.add_argument('-s', '--send', help='Message to be sent')

    args = parser.parse_args()

    # TODO: clean argument parsing!

    if args.username and args.password and args.list and not (args.to or args.send):
        to_display = display_messages(args.username, args.password)
        if not to_display:
            print('There are no messages to display for this user')
        else:
            for message in to_display:
                print(message)

    elif args.username and args.password and args.to and args.send:
        print(send_message(args.username, args.password, args.to, args.send))

    else:
        parser.print_help()
