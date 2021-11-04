class Users:
    def __init__(self, username='', password='', salt=''):
        self._id = -1
        self.username = username
        self._hashed_password = password    # TODO setup password hashing!
        self.salt = salt

    @property
    def user_id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, new_pass):
        self._hashed_password = new_pass    # TODO set up password hashing in setter!

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO users(username, hashed_password) VALUES (%s, %s) RETURNING id"
            values = (self.username, self._hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE users SET username = %s, hashed_password = %s WHERE id = %s"
            values = (self.username, self._hashed_password, self._id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_name(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username, hashed_password)
            loaded_user._id = id_
            return loaded_user

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id = %s"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username, hashed_password)
            loaded_user._id = id_
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        user_list = []
        sql = "SELECT id, username, hashed_password FROM users"
        cursor.execute(sql)
        data = cursor.fetchall()

        for row in data:
            id_, username, hashed_password = row
            loaded_user = Users(username, hashed_password)
            loaded_user._id = id_
            user_list.append(loaded_user)
        return user_list

    def delete_user(self, cursor):
        sql = "DELETE FROM users WHERE id = %s"
        cursor.execute(sql, (self._id,))
        self._id = -1
        return True

    @staticmethod
    def delete_user_by_id(cursor, id_):
        sql = "DELETE FROM users WHERE id = %s"
        cursor.execute(sql, (id_,))
        return True

class Messages:
    def __init__(self, from_id, to_id):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = ''
        self.creation_date = None

    @property
    def message_id(self):
        return self._id

    @staticmethod
    def load_all_messages(cursor):
        all_messages = []
        sql = "SELECT id, from_id, to_id, creation_date, text FROM messages"
        cursor.execute(sql)

        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_message = Messages(from_id, to_id)
            loaded_message._id = id_
            loaded_message.creation_date = creation_date
            loaded_message.text = text
            all_messages.append(loaded_message)
        return all_messages

    @staticmethod
    def load_messages_by_sender_id(cursor, sender_id):
        all_messages = []
        sql = "SELECT id, from_id, to_id, creation_date, text FROM messages WHERE from_id = %s"
        cursor.execute(sql, (sender_id,))

        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_message = Messages(from_id, to_id)
            loaded_message._id = id_
            loaded_message.creation_date = creation_date
            loaded_message.text = text
            all_messages.append(loaded_message)
        return all_messages

    @staticmethod
    def load_messages_by_receip_id(cursor, sender_id):
        all_messages = []
        sql = "SELECT id, from_id, to_id, creation_date, text FROM messages WHERE to_id = %s"
        cursor.execute(sql, (sender_id,))

        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_message = Messages(from_id, to_id)
            loaded_message._id = id_
            loaded_message.creation_date = creation_date
            loaded_message.text = text
            all_messages.append(loaded_message)
        return all_messages

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO messages(from_id, to_id, text) VALUES (%s, %s, %s) RETURNING id"
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE messages SET from_id = %s, to_id = %s, text = %s WHERE id = %s"
            values = (self.from_id, self.to_id, self.text, self._id)
            cursor.execute(sql, values)
            return True

    def delete_message(self, cursor):
        sql = "DELETE messages WHERE id = %s"
        cursor.execute(sql, self._id)
        self._id = -1



#FOR TESTING ONLY
from psycopg2 import connect

message_1 = Messages(15, 8)
message_1.text = 'This is a random message'
print(message_1._id)



try:
    conn = connect(user="postgres", password="coderslab", host="localhost", dbname="message_db")
    conn.autocommit = True
    cursor = conn.cursor()
    all_messages = Messages.load_all_messages(cursor)
    user_messages = Messages.load_messages_by_sender_id(cursor, 3)
    user_messages_2 = Messages.load_messages_by_receip_id(cursor, 6)
    user_messages_3 = Messages.load_messages_by_receip_id(cursor, 10)
    Messages.save_to_db(message_1, cursor)
except Exception as e:
    print(e)

for message in all_messages:
    print(message._id,message.from_id, message.to_id, message.creation_date, message.text)

print('*'*50)

for message in user_messages:
    print(message._id,message.from_id, message.to_id, message.creation_date, message.text)

print('*' * 50)

for message in user_messages_2:
    print(message._id, message.from_id, message.to_id, message.creation_date, message.text)

print('*' * 50)

for message in user_messages_3:
    print(message._id, message.from_id, message.to_id, message.creation_date, message.text)

message_1.text = 'A small Change'
print(message_1._id)

try:
    conn = connect(user="postgres", password="coderslab", host="localhost", dbname="message_db")
    conn.autocommit = True
    cursor = conn.cursor()
    Messages.save_to_db(message_1, cursor)
except Exception as e:
    print(e)