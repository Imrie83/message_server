import argparse
from models import Users, Messages
from psycopg2 import connect, OperationalError

# Database login variables
USER = 'postgres'
PASSWORD = 'coderslab'
HOST = 'localhost'
DB = 'message_db'

# TODO Add exception handling
# TODO Add additional functionality
# TODO create class to connect to database!


def display_messages(username, password):
    """
    Function displays all messages of a usser based on username.

    The function does the following:
        - Connects to the database
        - Creates User object based on username (load_user_by_name method)
        - Check if user exist (object not empty) and password correct
        - Creates Messages object based on user id, containing a list of all messages

    :param str username: user name
    :param str password: password, not hashed

    :rtype: list
    :return: returns a list of messages (as Messages object)
    """
    # Connecto to DB
    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    # Create user object based on user name
    user = Users.load_user_by_name(cursor, username)

    # Check if user exist and password correct
    if not user:
        conn.close()
        return 'User does not exist'
    elif not crypto.check_password(password, user.hashed_password):
        conn.close()
        return 'Incorrect Password'
    else:
        # Create a Messages object containing a list of all messages to be returned
        messages = Messages.load_messages_by_sender_id(cursor, user.user_id)
        conn.close()
    return messages


def send_message(sender, password, receiver, message):
    """
    Function displays all messages of a usser based on username.

    The function does the following:
        - Connects to the database
        - Creates User object based on username (load_user_by_name method)
        - Check if user exist (object not empty) and password correct
        - Creates Messages object based on user id, containing a list of all messages

    :param str username: user name
    :param str password: password, not hashed
    :param str receiver: send message to this user name
    :param str message: message to be sent, max 255 characters

    :rtype: str
    :return: Return messages based on whether operation have been successful or failed
    """
    # Connecto to DB
    try:
        conn = connect(user=USER, password=PASSWORD, host=HOST, dbname=DB)
        conn.autocommit = True
        cursor = conn.cursor()
    except OperationalError as e:
        return 'Connection error', e

    # Create two user objects, one for "sender" one for "receiver"
    # use  these to check if users exists, if yes extract user id required to send the message
    sender = Users.load_user_by_name(cursor, sender)
    receiver = Users.load_user_by_name(cursor, receiver)

    if not sender:                                                      # Check if "sender" exist
        conn.close()
        return 'User does not exist'
    elif not crypto.check_password(password, sender.hashed_password):   # Check if password for sender correct
        conn.close()
        return 'Incorrect Password'
    else:
        if not receiver:                                                # Check if "receiver" exist
            conn.close()
            return 'Recipient does not exist'
        elif len(message) > 255:                                        # Check message length, no more than 255 char
            return "Message can't be longer than 255 characters"
        else:
            to_send = Messages(sender.user_id, receiver.user_id)        # Create Messages object
            to_send.text = message                                      # Add message to the o bject
            to_send.save_to_db(cursor)                                  # Save message to the database
            conn.close()
            return 'Message sent successfully'


# TODO: Set parser help on incorrect argument

if __name__ == '__main__':
    # Initiate argument parser, and add require arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='User name')
    parser.add_argument('-p', '--password', help='password - minimum 8 characters')
    parser.add_argument('-t', '--to', help='send message TO')
    parser.add_argument('-l', '--list', help='list of messages', action='store_true')
    parser.add_argument('-s', '--send', help='Message to be sent')

    args = parser.parse_args()

    # TODO: clean argument parsing!

    # If ONLY username, password and list in arguments display messages
    if args.username and args.password and args.list and not (args.to or args.send):
        to_display = display_messages(args.username, args.password)
        if not to_display:                      # If message list empty return information
            print('There are no messages to display for this user')
        else:
            for message in to_display:          # Else iterate through message list and display each message
                print(message)
    # If username, password, to (addressee) and send in arguments
    elif args.username and args.password and args.to and args.send:
        # Send message / display error info
        print(send_message(args.username, args.password, args.to, args.send))

    else:
        parser.print_help()
