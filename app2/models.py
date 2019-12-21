from app2 import db
from flask_login import UserMixin
from app2 import login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    twofa = db.Column(db.String(30))
    spell_queries = db.relationship('SpellQueries', backref='inquirer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_2fa(self, twofa):
        if self.twofa == twofa:
            return True
        return False

    def set_2fa(self, twofa):
        self.twofa = twofa

    def __repr__(self):
        return '<User {}>'.format(self.username)


class SpellQueries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return'<SpellQueries {}'.format(self.query)
