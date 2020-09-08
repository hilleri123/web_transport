
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)



class Clients(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)




class Cars(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    date_in = db.Column(db.DateTime())
    date_out = db.Column(db.DateTime(), nullable = True)
    car_id = db.Column(db.Integer, db.ForeignKey('car_numbers.id'))




class Finances(db.Model):
    id = db.Column(db.Integer, primary_key = True)



class Exchange_rates(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime())
    dollar = db.Column(db.Float())
    euro = db.Column(db.Float())
    comment = db.Column(db.String(2048), nullable = True)
    author = db.Column(db.Integer, db.ForeignKey('user.id')) #!!!!!!!!!!!!!!!!!!!!!!




class Product_groups(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), unique = True)




class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256))
    group_id = db.Column(db.Integer, db.ForeignKey('product_groups.id'))
    count = db.Column(db.Integer)





class Car_types(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    car_type = db.Column(db.String(256))


class Car_numbers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.String(256))
    type_id = db.Column(db.Integer, db.ForeignKey('car_types.id'))


class Handbooks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    handbook = db.Column(db.String(256))
    handbook_id = db.Column(db.Integer)
    date = db.Column(db.DateTime())
    type_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    source = db.Column(db.String(2048), nullable = True)
    change = db.Column(db.String(2048))



class Admin_employees(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.String(256))
    type_id = db.Column(db.Integer, db.ForeignKey('car_types.id'))



class Admin_clients(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.String(256))
    type_id = db.Column(db.Integer, db.ForeignKey('car_types.id'))






class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.String(256))
    type_id = db.Column(db.Integer, db.ForeignKey('car_types.id'))







