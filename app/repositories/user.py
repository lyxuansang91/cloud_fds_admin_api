from app import models as m


class UserRepository(object):
    def insert_one(self, data):
        if 'email' in data and m.User.objects.filter(email=data['email']).first() is not None:
            return None, 'email existing'
        if 'username' in data and m.User.objects.filter(username=data['username']).first() is not None:
            return None, 'username existing'
        user = m.User(**data)
        user.save()
        return user, None

    def find_by_username_or_email(self, username):
        user = m.User.objects.get(username=username)
        if user is None:
            user = m.User.objects.get(email=username)
        return user


user_repo = UserRepository()
