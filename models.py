class Users:
    def __init__(self, username, password, salt=''):
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

    @new_password.setter
    def new_password(self, new_pass):
        self._hashed_password = new_pass    # TODO set up password hashing in setter!

    def save_to_db(self, cursor):           # TODO set method adding elements to table
        pass

    @staticmethod
    def load_user_by_name(cursor):          # TODO set method loading users by name
        pass

    @staticmethod
    def load_user_by_id(cursor):            # TODO set method loading users by id
        pass

    @staticmethod
    def load_all_users(cursor):             # TODO set method loading all users
        pass

    def delete_user(self, cursor):          # TODO set method deleting user
        pass
