import argparse
from models import Users, Messages
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

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

    m = (display_messages('test 5', 'asgdfs a3245'))
    for i in m:
        print(i)
    n = display_messages('test', 'aewstfgasdf')
    if not n:
        print('No Messages')
    else:
        for i in n:
            print(i)

    print(send_message('test 5', 'asgdfs a3245', 'Marcin22',\
                       'This is a random message to be sent lkasejf;l salkwasejro;awieujr sdaifo jawoiperu jsladk;fj \
                       ao;weiu jraslkef ja;woij 3efoiwaejt flkjsdrhfg lkjaewh talw3ehf lksadrjawslkje htfgawoueeh \
                       tiouwahefgkljsdarh glkjaershg askj hgfkljas hgsklaskej hfkljasdh s a sdaj'))

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
