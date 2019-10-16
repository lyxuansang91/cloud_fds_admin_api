from datetime import datetime

from app.extensions import db


class Price(db.Document):
    billingType = db.ObjectIdField(required=True)
    startDate = db.DateField(required=True)
    endDate = db.DateField(required=False)
    price = db.DecimalField(required=True)
    createdAt = db.DateTimeField(required=True, default=datetime.utcnow)
    createdBy = db.StringField(required=True, max_length=100)

    meta = {'collection': 'price'}
