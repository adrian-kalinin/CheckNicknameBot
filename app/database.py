import sqlite3


class DataBase:
    def __init__(self, name='users'):
        self.connection = sqlite3.connect(f'{name}.sqlite')
        self.name = name

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, ex_type, value, traceback):
        self.close()

    def setup(self):
        self.connection.execute(
            f'CREATE TABLE IF NOT EXISTS {self.name} ('
            'user_id INTEGER NOT NULL PRIMARY KEY UNIQUE,'
            'lang TEXT NOT NULL DEFAULT "en",'
            'requests INTEGER NOT NULL DEFAULT 0);'
        )
        self.connection.commit()

    def get_users(self):
        result = self.connection.execute(f'SELECT user_id FROM {self.name}')
        return [x[0] for x in result]

    def get_requests(self):
        result = self.connection.execute(f'SELECT SUM(requests) FROM {self.name}')
        return result.fetchone()[0]

    def add_user(self, user_id):
        if not self.check_user(user_id):
            stat = f'INSERT INTO {self.name} (user_id) VALUES (?)'
            self.connection.execute(stat, [user_id])
            self.connection.commit()

    def del_user(self, user_id):
        stat = f'DELETE FROM {self.name} WHERE user_id = (?)'
        if self.check_user(user_id):
            self.connection.execute(stat, [user_id])
            self.connection.commit()

    def check_user(self, user_id):
        stat = f'SELECT EXISTS(SELECT 1 FROM {self.name} WHERE user_id = (?));'
        result = self.connection.execute(stat, [user_id])
        return result.fetchone()[0]

    def get_users_amount(self):
        stat = f'SELECT Count(*) FROM {self.name}'
        result = self.connection.execute(stat)
        return result.fetchone()[0]

    def set_value(self, user_id, item, data):
        if self.check_user(user_id):
            try:
                query = f'UPDATE {self.name} SET {item} = (?) WHERE user_id = (?)'
                self.connection.execute(query, (data, user_id))
                self.connection.commit()
            except sqlite3.Error:
                return False

    def get_value(self, user_id, item):
        if self.check_user(user_id):
            try:
                query = f'SELECT {item} FROM {self.name} WHERE user_id = (?)'
                result = self.connection.execute(query, [user_id])
                return result.fetchone()[0]
            except sqlite3.Error:
                return False

    def increment(self, user_id, item):
        amount = self.get_value(user_id=user_id, item=item)
        self.set_value(user_id=user_id, item=item, data=amount + 1)

    def get_languages(self):
        en_users = self.connection.execute(f'SELECT Count(*) FROM {self.name} WHERE lang = "en"')
        ru_users = self.connection.execute(f'SELECT Count(*) FROM {self.name} WHERE lang = "ru"')
        return {'en': en_users.fetchone()[0], 'ru': ru_users.fetchone()[0]}

    def close(self):
        self.connection.close()
