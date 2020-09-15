
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid

from .forms import LoginForm
from .models import User, ROLE_USER, ROLE_ADMIN
from .menu import create_main_menu
from .tables import create_table_content, add_to_table, create_table_edit_form, table_html, form_html



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
    #return render_template("login.html", title = 'sign in', form = form, providers = app.config['OPENID_PROVIDERS'])
    return render_template("login.html", title = 'sign in', form = form)



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




@app.route('/table-add', methods=['GET', 'POST'])
def table_add():
    dbname = request.args.get('dbname')
    text_element = request.args.get('text_element')

    flash(text_element)
    add_to_table(dbname, text_element)

    return ('', 204)



@app.route('/table')
def table():
    dbname = request.args.get('dbname')

    return render_template(table_html(dbname), source=create_table_content(dbname))


@app.route('/table-edit-form', methods=['GET', 'POST'])
def table_edit_form():
    dbname = request.args.get('dbname')

    return render_template(form_html(dbname), form=create_table_edit_form(dbname), dbname=dbname)


@app.route('/api/add', methods=['GET', 'POST'])
def add_function():
    dbname = request.args.get('dbname')
    form = create_table_edit_form(dbname)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.cancel.data:
                return ('', 204) #!!!!!!!!НАДО ЗАКРЫТЬ ОКНО
            add_to_table(dbname, form)

    return ('', 204)

