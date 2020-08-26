
from flask import render_template
from app import app

class TMP():
    def __init__(self, num = 0, children = False):
        #if not children:
        self.html_class = 'parent'+str(num)
        self.child_name = 'child'+str(num)
        self.onclick = ''
        self.text = 'POPA'
        if children:
            self.children = [TMP(num), TMP(num)]


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname' : 'Burgers'}
    #return render_template("index.html", title = 'Home', user = user)
    return render_template("storage.html", menu = [TMP(0, True), TMP(1, True), TMP(2)])



