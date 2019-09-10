from flask import Flask, render_template, request, url_for, redirect
import json, requests
from googletrans import Translator
from flask_restful import Resource, Api

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="jhonyxf",
    password="Senha",
    hostname="jhonyxf.mysql.pythonanywhere-services.com",
    databasename="jhonyxf$default",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)

db = SQLAlchemy(app)

class Frases(db.Model):
    __tablename__ = "Frases"
    ID = db.Column(db.Integer, primary_key=True)
    Frase = db.Column(db.String(4096))

@app.route('/')
@app.route('/index')
def index():

    response = requests.get("https://api.chucknorris.io/jokes/random")
    content = json.loads(response.content)
    frasechuck = str(content['value'])
    translator = Translator()
    frasetraduzida = translator.translate(frasechuck,src="en",dest="pt")


    frase = Frases(Frase=frasechuck)
    db.session.add(frase)
    db.session.commit()

    return render_template('index.html', title='Home',frase=frasechuck,frasetraduzida=frasetraduzida.text)


@app.route('/frases/')
def listarFrases():
    frases = Frases.query.all()
    response = [{'id':i.ID,'frase':i.Frase} for i in frases]
    print(response)

    return render_template('frases.html', title='Frases',frases=response)

@app.route('/frase/<id>')
def delete(id):
    frase = Frases.query.filter_by(ID=id).first()
    db.session.delete(frase)
    db.session.commit()
    return redirect("/")
    #return {'status':'sucesso', 'mensagem':'frase excluida'}

@app.route('/formulario/')
def formulario():
    return render_template('formulario.html')

@app.route('/formulario/', methods=['POST'])
def post():
    texto = request.form['frase']
    print(texto)
    frase = Frases(Frase=texto)
    db.session.add(frase)
    db.session.commit()
    return render_template('formulario.html', title='Form',resultado="Cadastrado com sucesso!")


