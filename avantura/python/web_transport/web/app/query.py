import sqlalchemy

from .models import *
from .forms import *

ROLE_USER = 0
ROLE_ADMIN = 1

class QUser():
    pass


class QClients():
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




class QCars():
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



class QPrepared_cars():
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



class QSpent_cars():
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



class QFinances():
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



class QExchange_rates():
    def get_visible_clm_names():
        return ['Дата', 'Курс доллара', 'Курс евро', 'Комментарий', 'Автор изменений']

    def get_visible_data():
        return [[i.date, i.dollar, i.euro, i.comment, i.author] for i in __class__.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        #tmp = __class__(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        #db.session.add(tmp)
        #db.session.commit()



class QProduct_groups():
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



class QProducts():
    def name():
        return 'products'

    def get_visible_clm_names():
        return ['Наименование товара', 'Группа товара', 'Кол-во (по умолчанию)']

    def get_visible_data():
        return [[i.name, Product_groups.query.get(i.group_id).name, i.count] for i in Products.query.all()]

    def add_row(form):
        print('Adding', form)
        value = dict(form.group.choices).get(form.group.data)
        print(form.group.choices, form.group.data)
        print(value)
        #spliter = '@'
        #tmp_list = text.split('@')
        tmp = Products(name=form.name.data, group_id=form.group.data, count=form.count.data)
        db.session.add(tmp)
        db.session.commit()

    def form():
        res = FProducts()
        res.group.choices = [(i.id, i.name) for i in Product_groups.query.all()]
        return res




class QCar_types():
    def get_visible_clm_names():
        return ['Тип машины']

    def get_visible_data():
        return [[i.type] for i in Car_types.query.all()]

    def add_row(form):
        print('Adding', form)
        tmp = Car_types(type=form.name.data)
        db.session.add(tmp)
        db.session.commit()


class QCar_numbers():
    def get_visible_clm_names():
        return ['Номер машины', 'Тип машины']

    def get_visible_data():
        return [[i.number, i.type_id] for i in Car_numbers.query.all()]

    def add_row(text = ''):
        print('Adding', text)
        spliter = '@'
        tmp_list = text.split('@')
        #tmp = Car_numbers(name=tmp_list[0], group_name=tmp_list[1], count=int(tmp_list[2]))
        #db.session.add(tmp)
        #db.session.commit()



class QAdmin_employees():
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




class QAdmin_clients():
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






class QAdmin():
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







