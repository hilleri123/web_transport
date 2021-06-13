
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm

import time

from .forms import LoginForm
from .models import User, ROLE_USER, ROLE_ADMIN
from .menu import create_main_menu
from .tables import create_table_content, add_to_table, create_table_edit_form, table_html, form_html, create_inner_tables



@app.route('/')
#@login_required
def index():
    #user = {'nickname' : 'Burgers'}
    #return render_template("index.html", title = 'Home', user = user)
    try:
        if session['nickname'] == None:
            redirect_url = '/login'
            return redirect(redirect_url)
        user = current_user
        return render_template("storage.html", menu = create_main_menu(), username = session['nickname'])
    except:
        redirect_url = '/login'
        return redirect(redirect_url)



class lmUser:
    def __init__(self, db_id, active = True):
        self.is_active = active
        self.db_user = User.query.get(db_id)

    def get_id(self):
        self.db_user.id

@app.route('/login', methods=['GET', 'POST'])
#@oid.loginhandler
def login():
    form = LoginForm()

    #print(request.method, form.validate())
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user is None and user.verify_password(form.password.data):
            login_user(lmUser(user.id))
            #redirect_url = request.args.get('next') or url_for('main.login')
            session['nickname'] = current_user.db_user.nickname
            redirect_url = '/'
            print('logged in successfully')
            return redirect(redirect_url)

    return render_template("login.html", title = 'sign in', form = form)



@lm.user_loader
def load_user(user_id):
    return lmUser(user_id)



@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
#@login_required
def logout():
    session['nickname'] = None
    logout_user()
    print(session['nickname'])
    return redirect('/login')




@app.route('/table-add', methods=['GET', 'POST'])
def table_add():
    dbname = request.args.get('dbname')
    text_element = request.args.get('text_element')

    flash(text_element)
    print(dbname, text_element)
    add_to_table(dbname, text_element)

    return ('', 204)



@app.route('/table')
def table():
    time.sleep(0.2)
    dbname = request.args.get('dbname')
    inner = request.args.get('inner')
    if inner is None or inner == 'false':
        inner = False
    else:
        inner = True
    print('/TABLE', dbname, inner, create_table_content(dbname))

    # print(render_template(table_html(dbname), tables=create_table_content(dbname, inner=inner)))
    return render_template(table_html(dbname), tables=create_table_content(dbname, inner=inner))


@app.route('/table-edit-form', methods=['GET', 'POST'])
def table_edit_form():
    dbname = request.args.get('dbname')
    base_data = request.args.get('base_data')
    #if dbname == 'clients':
        #return render_template(form_html(dbname), form=create_table_edit_form(dbname), dbname=dbname, tables=create_table_content("clients_inner") )
    return render_template(form_html(dbname), form=create_table_edit_form(dbname, data=base_data), inner_tables=create_inner_tables(dbname), dbname=dbname)


@app.route('/api/add', methods=['GET', 'POST'])
def add_function():
    dbname = request.args.get('dbname')
    form = create_table_edit_form(dbname, empty = (request.method == 'POST'))
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.cancel.data:
                return ('', 204) #!!!!!!!!НАДО ЗАКРЫТЬ ОКНО
            add_to_table(dbname, form)
        else:
            flash(form.errors)

    return ('', 204)
