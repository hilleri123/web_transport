
from flask import render_template
from app import app

class TMP():
    def __init__(self):
        self.html_class = 'choice3'
        self.onclick = ''
        self.text = 'POPA'


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname' : 'Burgers'}
    #return render_template("index.html", title = 'Home', user = user)
    return render_template("storage.html", menu = [TMP(), TMP(), TMP()])



