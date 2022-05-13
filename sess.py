from flask import Flask, session, request, url_for, redirect
from markupsafe import escape

import random
import json

app = Flask(__name__)

# generar con
#         python -c 'import secrets; print(secrets.token_hex())'
# o con 
#         python3 -c 'import secrets; print(secrets.token_hex())'
app.secret_key = "887e18e60395e07dd96ed8bafcc219d29d697aee814a01bde5f9c8e4236293b6"

class DB:
    def __init__(self, ruta='db.json'):
        self.ruta = ruta
        try:
            with open(self.ruta) as f:
                self.data = json.loads(f.read())
        except:
            # nueva base de datos
            self.data = {}
            self.data.setdefault('userdata', {})

    def guardar(self):
        with open(self.ruta, 'w') as f:
            f.write(json.dumps(self.data, indent=4, sort_keys=True))

    def nuevo_user(self):
        # uid numerico
        nuid = self.data.get('uid_next', 1000)
        self.data['uid_next'] = nuid + 1

        # uid como string (las claves de un json van a ser string)
        uid = str(nuid)

        ud = self.data['userdata'][uid] = {}

        n = random.choice([
                    "sinnombre",
                    "unnamed",
                    "unknown",
                    "sampletext",
                    ])
        a = random.choice([
                    "ramirez",
                    "gutierrez",
                    "lopez",
                    "martinez",
                    ])
        i = random.randint(100, 1000)

        ud['nombre'] = f"{n} {a} {i}"

        self.set_userdata(uid, ud)  # guarda
        return uid

    def get_userdata(self, uid):
        return self.data['userdata'].get(uid)

    def set_userdata(self, uid, ud):
        self.data['userdata'][uid] = ud
        self.guardar()

db = DB()

def ensure_valid_userid():
    if 'userid' in session:
        uid = session['userid']
        if db.get_userdata(uid) is not None:
            # el userid de la sesion ya estaba en la db
            return

    # generar uno nuevo
    session['userid'] = db.nuevo_user()
        
@app.route('/')
def index():
    ensure_valid_userid()
    return redirect(url_for("nombre"))

@app.route('/nombre', methods=['GET', 'POST'])
def nombre():
    ensure_valid_userid()

    uid = session['userid']
    ud = db.get_userdata(uid)

    if request.method == 'POST':
        ud["nombre"] = request.form['usernombre']
        db.set_userdata(uid, ud)
        return redirect(url_for('nombre'))

    nombre = ud["nombre"]
    return f'''
        <p>Buenas! Tu user id es {uid}, y tu nombre actual es: <b>{escape(nombre)}</b></p>
        <form method="post">
            <p>Nuevo nombre <input type=text name=usernombre>
            <p><input type=submit value=Cambiar>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('index'))
