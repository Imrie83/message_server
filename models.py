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

    def save_to_db(self, cursor):           # TODO set method adding elements to table
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
        data =cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user.hashed_password = hashed_password
        return loaded_user

    @staticmethod
    def load_user_by_id(cursor):            # TODO set method loading users by id
        pass

    @staticmethod
    def load_all_users(cursor):             # TODO set method loading all users
        pass

    def delete_user(self, cursor):          # TODO set method deleting user
        pass


# For testing only!
from psycopg2 import connect

# test_case = Users('test_dummy', 'not a strong password')
# test_case_2 = Users('Dan', 'Some Random Passowrd')
# print(test_case_2.username)
# print(test_case_2.hashed_password)
# print(test_case_2._id)
# test_case.username = 'Marcin'
# test_case.hashed_password = 'my_test_password'
# print(test_case.hashed_password)
# print(test_case.username)
# print(test_case._id)
#
try:
    conn = connect(user="postgres", password="coderslab", host="localhost", dbname="message_db")
    conn.autocommit = True
    cursor = conn.cursor()
    new_user = Users.load_user_by_name(cursor, 'test 5')
except Exception as e:
    print(e)

print(new_user._id)
print(new_user.username)
print(new_user.hashed_password)