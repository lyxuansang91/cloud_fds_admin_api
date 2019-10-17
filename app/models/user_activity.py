from datetime import datetime

from app.extensions import db


class UserActivity(db.Document):
    userId = db.ObjectIdField()
    activity = db.StringField(required=True, default='')
    desc = db.StringField(required=True, default='')
    createdAt = db.DateTimeField(required=True, default=datetime.utcnow)

    meta = {
        'collection': 'userActivity',
        'indexes': [
            'userId',
            'activity',
            '-createdAt'
        ]
    }
