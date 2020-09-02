
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Product_groups(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))

    def get_visible_clm_names():
        return ['Группа товара']

    def get_visible_data():
        return [[i.name] for i in __class__.query.all()]

    def __repr__(self):
        return '<Product %r>' % (self.name)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    group_id = db.Column(db.Integer, db.ForeignKey('product_groups.id'))
    #group_name = db.Column(db.String(140))
    count = db.Column(db.Integer)

    def get_visible_clm_names():
        return ['Наименование товара', 'Группа товара', 'Кол-во (по умолчанию)']

    def get_visible_data():
        return [[i.name, i.group_id, i.count] for i in __class__.query.all()]

    def __repr__(self):
        return '<Product %r>' % (self.name)

