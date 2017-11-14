from flask_login import UserMixin

from app import db, lm


class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

    @classmethod
    def load(cls, user_id):
        return cls.query.get(int(user_id))


@lm.user_loader
def load_user(user_id):
    return UserModel.load(user_id)
