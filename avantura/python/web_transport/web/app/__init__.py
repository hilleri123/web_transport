
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)



lm = LoginManager()
lm.session_protection = 'strong'
lm.init_app(app)
lm.login_view = 'login'
#oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models


try:
    tmp_user = models.User(email='aa@a.ru', nickname='aaa_norm', client=1, role=1)
    tmp_user.password = "123"
    db.session.add(tmp_user)
    db.session.commit()
except:
    pass

try:
    tmp_currency = {'Доллар':'$', 'Евро':'&', 'Руболь':'Р'}
    for name, symbol in tmp_currency.items():
        tmp = models.Currency_types(currency_name=name, currency_symbol=symbol)
        db.session.add(tmp)
        db.session.commit()
except:
    pass





