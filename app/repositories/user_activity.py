from flask import current_app

from app import models as m


class UserActivityRepository(object):
    def create_activity(self, args):
        try:
            activity = m.UserActivity(**args)
            activity.save()
            return activity
        except Exception as e:
            current_app.logger.error(e)
            return None


user_activity_repo = UserActivityRepository()
