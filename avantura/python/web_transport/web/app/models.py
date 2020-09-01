
from app import bd

ROLE_USER = 0
ROLE_ADMIN = 0

class User(bd.Model):
    id = bd.Column(bd.Integer,  primary_key = True)
    nickname = bd.Column(bd.String(64), index = True, unique = True)
    email = bd.Column(bd.String(120), index = True, unique = True)
    role = bd.Column(bd.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


