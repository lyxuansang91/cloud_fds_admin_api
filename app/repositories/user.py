from datetime import datetime
from flask import current_app
from bson import ObjectId

from app import models as m
from app.extensions import flask_bcrypt


class UserRepository(object):
    def get_by_id(self, user_id):
        return m.User.objects.filter(id=ObjectId(user_id)).first()

    def insert_one(self, data):
        if 'email' in data and m.User.objects.filter(email=data['email']).first() is not None:
            return None, 'email existing'
        if 'username' in data and m.User.objects.filter(username=data['username']).first() is not None:
            return None, 'username existing'
        user = m.User(**data)
        user.save()
        return user, None

    def find_by_username_or_email(self, username):
        user = m.User.objects.filter(username=username).first()
        if user is None:
            user = m.User.objects.filter(email=username).first()
        return user

    def update_user(self, user, current_user, args):
        args['updatedAt'] = datetime.utcnow()
        args['updatedBy'] = current_user.email
        if 'password' in args:
            args['password'] = flask_bcrypt.generate_password_hash(args['password']).decode('utf-8')
        try:
            user.update(**args)
            return True
        except Exception as e:
            current_app.logger.error('exception:', e)
            return False


user_repo = UserRepository()
