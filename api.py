import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy  # type: ignore

app = Flask ('carros') #aplicação do tipo flask

app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #geralmente o pdrão é false, esse comando ativa as alterações

#anotar a senha, o banco, o loggin, o %40 substitui o @ na configuracao, ip, nome da base que queremos acessar
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:adm123@localhost/bd_carro'

mybd = SQLAlchemy(app)

#estrutura da tabela tb_carro
class Carros(mybd.Model):
    __tablename__ = 'tb_carro'
    id = mybd.Column(mybd.Integer, primary_key = True)
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(10))

    def to_json(self): 
        return{'id':self.id, 'marca':self.marca, 'modelo':self.modelo, 'valor':self.valor, 'cor':self.cor, 'numero_vendas':self.numero_vendas, 'ano': self.ano}

#API
@app.route('/carros', methods=['GET'])
def selecionar_carros():
    carro_objetos = Carros.query.all()

    carro_json = [carro.to_json() for carro in carro_objetos]

    return gera_response(200, 'carros', carro_json)

#selececionar por ID
@app.route("/carros/<id>", methods=["GET"])
def selecionar_carro_id(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    carro_json = carro_objetos.to_json()

    return gera_response(200, "carro", carro_json)


#Cadastrar carro
@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()

    try:
        carro = Carros(id=body["id"],marca=body["marca"],modelo=body["modelo"], valor=body["valor"], 
            cor=body["cor"], numero_vendas=body["numero_vendas"], ano=body["ano"])

        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201, "carros", carro.to_json(), "Criado com sucesso")
    
    except Exception as e:
        return gera_response(400, "carros", {}, f'O erro é referente a: {e}')
    

#atualizar carro
@app.route("/carros/<id>", methods=["PUT"])
def atualizar_carro(id):
    #consutar ID
    carro_objetos = Carros.query.filter_by(id=id).first()
    
    #corpo da requisição
    body = request.get_json()
#
    try:
        if('marca' in body):
            carro_objetos.marca = body['marca']
        if('modelo' in body):
            carro_objetos.modelo = body['modelo']
        if('valor' in body):
            carro_objetos.valor = body['valor']
        if('cor' in body):
            carro_objetos.cor = body['cor']
        if('numero_vendas' in body):
            carro_objetos.numero_vendas = body['numero_vendas']
        if('ano' in body):
            carro_objetos.ano = body['ano']
        
        mybd.session.add(carro_objetos)
        mybd.session.commit()

        return gera_response(200, "carros", carro_objetos.to_json(), "Atualizado com Sucesso !")
    
    except Exception as e:
        print(f"ERRO: {e}")
        return gera_response(400, "carros", {}, f"erro: {e}")
    

@app.route("/carros/<id>", methods=["DELETE"])
def deletar_carro(id):
    carro_objetos = Carros.query.filter_by(id=id).first()

    try:
        mybd.session.add(carro_objetos)
        mybd.session.commit()

        return gera_response(200, "carros", carro_objetos.to_json(), "Carro deletado")
    except Exception as e:
        return gera_response(400, "carro", {}, f'Erro: {e}')


def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype ='application/json')

app.run(port=5000, host='localhost', debug=True)

