from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SelectField, IntegerField, SubmitField, RadioField, FloatField, FieldList, FormField, DateTimeField, PasswordField
from wtforms.validators import Required, ValidationError, Email, EqualTo

from .models import User


def _required(form, field):
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError('Field is required')

class MyForm(FlaskForm):
    class Meta:
        csrf = True
    submit = SubmitField('Ok')
    cancel = SubmitField('Cancel')
    form_name = 'form name'


class LoginForm(FlaskForm):
    email = TextField('E-mail', validators = [Required(), Email()])
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
    username = TextField('Username', validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])
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




class FClient_rates(FlaskForm):
    product_group = ''
    product_group_id = None
    price = FloatField('Цена', validators = [_required])


class FClient_products(FlaskForm):
    product = RadioField('Включить')
    product = ''
    product_id = None
    price = FloatField('Кол-во', validators = [_required])



class FClients(MyForm):
    brand = TextField('Наименование', validators = [_required])
    Fname = TextField('Фамилия', validators = [_required])
    Iname = TextField('Имя', validators = [_required])
    Oname = TextField('Отчество', validators = [_required])
    phone = TextField('Телефон', validators = [_required])
    email = TextField('E-mail', validators = [_required])
    comment = TextField('Комментарий', validators = [_required])
    rates = FieldList(FormField(FClient_rates))
    form_name = "Добавить клиента"




class FProducts(MyForm):
    name = TextField('Наименование', validators = [_required])
    group = SelectField('Группа товаров', validators = [_required])
    count = IntegerField('Кол-во на паллете', validators = [_required])
    form_name = "Добавить товар"

class FProduct_groups(MyForm):
    name = TextField('Группа товаров', validators = [_required])
    form_name = "Добавить группу товаров"


class FCar_types(MyForm):
    car_type = TextField('Тип машины', validators = [_required])
    form_name = "Добавить тип машины"


class FCar_numbers(MyForm):
    number = TextField('Номер машины', validators = [_required])
    car_type = SelectField('Тип машины', validators = [_required])
    form_name = "Добавить машину"

class FExchange_rates(MyForm):
    date = DateTimeField('Дата', validators = [_required])
    currency_dollar = FloatField('Курс доллара', validators = [_required])
    currency_euro = FloatField('Курс евро', validators = [_required])
    comment = TextField('Комментарий', validators = [_required])
    author = TextField('Автор изменений', validators = [_required])
    form_name = "Добавить курс валют"

class FPrepared_cars(MyForm):
    car = SelectField('Номер машины', validators = [_required])
    id_type = SelectField('Тип машины', validators = [_required])
    date_in = DateTimeField('Дата поступления', validators = [_required])
    form_name = "Добавить Машину"
