from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SelectField, IntegerField, SubmitField, RadioField, FloatField, FieldList, FormField
from wtforms.validators import Required, ValidationError


def _required(form, field):
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError('Field is required')

class MyForm(FlaskForm):
    class Meta:
        csrf = True
    submit = SubmitField('Ok')
    cancel = SubmitField('Cancel')
    form_name = 'form name'
    

class LoginForm(MyForm):
    openid = TextField('openid', validators = [_required])
    remember_me = BooleanField('remember_me', default = False)
    form_name = ""


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


