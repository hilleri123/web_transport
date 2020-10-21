
from app import db

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import db, lm


ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    email = db.Column(db.String(128), index = True, unique = True)
    nickname = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    client = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



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

class Clients_rates_and_products(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    date_start = db.Column(db.DateTime())
    date_end = db.Column(db.DateTime(), nullable = True)
    comment = db.Column(db.String(2048), nullable = True)

class Currency_types(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    currency_name = db.Column(db.String(64), unique = True)
    currency_symbol = db.Column(db.String(8), unique = True)
    


class Clients_rates_inner(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    rates_and_products_id = db.Column(db.Integer, db.ForeignKey('clients_rates_and_products.id'))
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_groups.id'))
    price = db.Column(db.Float)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency_types.id'))

class Clients_products_inner(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    rates_and_products_id = db.Column(db.Integer, db.ForeignKey('clients_rates_and_products.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quanity = db.Column(db.Float)

#delal grisha
class Prepared_cars_clients(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    client = db.Column(db.Integer, db.ForeignKey('clients.id'))
    price = db.Column(db.String(256))

#delal grisha
class Prepared_cars_clients_stavka(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    product_type = db.Column(db.Integer, db.ForeignKey('product_groups.id'))
    price = db.Column(db.Float)
    weight = db.Column(db.Float)
    cost = db.Column(db.Float)

#delal grisha
class Prepared_cars_clients_spisok(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    on = db.Column(db.Boolean)
    product = db.Column(db.String(256))
    quanity = db.Column(db.Float)
    weight = db.Column(db.Float)
    weight_final = db.Column(db.Float)
    cost = db.Column(db.Float)

#delal grisha
class Clients_finances(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    data = db.Column(db.DateTime())
    price = db.Column(db.Float)
    korrekt =db.Column(db.Boolean)

#delal grisha
class Clients_delivery(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    car = db.Column(db.Integer, db.ForeignKey('car_numbers.id'))
    date = db.Column(db.DateTime())
    price = db.Column(db.Float)
    close = db.Column(db.Boolean)


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
    car_id =  db.Column(db.Integer, db.ForeignKey('car_numbers.id'))
    date_in = db.Column(db.DateTime())
    date_out = db.Column(db.DateTime(), nullable = True)



class Finances(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    clients = db.Column(db.Integer, db.ForeignKey('clients.id'))
    Progress_sum = db.Column(db.Integer)
    Now_sum = db.Column(db.Integer)
    Paid = db.Column(db.Integer)
    Overall = db.Column(db.Integer)
    Days = db.Column(db.Integer)



class Exchange_rates(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime())
    currency_dollar = db.Column(db.Float())
    currency_euro = db.Column(db.Float())
    comment = db.Column(db.String(2048), nullable = True)
    author = db.Column(db.String(256), db.ForeignKey('user.id')) #!!!!!!!!!!!!!!!!!!!!!!




class Product_groups(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), unique = True)




class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), unique = True)
    group_id = db.Column(db.Integer, db.ForeignKey('product_groups.id'))
    quanity = db.Column(db.Integer)




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
