from app.extensions import mongo


class UserRepository(object):
    def insert_one(self, data):
        if 'username' in data and mongo.db.user.find_one({'username': data['username']}) is not None:
            return None
        if 'email' in data and mongo.db.user.find_one({'email': data['email']}) is not None:
            return None
        result = mongo.db.user.insert_one(data)
        user = mongo.db.user.find_one({"_id": result.inserted_id})
        return user

    def find_by_username_or_email(self, username):
        user = mongo.db.user.find_one({'username': username})
        if user is None:
            user = mongo.db.user.find_one({'email': username})
        return user


user_repo = UserRepository()
