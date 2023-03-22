from flask import Flask,request,jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle 
import os

modelo = pickle.load(open('models/modelo.sav','rb'))

colunas = ['tamanho','ano','garagem']
## Instanciando API
app = Flask(__name__)

## Autenticação basica
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basiuc_auth = BasicAuth(app)

## Rotas da API - criando a rota base

@app.route('/')

## Funcao a ser retornada quando usuaria acessar a rota
def home():
    return "Minha primeira API"

## Receber do usuario
@app.route('/sentimento/<frase>')
@basiuc_auth.required
## Requisito para acesso via autenticação
def sentimento(frase):
    """

    Funcao que define a probabilidade da frase ser positiva ou negativa

    Funcao polaridade:
    1) Varia de -1 a 1 
    2)Quanto mais proximo de -1 mais negativa é a mensagem enquanto que 
    mais próxima de 1 é positiva

    """
    
    tb = TextBlob(frase)
    tb_eng = tb.translate(from_lang='pt_br', to='en')
    polaridade = tb_eng.sentiment.polarity
    return "A polaridade é de : {}".format(polaridade)

## Metodo post =m receber em formato JSON
@app.route('/cotacao/', methods=['POST'])
@basiuc_auth.required
def cotacao():
    ##Entrada de dados por JSON
    dados = request.get_json()

    ## Garantindo que a resposta do usuario entre na forma correta da funcao predict
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco = preco[0])


## Rodar a API
if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')


## Rodando em "Running on http://127.0.0.1:5000"
# Endereco da maquina


