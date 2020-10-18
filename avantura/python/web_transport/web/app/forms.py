from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, SubmitField, RadioField, FloatField, FieldList, FormField, DateTimeField, PasswordField, HiddenField
from wtforms.validators import Required, ValidationError, Email, EqualTo

from wtforms.fields.html5 import DateTimeLocalField

from datetime import datetime

from .models import User


def _required(form, field):
    print(field, bool(not field.raw_data or not field.raw_data[0]))
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError('Field is required')

class MyForm(FlaskForm):
    class Meta:
        csrf = True
    submit = SubmitField('Ok')
    cancel = SubmitField('Cancel')
    form_name = 'form name'

class MyFieldList(FieldList):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.clm_names = []
    


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators = [Required(), Email()])
    password = PasswordField('passwprd', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    submit = SubmitField('Log in')
    #form_name = "login"

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('Unknown email')
            return False
        if not user.verify_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    confirm = PasswordField('Verify password', validators=[Required(), EqualTo('password', message='Passwords must match')])
    remember_me = BooleanField('remember_me', default = False)
    submit = SubmitField('Log in')


    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True




class FClients_delivery(MyForm):
    form_name = "Доставки"

class FClients_finances(MyForm):
    form_name = "Финансы"

class FClients_rate_inner(FlaskForm):
    product_group = StringField('Группа товаров')
    #product_group_id = HiddenField('Id группы товаров')
    rate = FloatField('Ставка', validators = [_required])
    currency = SelectField('Валюта', validators = [_required])


class FClients_product_inner(FlaskForm):
    checkbox = BooleanField('Включение')
    product_name = StringField('Товар')
    #product_id = HiddenField('Id товара')
    count = IntegerField('Кол-во на паллете')


class FClients_rates_and_products(MyForm):
    data_start = DateTimeLocalField('Дата начала', default=datetime.today, format='%Y-%m-%dT%H:%M')
    rates = MyFieldList(FormField(FClients_rate_inner))
    products = MyFieldList(FormField(FClients_product_inner))
    comment = StringField('Комментарий', validators = [_required])
    form_name = "Ставки и товары"


class FClients(MyForm):
    brand = StringField('Наименование', validators = [_required])
    Fname = StringField('Фамилия', validators = [_required])
    Iname = StringField('Имя', validators = [_required])
    Oname = StringField('Отчество', validators = [_required])
    phone = StringField('Телефон', validators = [_required])
    email = StringField('E-mail', validators = [_required])
    comment = StringField('Комментарий', validators = [_required])
    form_name = "Добавить клиента"

class FFinances(MyForm):
    clients = StringField('Наименование', validators = [_required])
    Progress_sum = IntegerField('Наименование', validators = [_required])
    Now_sum = IntegerField('Наименование', validators = [_required])
    Paid = IntegerField('Наименование', validators = [_required])
    Overall = IntegerField('Наименование', validators = [_required])
    Days = IntegerField('Наименование', validators = [_required])


class FProducts(MyForm):
    name = StringField('Наименование', validators = [_required])
    group = SelectField('Группа товаров', validators = [_required])
    count = IntegerField('Кол-во на паллете', validators = [_required])
    form_name = "Добавить товар"

class FProduct_groups(MyForm):
    name = StringField('Группа товаров', validators = [_required])
    form_name = "Добавить группу товаров"


class FCar_types(MyForm):
    car_type = StringField('Тип машины', validators = [_required])
    form_name = "Добавить тип машины"


class FCar_numbers(MyForm):
    number = StringField('Номер машины', validators = [_required])
    car_type = SelectField('Тип машины', validators = [_required])
    form_name = "Добавить машину"

class FExchange_rates(MyForm):
    date = DateTimeField('Дата', validators = [_required])
    currency_dollar = FloatField('Курс доллара', validators = [_required])
    currency_euro = FloatField('Курс евро', validators = [_required])
    comment = StringField('Комментарий', validators = [_required])
    author = StringField('Автор изменений', validators = [_required])
    form_name = "Добавить курс валют"

class FPrepared_cars(MyForm):
    car_id = SelectField('Номер машины', validators = [_required])
    date_in = DateTimeLocalField('Дата поступления', default=datetime.today, format='%Y-%m-%dT%H:%M')
    form_name = "Добавить Машину"

class FPrepared_cars_clients(MyForm):
    client = SelectField('Наименование', validators = [_required])
    form_name = "Добавить клиента"
