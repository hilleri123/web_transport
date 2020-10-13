import sqlalchemy

from .models import *
from .forms import *

ROLE_USER = 0
ROLE_ADMIN = 1

class MainQueryHandler():
    table_html = 'table.html'
    form_html = 'form.html'

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
    form_html = 'Clients_form_1.html'

    def name():
        return 'clients'

    def get_visible_clm_names():
        return ['Маркировкa','Личные данные','Телефон', 'E-mail', 'Комментарий']


    def get_visible_data():
        return [[i.brand, ' '.join([i.Fname, i.Iname, i.Oname]), i.phone, i.email, i.comment] for i in Clients.query.all()]

    def add_row(form):
        #tmp = Product_groups(name=form.data.get('name'))
        tmp = Clients(brand=form.brand.data, Fname=form.Fname.data, Iname=form.Iname.data, Oname=form.Oname.data, phone=form.phone.data, email = form.email.data, comment = form.comment.data)
        tmp1 = Finances(clients=form.brand.data,  Progress_sum='0', Now_sum='0', Paid='0', Overall='0', Days='0')
        try:
            db.session.add(tmp)
            db.session.add(tmp1)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Product_groups try except!!!!!!") #!!!!!!!!!!

    def form():
        return FClients()

class QClients_redakt1(MainQueryHandler):
    def name():
        return 'redakt1'

    def get_visible_clm_names():
        return ['Машина','Дата закрытия','Сумма','Закрыта']

    # def get_visible_data():
    #     return [[i.brand, ' '.join([i.Fname, i.Iname, i.Oname]), i.phone, i.email, i.comment] for i in Clients.query.all()]

class QClients_redakt2(MainQueryHandler):
    def name():
        return 'redakt2'

    def get_visible_clm_names():
        return ['Дата','Сумма','Корректировка']

    # def get_visible_data():
    #     return [[i.brand, ' '.join([i.Fname, i.Iname, i.Oname]), i.phone, i.email, i.comment] for i in Clients.query.all()]

class QClients_redakt3(MainQueryHandler):
    def name():
        return 'redakt3'

    def get_visible_clm_names():
        return ['Дата начала действия','Дата оканчания действия','Комментарий']

    # def get_visible_data():
    #     return [[i.brand, ' '.join([i.Fname, i.Iname, i.Oname]), i.phone, i.email, i.comment] for i in Clients.query.all()]



class QPrepared_cars(MainQueryHandler):
    def name():
        return 'prepared_cars'

    def get_visible_clm_names():
        return ['Машина', 'Тип машины', 'Дата поступления']

    def get_visible_data():
        return [[Car_numbers.query.get(i.car_id).number,
                    Car_types.query.get(Car_numbers.query.get(i.car_id).type_id).car_type,
                    i.date_in] for i in Cars.query.filter(Cars.date_out.is_(None))]

    def add_row(form):
        tmp = Cars(car_id=form.car_id.data, date_in=form.date_in.data)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
                print("Prepared_cars try except!!!!!!") #!!!!!!!!!!

    def form():
        res = FPrepared_cars()
        res.car_id.choices = [(i.id, i.number + " (" + Car_types.query.get(i.type_id).car_type + ")") for i in Car_numbers.query.all()]
        return res


class QSpent_cars(MainQueryHandler):
    def name():
        return 'spent_cars'
    def get_visible_clm_names():
        return ['№', 'Машина', 'Тип машины', 'Дата закрытия']

    def get_visible_data():
        return [[Car_numbers.query.get(i.car_id).number,
                    Car_types.query.get(Car_numbers.query.get(i.car_id).type_id).car_type,
                    i.date_in, i.date_out] for i in Cars.query.filter(Cars.date_out.isnot(None))]

    def add_row(form):
        pass
        #tmp = Exchange_rates(car=form.car.data, id_type=form.id_type.data, date_out=form.date_out.data)
        #try:
            #db.session.add(tmp)
            #db.session.commit()
        #except sqlalchemy.exc.IntegrityError:
                #print("Spent_cars try except!!!!!!") #!!!!!!!!!!




class QFinances(MainQueryHandler):
    def name():
        return 'finances'

    def get_visible_clm_names():
        return ['Клиент Маркировкa(Маркировкa)','Сумма по машинам в пути($)','К оплате($)','Оплачено($)','Итого($)','Дней с разгрузки']

    def get_visible_data():
        return [[i.clients, i.Progress_sum, i.Now_sum, i.Paid, i.Overall, i.Days] for i in Finances.query.all()]

    def add_row(form):
        tmp = Finances(clients=form.clients.data, Progress_sum=form.Progress_sum.data, Now_sum=form.Now_sum.data, Paid=form.Paid.data, Overall=form.Overall.data, Days=form.Days.data)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
                print("Finances try except!!!!!!") #!!!!!!!!!!
    def form():
        return FFinances()



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
