import sqlalchemy

from .models import *
from .forms import *

ROLE_USER = 0
ROLE_ADMIN = 1

class MainQueryHandler():
    def name():
        return ''

    def get_visible_clm_names():
        return []

    def get_visible_data():
        return [[]]

    def add_row(form):
        pass

    def form():
        return MyForm()


class QUser(MainQueryHandler):
    pass


class QClients(MainQueryHandler):
    def get_visible_clm_names():
        return ['Группа товара']

    def get_visible_data():
        return [[i.name] for i in __class__.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        db.session.add(tmp)
        db.session.commit()




class QCars(MainQueryHandler):
    def name():
        return 'cars'

    def get_visible_clm_names():
        return ['Машина', 'Тип машины', 'Дата поступления', 'Дата закрытия']

    def get_visible_data():
        return [[i.car_id] for i in __class__.query.all()]

    def add_row(text = ''):
        spliter = '@'
        tmp_list = text.split('@')
        tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        db.session.add(tmp)
        db.session.commit()



class QPrepared_cars(MainQueryHandler):
    def name():
        return 'prepared_cars'

    def get_visible_clm_names():
        return ['Машина', 'Тип машины', 'Дата поступления', 'Дата закрытия']

    def get_visible_data():
        return [[i.name] for i in Cars.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        db.session.add(tmp)
        db.session.commit()



class QSpent_cars(MainQueryHandler):
    def get_visible_clm_names():
        return ['Машина', 'Тип машины', 'Дата поступления', 'Дата закрытия']

    def get_visible_data():
        return [[i.name] for i in __class__.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        db.session.add(tmp)
        db.session.commit()



class QFinances(MainQueryHandler):
    def get_visible_clm_names():
        return ['Группа товара']

    def get_visible_data():
        return [[i.name] for i in __class__.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        db.session.add(tmp)
        db.session.commit()



class QExchange_rates(MainQueryHandler):
    def name():
        return 'exchange_rates'

    def get_visible_clm_names():
        return ['Дата', 'Курс доллара', 'Курс евро', 'Комментарий', 'Автор изменений']

    def get_visible_data():
        return [[i.date, i.currency_dollar, i.currency_euro, i.comment, i.author] for i in Exchange_rates.query.all()]

    def add_row(form):
        tmp = Exchange_rates(date=form.date.data, currency_dollar=form.currency_dollar.data, currency_euro=form.currency_euro.data, comment=form.comment.data, author=form.author.data)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
                print("Exchange_rates try except!!!!!!") #!!!!!!!!!!
    def form():
        return FExchange_rates()


class QProduct_groups(MainQueryHandler):
    def name():
        return 'product_groups'

    def get_visible_clm_names():
        return ['Группа товара']

    def get_visible_data():
        return [[i.name] for i in Product_groups.query.all()]

    def add_row(form):
        tmp = Product_groups(name=form.data.get('name'))
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Product_groups try except!!!!!!") #!!!!!!!!!!

    def form():
        return FProduct_groups()



class QProducts(MainQueryHandler):
    def name():
        return 'products'

    def get_visible_clm_names():
        return ['Наименование товара', 'Группа товара', 'Кол-во (по умолчанию)']

    def get_visible_data():
        return [[i.name, Product_groups.query.get(i.group_id).name, i.count] for i in Products.query.all()]

    def add_row(form):
        value = dict(form.group.choices).get(form.group.data)
        tmp = Products(name=form.name.data, group_id=form.group.data, count=form.count.data)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Products try except!!!!!!") #!!!!!!!!!!

    def form():
        res = FProducts()
        res.group.choices = [(i.id, i.name) for i in Product_groups.query.all()]
        return res




class QCar_types(MainQueryHandler):
    def name():
        return 'car_types'

    def get_visible_clm_names():
        return ['Тип машины']

    def get_visible_data():
        return [[i.car_type] for i in Car_types.query.all()]

    def add_row(form):
        tmp = Car_types(car_type=form.car_type.data)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Car_types try except!!!!!!") #!!!!!!!!!!

    def form():
        return FCar_types()


class QCar_numbers(MainQueryHandler):
    def name():
        return 'car_numbers'

    def get_visible_clm_names():
        return ['Номер машины', 'Тип машины']

    def get_visible_data():
        return [[i.number, Car_types.query.get(i.type_id).car_type] for i in Car_numbers.query.all()]

    def add_row(form):
        tmp = Car_numbers(number=form.number.data, type_id=form.car_type.data)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Car_numbers try except!!!!!!") #!!!!!!!!!!

    def form():
        res = FCar_numbers()
        res.car_type.choices = [(i.id, i.car_type) for i in Car_types.query.all()]
        return res



class QAdmin_employees(MainQueryHandler):
    def name():
        return 'admin_employees'

    def get_visible_clm_names():
        return ['Группа товара']

    def get_visible_data():
        return [[i.name] for i in __class__.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        db.session.add(tmp)
        db.session.commit()




class QAdmin_clients(MainQueryHandler):
    def name():
        return 'admin_clients'

    def get_visible_clm_names():
        return ['Группа товара']

    def get_visible_data():
        return [[i.name] for i in __class__.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        db.session.add(tmp)
        db.session.commit()






class QAdmin(MainQueryHandler):
    def name():
        return 'admin'

    def get_visible_clm_names():
        return ['Группа товара']

    def get_visible_data():
        return [[i.name] for i in __class__.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        db.session.add(tmp)
        db.session.commit()
