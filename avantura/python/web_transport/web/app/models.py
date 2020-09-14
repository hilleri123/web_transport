
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    client = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)



class Clients(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    brand = db.Column(db.String(256))
    #FIO
    Fname = db.Column(db.String(64))
    Iname = db.Column(db.String(64))
    Oname = db.Column(db.String(64))
    #nickname = db.Column(db.String(64), index = True, unique = True)
    phone = db.Column(db.String(32), nullable = True)
    email = db.Column(db.String(128), index = True, unique = True)
    comment = db.Column(db.String(2048), nullable = True)
    #role = db.Column(db.SmallInteger, default = ROLE_USER)

class Client_products(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    client = db.Column(db.Integer, db.ForeignKey('clients.id'))
    product = db.Column(db.Integer, db.ForeignKey('products.id'))
    count = db.Column(db.Integer)
    


class Client_rates(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    starts = db.Column(db.DateTime())
    client = db.Column(db.Integer, db.ForeignKey('clients.id'))
    product = db.Column(db.Integer, db.ForeignKey('product_groups.id'))
    price = db.Column(db.Float)
    





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
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True) #!!!!!!!!!!!!!!!!!!!!!!




class Product_groups(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), unique = True)




class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), unique = True)
    group_id = db.Column(db.Integer, db.ForeignKey('product_groups.id'))
    count = db.Column(db.Integer)





class Car_types(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    car_type = db.Column(db.String(256), unique = True)


class Car_numbers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.String(256), unique = True)
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







