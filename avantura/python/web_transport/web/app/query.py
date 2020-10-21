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

    def form():
        return MyForm()


class QUser(MainQueryHandler):
    pass


class QClients(MainQueryHandler):
    #form_html = 'clients_form.html'
    def get_visible_table_name():
        return 'Клиенты'

    def inner_tables():
        return ['clients_dilivery', 'clients_finances', 'clients_rates_and_products']

    def name():
        return 'clients'

    def get_visible_clm_names():
        return ['Маркировкa','Личные данные','Телефон', 'E-mail', 'Комментарий']


    def get_visible_data():
        return [[i.brand, ' '.join([i.Fname, i.Iname, i.Oname]), i.phone, i.email, i.comment] for i in Clients.query.all()]

    def add_row(form):
        tmp = Clients(brand=form.brand.data, Fname=form.Fname.data, Iname=form.Iname.data, Oname=form.Oname.data, phone=form.phone.data, email = form.email.data, comment = form.comment.data)
        tmp1 = Finances(clients=len(Clients.query.all())+1,  Progress_sum=0, Now_sum=0, Paid=0, Overall=0, Days=0)
        try:
            db.session.add(tmp)
            db.session.add(tmp1)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Clients try except!!!!!!") #!!!!!!!!!!

    def form():
        return FClients()

class QClients_delivery(MainQueryHandler):
    def get_visible_table_name():
        return 'Доставки'

    def name():
        return QClients.inner_tables()[0]

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

    def form():
        return FClients_delivery()

class QClients_finances(MainQueryHandler):
    def get_visible_table_name():
        return 'Финансы'

    def name():
        return QClients.inner_tables()[1]

    def get_visible_clm_names():
        return ['Дата','Сумма','Корректировка']

    def get_visible_data():
        return [[i.data, i.price, i.korrekt] for i in Clients_finances.query.all()]

    def form():
        return FClients_finances()

class QClients_rates_and_products(MainQueryHandler):
    def get_visible_table_name():
        return 'Ставки и товары'

    def name():
        return QClients.inner_tables()[2]

    def get_visible_clm_names():
        return ['Дата начала действия','Дата оканчания действия','Комментарий']

    def get_visible_data():
        return [[i.data_start, i.data_end, i.comment] for i in Clients_rates_and_products.query.all()]

    def add_row(form):
        tmp = Clients(brand=form.brand.data, Fname=form.Fname.data, Iname=form.Iname.data, Oname=form.Oname.data, phone=form.phone.data, email = form.email.data, comment = form.comment.data)
        tmp1 = Finances(clients=len(Clients.query.all())+1,  Progress_sum=0, Now_sum=0, Paid=0, Overall=0, Days=0)
        try:
            db.session.add(tmp)
            db.session.add(tmp1)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Clients try except!!!!!!") #!!!!!!!!!!

    def form():
        form = FClients_rates_and_products()

        for product_group in Product_groups.query.all():
            rate = FClients_rate_inner()
            form.rates.append_entry(rate)
            rate = form.rates[-1]
            rate.product_group_id.data = product_group.id
            rate.product_group.data = product_group.name
            rate.rate.data = 0
            rate.currency.choices = [(i.id, i.currency_symbol) for i in Currency_types.query.all()]
            if len(form.rates.clm_names) <= 0:
                form.rates.clm_names = [i.label.text for i in [rate.product_group,rate.rate,rate.currency]]
        form.rates.table_name = 'Ставки по товарам'

        for product in Products.query.all():
            cl_product = FClients_product_inner()
            form.products.append_entry(cl_product)
            cl_product = form.products[-1]
            cl_product.product_id.data = product.id
            cl_product.product_name.data = product.name
            cl_product.quanity.data = product.quanity
            if len(form.products.clm_names) <= 0:
                form.products.clm_names = [i.label.text for i in [cl_product.checkbox, cl_product.product_name, cl_product.quanity]]
        form.products.table_name = 'Товары'

        return form



    # def get_visible_data():
    #     return [[i.group_tovar, i.stavka, i.currency] for i in stavki.query.all()]
    #
    # # def add_row(form):
    #     tmp = Stavki(group_tovar=form.group_tovar.data, stavka=form.stavka.data, currency=form.currency.data)
    #     try:
    #         db.session.add(tmp)
    #         db.session.commit()
    #     except sqlalchemy.exc.IntegrityError:
    #             print("stavki try except!!!!!!") #!!!!!!!!!!
    # def form():
    #     return FStavki()

class QSpisokTovarov(MainQueryHandler):
    def get_visible_table_name():
        return 'Список товаров'

    def name():
        return 'SpisokTovarov'

    def get_visible_clm_names():
        return ['№', 'Товар', 'Кол-во на паллете']

    # def get_visible_data():
    #     return [[i.number, i.tovar, i.quanity] for i in SpisokTovarov.query.all()]
    #
    # def add_row(form):
    #     tmp = SpisokTovarov(number=form.number.data, tovar=form.tovar.data, quanity=form.quanity.data)
    #     try:
    #         db.session.add(tmp)
    #         db.session.commit()
    #     except sqlalchemy.exc.IntegrityError:
    #             print("SpisokTovarov try except!!!!!!") #!!!!!!!!!!
    # def form():
    #     return FSpisokTovarov()

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

    def form():
        res = FPrepared_cars()
        res.car_id.choices = [(i.id, i.number + " (" + Car_types.query.get(i.type_id).car_type + ")") for i in Car_numbers.query.all()]
        return res

class QPrepared_cars_clients(MainQueryHandler):
    def get_visible_table_name():
        return 'Клиенты'

    def inner_tables():
        return ['Prepared_cars_clients_stavka', 'Prepared_cars_clients_spisok']

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

    def form():
        res = FPrepared_cars_clients()
        res.client.choices = [(i.id, i.brand) for i in Clients.query.all()]
        return res

class QPrepared_cars_clients_stavka(MainQueryHandler):
    def get_visible_table_name():
        return 'Ставки'

    def name():
        return QPrepared_cars_clients.inner_tables()[1]

    def get_visible_clm_names():
        return ['Группа товаров','Ставка','Общий вес, кол-во', 'Итого($)']

    def get_visible_data():
        return [[i.product_type, i.price, i.weight, i.price] for i in Prepared_cars_clients_stavka.query.all()]

class QPrepared_cars_clients_spisok(MainQueryHandler):
    def get_visible_table_name():
        return 'Список товаров'

    def name():
        return QPrepared_cars_clients.inner_tables()[0]

    def get_visible_clm_names():
        return ['Товар','Кол-во на паллете', 'Вес, кол-во', 'Объем','Сумма($)']

    def get_visible_data():
        return [[i.product, i.quanity, i.weight, i.weight_final, i.cost] for i in Prepared_cars_clients_spisok.query.all()]

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
    def form():
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
    def form():
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
        tmp1 =Clients_rates_and_products_table1( product_type = len(Product_groups.query.all())+1,  price=0, currency="$")
        try:
            db.session.add(tmp)
            db.session.add(tmp1)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Product_groups try except!!!!!!") #!!!!!!!!!!

    def form():
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

    def form():
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

    def form():
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

    def form():
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
