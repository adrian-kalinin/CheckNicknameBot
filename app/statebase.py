import pymongo


class StateBase:
    def __init__(self, db_name='CheckNicknameBot', coll_name='states'):
        self.client = pymongo.MongoClient()
        self.db = self.client[db_name]
        self.coll = self.db[coll_name]

    def __enter__(self):
        return self

    def __exit__(self, ex_type, value, traceback):
        self.client.close()

    def __getitem__(self, user_id):
        result = self.coll.find_one({'user_id': user_id})

        if isinstance(result, dict):
            del result['user_id']
            del result['_id']

            return result

    def __setitem__(self, user_id, value):
        if self.__getitem__(user_id):
            self.coll.delete_many({'user_id': user_id})

        if isinstance(value, (tuple, list)):
            state = value[0]
            data = value[1]
        else:
            state = value
            data = None

        self.coll.insert_one({'user_id': user_id, 'state': state, 'data': data})

    def __delitem__(self, user_id):
        self.coll.delete_many({'user_id': user_id})

