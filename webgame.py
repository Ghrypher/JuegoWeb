# Inspirado en https://flask.palletsprojects.com/en/2.1.x/quickstart/
# En un cmd:
#   > pip install flask
#   > set FLASK_APP=hello
#   > flask run
# En el browser, entrar a http://localhost:5000

from flask import Flask  
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/papel")
def rojardo():
    return render_template('papel.html')

@app.route("/tijera")
def azulicio():
    return render_template('tijera.html')

@app.route("/piedra")
def petardo():
    return render_template('piedra.html')
