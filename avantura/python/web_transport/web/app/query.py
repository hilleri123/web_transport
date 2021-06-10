import sqlalchemy

from werkzeug.datastructures import MultiDict


from .models import *
from .forms import *

ROLE_USER = 0
ROLE_ADMIN = 1

class MainQueryHandler():
    table_html = 'table.html'
    form_html = 'form.html'

    def get_visible_table_name():
        return ''

    def inner_tables():
        return []

    def name():
        return ''

    def get_visible_tables():
        return []

    def get_visible_clm_names():
        return []

    def get_visible_data():
        return [[]]

    def add_row(form):
        pass

    def form(data=None, empty=False):
        return MyForm()


class QUser(MainQueryHandler):
    pass


class QClients(MainQueryHandler):
    def get_visible_table_name():
        return 'Клиенты'

    def inner_tables():
        return []
        #return ['clients_dilivery', 'clients_finances', 'clients_rates_and_products']

    def name():
        return 'clients'

    def get_visible_clm_names():
        return ['Маркировкa','Личные данные','Телефон', 'E-mail', 'Комментарий']


    def get_visible_data():
        return [[i.brand, ' '.join([i.Fname, i.Iname, i.Oname]), i.phone, i.email, i.comment] for i in Clients.query.all()]

    def add_row(form):
        tmp_client = Clients(brand=form.brand.data, Fname=form.Fname.data, Iname=form.Iname.data, Oname=form.Oname.data,
                phone=form.phone.data, email = form.email.data, comment = form.comment.data)
        try:
            db.session.add(tmp_client)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Clients try except!!!!!!") #!!!!!!!!!!

        tmp_finance = Finances(clients=tmp_client.id,  Progress_sum=0, Now_sum=0, Paid=0, Overall=0, Days=0)
        tmp_rates_and_products = Clients_rates_and_products(client_id=tmp_client.id)
        try:
            db.session.add(tmp_finance)
            db.session.add(tmp_rates_and_products)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Clients try except!!!!!!") #!!!!!!!!!!

        for rate in form.rates:
            try:
                db.session.add(Clients_rates_inner(rates_and_products_id = tmp_rates_and_products.id, product_group_id = rate.product_group_id.data,
                    price = rate.rate.data, currency_id = rate.currency.data))
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("Clients try except!!!!!!") #!!!!!!!!!!

        for product in form.products:
            try:
                db.session.add(Clients_products_inner(rates_and_products_id = tmp_rates_and_products.id, product_id = product.product_id.data, quanity = product.quanity.data))
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("Clients try except!!!!!!") #!!!!!!!!!!


    def form(data=None, empty=False):
        form = FClients()

        for i, product_group in enumerate(Product_groups.query.all()):
            if len(form.rates) != Product_groups.query.count() and not empty:
                rate = FClients_rate_inner()
                form.rates.append_entry(rate)
            rate = form.rates[i]
            if not empty:
                rate.product_group_id.data = product_group.id
                rate.product_group.data = product_group.name
                rate.rate.data = 0
            rate.currency.choices = [(i.id, i.currency_symbol) for i in Currency_types.query.all()]
            if len(form.rates.clm_names) <= 0:
                form.rates.clm_names = [i.label.text for i in [rate.product_group,rate.rate,rate.currency]]
        form.rates.table_name = 'Ставки по товарам'

        for i, product in enumerate(Products.query.all()):
            if len(form.products) != Products.query.count() and not empty:
                cl_product = FClients_product_inner()
                form.products.append_entry(cl_product)
            cl_product = form.products[i]
            if not empty:
                cl_product.product_id.data = product.id
                cl_product.product_name.data = product.name
                cl_product.quanity.data = product.quanity
            if len(form.products.clm_names) <= 0:
                form.products.clm_names = [i.label.text for i in [cl_product.checkbox, cl_product.product_name, cl_product.quanity]]
        form.products.table_name = 'Товары'

        return form

class QClients_delivery(MainQueryHandler):
    def get_visible_table_name():
        return 'Доставки'

    def name():
        return 'delivery'
        #return QClients.inner_tables()[0]

    def get_visible_clm_names():
        return ['Машина','Дата закрытия','Сумма','Закрыта']

    def get_visible_data():
         return [[i.car, i.date, i.price, i.close] for i in Clients_delivery.query.all()]

    def add_row(form):
        #tmp = Product_groups(name=form.data.get('name'))
        tmp = Clients(car=form.car.data, date=form.date.data, price=form.price.data, close=form.close.data)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Product_groups try except!!!!!!") #!!!!!!!!!!

    def form(data=None, empty=False):
        return FClients_delivery()

class QClients_finances(MainQueryHandler):
    def get_visible_table_name():
        return 'Финансы'

    def name():
        return 'aaa'
        #return QClients.inner_tables()[1]

    def get_visible_clm_names():
        return ['Дата','Сумма','Корректировка']

    def get_visible_data():
        return [[i.data, i.price, i.korrekt] for i in Clients_finances.query.all()]

    def form(data=None, empty=False):
        return FClients_finances()

class QClients_rates_and_products(MainQueryHandler):
    def get_visible_table_name():
        return 'Ставки и товары'

    def name():
        return 'bbb'
        #return QClients.inner_tables()[2]

    def get_visible_clm_names():
        return ['Дата начала действия','Дата оканчания действия','Комментарий']

    def get_visible_data():
        return [[i.date_start, i.date_end, i.comment] for i in Clients_rates_and_products.query.all()]

    def add_row(form):
        print("clients_rates_and_products")
        tmp = Clients_rates_and_products(date_start = form.date_start.data, comment = form.comment.data)

        for rate in form.rates:
            pass

        for product in form.products:
            pass

        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Clients try except!!!!!!") #!!!!!!!!!!

    def form(data=None, empty=False):
        form = FClients_rates_and_products()


        for i, product_group in enumerate(Product_groups.query.all()):
            if len(form.rates) != Product_groups.query.count() and not empty:
                rate = FClients_rate_inner()
                form.rates.append_entry(rate)
            rate = form.rates[i]
            if not empty:
                rate.product_group_id.data = product_group.id
                rate.product_group.data = product_group.name
                rate.rate.data = 0
            rate.currency.choices = [(i.id, i.currency_symbol) for i in Currency_types.query.all()]
            if len(form.rates.clm_names) <= 0:
                form.rates.clm_names = [i.label.text for i in [rate.product_group,rate.rate,rate.currency]]
        form.rates.table_name = 'Ставки по товарам'

        for i, product in enumerate(Products.query.all()):
            if len(form.products) != Products.query.count() and not empty:
                cl_product = FClients_product_inner()
                form.products.append_entry(cl_product)
            cl_product = form.products[i]
            if not empty:
                cl_product.product_id.data = product.id
                cl_product.product_name.data = product.name
                cl_product.quanity.data = product.quanity
            if len(form.products.clm_names) <= 0:
                form.products.clm_names = [i.label.text for i in [cl_product.checkbox, cl_product.product_name, cl_product.quanity]]
        form.products.table_name = 'Товары'

        return form




class QPrepared_cars(MainQueryHandler):
    def get_visible_table_name():
        return 'Предварительные машины'

    def inner_tables():
        return ['Prepared_cars_clients']

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

    def form(data=None, empty=False):
        res = FPrepared_cars()
        res.car_id.choices = [(i.id, i.number + " (" + Car_types.query.get(i.type_id).car_type + ")") for i in Car_numbers.query.all()]

        return res

class QPrepared_car_clients(MainQueryHandler):
    #form_html = 'prepared_car_clients_form.html'
    def get_visible_table_name():
        return 'Клиенты'

    def name():
        return QPrepared_cars.inner_tables()[0]

    def get_visible_clm_names():
        return ['Маркировкa','Сумма']

    def get_visible_data():
        return [[Clients.query.get(i.client).brand, i.price] for i in Prepared_cars_clients.query.all()]

    def add_row(form):
        tmp = Prepared_cars_clients(client=form.client.data, price=0)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Prepared_cars_clients try except!!!!!!") #!!!!!!!!!!

    def form(data=None, empty=False):
        form = FPrepared_car_clients()
        form.client.choices = [(i.id, i.brand) for i in Clients.query.all()]

        return form

class QPrepared_car_client_rates_and_products(MainQueryHandler):
    form_html = 'prepared_car_client_rates_and_products_form.html'
    def get_visible_table_name():
        return 'Ставки и товары'

    def name():
        return QPrepared_cars.inner_tables()[0]+'_inner'

    def add_row(form):
        tmp = Prepared_cars_clients(client=form.client.data, price=0)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Prepared_cars_clients try except!!!!!!") #!!!!!!!!!!

    def form(data=None, empty=False):
        form = FPrepared_car_clients_inner()

        for i, product_group in enumerate(Product_groups.query.all()):
            if len(form.rates) != Product_groups.query.count() and not empty:
                rate = FClients_rate_inner()
                form.rates.append_entry(rate)
            rate = form.rates[i]
            if not empty:
                rate.product_group_id.data = product_group.id
                rate.product_group.data = product_group.name
                rate.rate.data = 0
            rate.currency.choices = [(i.id, i.currency_symbol) for i in Currency_types.query.all()]
            if len(form.rates.clm_names) <= 0:
                form.rates.clm_names = [i.label.text for i in [rate.product_group,rate.rate,rate.currency]]
        form.rates.table_name = 'Ставки по товарам'

        for i, product in enumerate(Products.query.all()):
            if len(form.products) != Products.query.count() and not empty:
                cl_product = FClients_product_inner()
                form.products.append_entry(cl_product)
            cl_product = form.products[i]
            if not empty:
                cl_product.product_id.data = product.id
                cl_product.product_name.data = product.name
                cl_product.quanity.data = product.quanity
            if len(form.products.clm_names) <= 0:
                form.products.clm_names = [i.label.text for i in [cl_product.checkbox, cl_product.product_name, cl_product.quanity]]
        form.products.table_name = 'Товары'

        return form



class QSpent_cars(MainQueryHandler):
    def get_visible_table_name():
        return 'Закрытые машины'

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
    def get_visible_table_name():
        return 'Финансы'

    def name():
        return 'finances'

    def get_visible_clm_names():
        return ['Клиент Маркировкa(Маркировкa)','Сумма по машинам в пути($)','К оплате($)','Оплачено($)','Итого($)','Дней с разгрузки']

    def get_visible_data():
        return [[Clients.query.get(i.clients).brand, i.Progress_sum, i.Now_sum, i.Paid, i.Overall, i.Days] for i in Finances.query.all()]

    def add_row(form):
        tmp = Finances(clients=form.clients.data, Progress_sum=form.Progress_sum.data, Now_sum=form.Now_sum.data, Paid=form.Paid.data, Overall=form.Overall.data, Days=form.Days.data)
        try:
            db.session.add(tmp)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
                print("Finances try except!!!!!!") #!!!!!!!!!!
    def form(data=None, empty=False):
        return FFinances()



class QExchange_rates(MainQueryHandler):
    def get_visible_table_name():
        return 'Курсы валют'

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
    def form(data=None, empty=False):
        return FExchange_rates()


class QProduct_groups(MainQueryHandler):
    def get_visible_table_name():
        return 'Группы товаров'

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

    def form(data=None, empty=False):
        return FProduct_groups()



class QProducts(MainQueryHandler):
    def get_visible_table_name():
        return 'Товары'

    def name():
        return 'products'

    def get_visible_clm_names():
        return ['Наименование товара', 'Группа товара', 'Кол-во (по умолчанию)']

    def get_visible_data():
        return [[i.name, Product_groups.query.get(i.group_id).name, i.quanity] for i in Products.query.all()]

    def add_row(form):
        value = dict(form.group.choices).get(form.group.data)
        tmp = Products(name=form.name.data, group_id=form.group.data, quanity=form.quanity.data)
        #tmp1 = Clients_rates_and_products_table2(on = False,  product=len(Products.query.all())+1, quanity=len(Products.query.all())+1)
        try:
            db.session.add(tmp)
            #db.session.add(tmp1)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Products try except!!!!!!") #!!!!!!!!!!

    def form(data=None, empty=False):
        res = FProducts()
        res.group.choices = [(i.id, i.name) for i in Product_groups.query.all()]
        return res




class QCar_types(MainQueryHandler):
    def get_visible_table_name():
        return 'Типы машин'

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

    def form(data=None, empty=False):
        return FCar_types()


class QCar_numbers(MainQueryHandler):
    def get_visible_table_name():
        return 'Номера машин'

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

    def form(data=None, empty=False):
        res = FCar_numbers()
        res.car_type.choices = [(i.id, i.car_type) for i in Car_types.query.all()]
        return res



class QAdmin_employees(MainQueryHandler):
    def get_visible_table_name():
        return ''

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
    def get_visible_table_name():
        return ''

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
    def get_visible_table_name():
        return ''

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
