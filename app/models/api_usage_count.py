from datetime import datetime

from app.extensions import db


class ApiUsageCount(db.Document):
    userId = db.ObjectIdField(required=True)
    apiId = db.ObjectIdField(required=True)
    date = db.DateField(required=True)
    count = db.IntField(required=True, default=0)

    meta = {
        'collection': 'apiUsageCount',
        'indexes': [
            'userId',
            'apiId',
            '-date',
        ]
    }

    @staticmethod
    def increaseCount(apiId):
        ApiUsageCount.objects(apiId=apiId, date=datetime.utcnow()).update_one(inc__count=1, upsert=True)
