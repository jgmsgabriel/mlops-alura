from flask import Flask, request, jsonify
from textblob import TextBlob
from flask_basicauth import BasicAuth
from sklearn.linear_model import LinearRegression
import pickle
import os

colunas = ['tamanho','ano','garagem']
modelo = pickle.load(open('../../models/modelo.sav','rb'))

app = Flask(__name__)
#app.config['BASIC_AUTH_USERNAME'] = 'admin'
#app.config['BASIC_AUTH_PASSWORD'] = 'admin1223'

app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return 'Minha primeira API'

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    polaridade = tb.sentiment.polarity
    return "polaridade: {}".format(polaridade)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True, host='0.0.0.0')