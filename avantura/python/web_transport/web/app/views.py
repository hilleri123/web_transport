
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname' : 'Burgers'}
    #return render_template("index.html", title = 'Home', user = user)
    return render_template("sklad.html", title = 'Home', user = user)


