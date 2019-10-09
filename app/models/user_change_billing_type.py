from datetime import datetime

from app.extensions import db
from app.utils import first_of_next_month


class UserChangeBillingType(db.Document):
    userId = db.ObjectIdField(required=True)
    billingType = db.ObjectIdField(required=True)
    startDate = db.DateField(required=True, default=first_of_next_month)
    createdAt = db.DateTimeField(required=True, default=datetime.utcnow)
    createdBy = db.StringField(required=True, max_length=100)
    updatedAt = db.DateTimeField()
    isUpdated = db.BooleanField(required=True, default=False)
    updatedBy = db.StringField(max_length=100)

    meta = {
        'collection': 'userChangeBillingType',
        'indexes': [
            'userId'
        ]
    }
