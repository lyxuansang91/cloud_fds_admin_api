from datetime import datetime

from app.extensions import db
from .seq import Seq


class UserAddress(db.Document):
    userId = db.ObjectIdField(required=True)
    addressId = db.IntField(required=True, unique=True)
    address = db.StringField(required=True, max_length=200)
    currency = db.StringField(required=True, max_length=200)
    createdAt = db.DateTimeField(required=True, default=datetime.utcnow)
    updatedAt = db.DateTimeField()

    meta = {
        'collection': 'userAddress',
        'indexes': [
            {'fields': ['address', 'currency']},
            'userId',
            'currency',
            'address'
        ]
    }

    @staticmethod
    def get_address(user_id, currency, address):
        try:
            doc = UserAddress.objects.get(address=address, currency=currency)
            return doc
        except Exception:
            doc = UserAddress(userId=user_id, addressId=Seq.getNextValue('userAddress'), address=address, currency=currency, updatedAt=datetime.utcnow())
            doc.save()
            return doc
