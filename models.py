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

class