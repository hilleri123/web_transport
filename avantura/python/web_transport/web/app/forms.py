from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SelectField, IntegerField, SubmitField, DateTimeField
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
    currency_dollar = IntegerField('Курс доллара', validators = [_required])
    currency_euro = IntegerField('Курс евро', validators = [_required])
    comment = TextField('Комментарий', validators = [_required])
    author = TextField('Автор изменений', validators = [_required])
    form_name = "Добавить курсы валют"
