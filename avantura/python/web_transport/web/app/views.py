
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid

from .forms import LoginForm
from .models import User, ROLE_USER, ROLE_ADMIN
from .menu import create_main_menu
from .tables import create_table_content



@app.route('/')
def index():
    user = {'nickname' : 'Burgers'}
    #return render_template("index.html", title = 'Home', user = user)
    return render_template("storage.html", menu = create_main_menu())



@app.route('/login', methods=['GET', 'POST'])
#@oid.loginhandler
def login():
    #if g.user is not None and g.user.is_authenticated():
        #return redirect(url_for('index'))
    form = LoginForm()
    #if form.validate_on_submit():
        #session['remember_me'] = form.remember_me.data
        #return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template("login.html", title = 'sign in', form = form, providers = app.config['OPENID_PROVIDERS'])



@lm.user_loader
def load_user(user_id):
    return User.get(user_id)


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))






@app.route('/table')
def table():
    text = request.args.get('jsdata')

    #tmp_list = Table(['Наименование товара', 'Группа товара', 'Кол-во (по умолчанию)'], [[text, 'popa', i] for i in range(10)])
    
    return render_template('table.html', source=create_table_content(text))




