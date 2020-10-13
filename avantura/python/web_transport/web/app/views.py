
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm

from .forms import LoginForm
from .models import User, ROLE_USER, ROLE_ADMIN
from .menu import create_main_menu
from .tables import create_table_content, add_to_table, create_table_edit_form, table_html, form_html, Table



@app.route('/')
def index():
    user = {'nickname' : 'Burgers'}
    #return render_template("index.html", title = 'Home', user = user)
    return render_template("storage.html", menu = create_main_menu())



@app.route('/login', methods=['GET', 'POST'])
#@oid.loginhandler
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            #redirect_url = request.args.get('next') or url_for('main.login')
            redirect_url = '/'
            return redirect(redirect_url)

    return render_template("login.html", title = 'sign in', form = form)



@lm.user_loader
def load_user(user_id):
    return User.get(user_id)



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
    print(dbname, text_element)
    add_to_table(dbname, text_element)

    return ('', 204)



@app.route('/table')
def table():
    dbname = request.args.get('dbname')
    print(dbname)

    return render_template(table_html(dbname), source=create_table_content(dbname))


@app.route('/table-edit-form', methods=['GET', 'POST'])
def table_edit_form():
    dbname = request.args.get('dbname')
    if dbname == 'clients':
        return render_template("Clients_form_1.html", form=create_table_edit_form(dbname), dbname=dbname , source1=create_table_content("redakt1"), source2=create_table_content("redakt2"), source3=create_table_content("redakt3") )
    table = Table(["aip","str"],[["aaadata","bbbbbb"],["data","rrrrrr"]])
    return render_template(form_html(dbname),  form=create_table_edit_form(dbname), source=table, dbname=dbname)


@app.route('/api/add', methods=['GET', 'POST'])
def add_function():
    dbname = request.args.get('dbname')
    form = create_table_edit_form(dbname)
    if request.method == 'POST':
        print('val', form.submit.data, form.validate_on_submit())
        if form.validate_on_submit():
            if form.cancel.data:
                return ('', 204) #!!!!!!!!НАДО ЗАКРЫТЬ ОКНО
            add_to_table(dbname, form)
        else:
            flash(form.errors)

    return ('', 204)
