from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SelectField, IntegerField, SubmitField
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


